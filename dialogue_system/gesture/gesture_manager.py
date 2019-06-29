import sys
import copy
import random
from dialogue_system.bml.speech import Speech, Mark
from dialogue_system.bml.gesture import Gesture
from dialogue_system.bml.head import Head
from dialogue_system.bml.face import Face
from dialogue_system.bml.event import Event

import itertools
import logging

logger = logging.getLogger().getChild(__name__)

class GestureManager:
    def __init__(self, gesture_db, gesture_categories, emotion_categories, au_categories):
        # Load databases
        self.gesture_db = gesture_db
        self.gesture_categories = gesture_categories  # TODO: should I remove gestures by word from this list?
        self.emotion_categories = emotion_categories
        self.au_categories = au_categories

        self.speech_id = 0  # FIXME: Control this from the controller or sth

    def gesture_selection(self, state=None, emotion=None, pad=None):
        if state != "Speaking":
            return self.return_behavior(self.get_state_gesture(state))
        if emotion is not None:
            return self.return_behavior(self.get_emotion_gesture(emotion))
        if pad is not None:
            pass  # TODO: how to consume P.A.D scale properly

    def get_state_gesture(self, state):
        return random.choice(self.gesture_categories[str(state)]["gestures"])

    def get_emotion_gesture(self, emotion):
        return random.choice(self.emotion_categories[emotion]["gestures"])

    def get_gesture_from_db(self, db,  category, name):
        return copy.deepcopy(db[category][name])

    def return_behavior(self, gesture_list, timing=None, amount=1.0):
        behavior_list = []
        if gesture_list is not None:
            for gesture in gesture_list:
                category, name = gesture.split("_")
                gesture_dict = self.get_gesture_from_db(self.gesture_db, category, name)
                if timing is not None:  # TODO better timing depending on PAD?
                    gesture_dict.update({'stroke': timing})
                if 'amount' in gesture_dict:
                    gesture_dict['amount'] = str(float(gesture_dict['amount'])*amount)
                behavior_list.append(getattr(sys.modules[__name__], category)(**gesture_dict))
            return behavior_list
        else:
            return None

    def return_gesture(self, gesture):  # gesture = {"category":"Gesture", "name":"BEAT"} # TODO: fix the timing, amount?
        gesture_dict = self.get_gesture_from_db(self.gesture_db, gesture["category"], gesture["name"])
        return getattr(sys.modules[__name__], gesture["category"])(**gesture_dict)

    def return_emotion_bml_list(self, emotion, amount=1.0):
        gestures = random.choice(self.emotion_categories[emotion]["gestures"])
        bml_list = self.return_behavior(gestures, amount=amount)
        return bml_list

    def return_au_category(self, behavior_name):
        behavior_list = []
        gesture_list = self.get_gesture_from_db(self.au_categories, behavior_name, "gestures")
        for gesture in gesture_list:
            behavior_list.append(self.return_gesture(gesture))
        return behavior_list

    # TODO: add handling speaking

    def gestures_on_word(self, word):
        for k, v in self.gesture_categories.items():
            if word in v["keywords"]:
                return random.choice(v["gestures"])
        return None

    def words_to_bml(self, word_list, speech_id):
        text = [Mark('T0'), '. ']
        for i in range(len(word_list)):
            text.append(Mark('T'+str(i+1)))
            text.append(word_list[i])
        text.append(Mark('T'+str(len(word_list)+1)))
        return [Speech(id=speech_id, text=text)]

    # return face gestures based on sentiments of the vader just passing sentiment and emotion_list
    # according to sentiment or personality re-arrange the
    '''
    def wg_to_bml(self, word_list, speech_id):  # merged word to bml and word to gesture
        text = [Mark('T0'), '. ']
        no_g = 0
        gesture_list = [None] * len(word_list)

        for i in range(len(word_list)):
            text.append(Mark('T'+str(i+1)))
            text.append(word_list[i])
            # add gestures
            g = self.gestures_on_word(word_list[i])
            if g:
                gesture_list[i] = self.return_behavior(g, timing=speech_id+':T'+str(i + 1))  # FIXME with timing??
                no_g += 1
        text.append(Mark('T' + str(len(word_list) + 1)))
        return [Speech(id=speech_id, text=text)], gesture_list, no_g
    '''

    def get_iconic(self, word_list, speech_id):
        no_g = 0
        gesture_list = [None]*len(word_list)
        for i in range(len(word_list)):
            g = self.gestures_on_word(word_list[i])
            if g:
                gesture_list[i] = self.return_behavior(g, timing=speech_id+':T'+str(i+1))
                no_g += 1
        return gesture_list, no_g

    # TODO: Justify proportion as the percentage of gestures
    def place_gestures(self, word_list, expressiveness, speech_id):
        gesture_list, no_g = self.get_iconic(word_list, speech_id)
        req = len(word_list)*expressiveness - no_g
        if req > 0:
            for x in range(0, int(req)):
                pos = self.find_farthest_position(gesture_list)
                gesture_list[pos] = self.return_behavior(self.get_state_gesture("beats"),
                                                         timing=speech_id+':T'+str(pos+1))
        elif req < 0:
            for x in range(0, int(req*-1)):
                pos = self.remove_excess_gestures(gesture_list)
                gesture_list[pos] = None
        return gesture_list

    def find_farthest_position(self, gesture_list):
        l = [1.0]*len(gesture_list)
        for i in range(len(gesture_list)):
            if gesture_list[i] is not None:
                l[i] = -99
                for j in range(len(gesture_list)):
                    if i != j:
                        l[j] -= 1.0/abs(i-j)
        return l.index(max(l))

    def place_timing_str(self, id, timing_no):
        return id+':T'+str(timing_no)

    def place_timing_list(self, gestures, timing_name, timing_str):
        for gesture in gestures:
            setattr(gesture, timing_name, timing_str)

    def return_mid_timing(self, time1, time2):
        id1, t1 = time1.split('T')
        id2, t2 = time2.split('T')
        mid = int((int(t2)-int(t1))/2)
        m1 = int(t1)+mid
        if mid != 0:
            return id1+'T'+str(m1)
        else:
            return None  # TODO: write tests for this, I didnt check all conditions

    # get list of dict/None [None, None, dict, None, None, dict]
    # dict = {"emotion":"joy", "value":0.5, "valence":0.9, "arousal":0.8, "dominance":0.6}
    # return Face(au='', start='', stroke='', relax='', ready='')
    def place_emotions(self, emotion_list, speech_id):
        emotions_bml, emotions = self.emotion_dict_to_bml(emotion_list, speech_id)
        # place the start and ending gestures
        self.place_timing_list(emotions_bml[0], 'ready', self.place_timing_str(speech_id, 0))
        self.place_timing_list(emotions_bml[-1], 'relax', self.place_timing_str(speech_id, len(emotion_list)+1))
        # for the rest, check if emotions change and place gesture timings
        for i in range(1, len(emotions)):
            stroke1 = emotions_bml[i - 1][0].stroke
            stroke2 = emotions_bml[i][0].stroke
            if emotions[i-1] != emotions[i]:
                logger.debug('emotions %s %s:', emotions[i-1], emotions[i])
                t1 = self.return_mid_timing(stroke1, stroke2)
                if t1:
                    self.place_timing_list(emotions_bml[i-1], 'relax', t1)
                    self.place_timing_list(emotions_bml[i], 'ready', t1)
            else:
                self.place_timing_list(emotions_bml[i-1], 'relax', stroke1)
                self.place_timing_list(emotions_bml[i], 'ready', stroke2)
        return [item for sublist in emotions_bml for item in sublist]

    def emotion_dict_to_bml(self, emotion_list, speech_id):
        emotions = []
        emotions_bml_list = []
        for i in range(len(emotion_list)):
            emotion = emotion_list[i]
            if emotion is not None:
                current_emotion = emotion['emotion']
                amplitude = emotion['value']
                emotions.append(current_emotion)
                au_list = self.return_emotion_bml_list(current_emotion, amount=amplitude) # TODO: currently amount does nothing
                for au in au_list:
                    au.stroke = speech_id + ':T' + str(i + 1)
                emotions_bml_list.append(au_list)
        return emotions_bml_list, emotions

    def remove_excess_gestures(self, gesture_list):
        l = [0.0] * len(gesture_list)
        for i in range(len(gesture_list)):
            if gesture_list[i] is None:
                l[i] = -99
            for j in range(len(gesture_list)):
                if i != j:
                    l[j] += 1.0 / abs(i - j)
        return l.index(max(l))

    def remove_none_list(self, item_list):
        return itertools.chain.from_iterable([item for item in item_list if item is not None])

    def mood_blending(self, mood, start_id, end_id):
        mood_bml = self.return_emotion_bml_list(mood[0], amount=mood[1])
        self.place_timing_list(mood_bml, 'ready', start_id+':start')
        self.place_timing_list(mood_bml, 'relax', end_id+':end')
        return mood_bml

    # Things I had for offline tests and MTurk
    def default_face_mood(self, mood=None, value=None):
        #if mood is not None:
        #    self.mood = mood
        #if value is not None:
        #    self.mood_value = value
        au_list = self.return_emotion_bml_list(self.mood, amount=self.mood_value)
        return self.default_face_from_au_list(au_list)
    
    def default_face_from_au_list(self, au_list):
        event_list = []
        for au in au_list:
            event_list.append(Event(message="char ChrBrad viseme au_" + str(au.au) + " " + str(au.amount)))
        return event_list

    '''
    def set_neutral(self):  # FIXME: Do we really need this?
        self.mood = None
        self.mood_value = 1.0
        event_list = []
        for au in ["1_left", "1_right", "2_left", "2_right", "4_left", "4_right", "5", "6", "7",
                   "12_left", "12_right", "26", "131"]:
            event_list.append(Event(message="char ChrBrad viseme au_"+au+ " 0.00"))
        return event_list
    '''
    def get_bml_speech_response(self, response_list, mood=None):  # No nlp processing here, it gets the data pre-splitted
        # list of dicts with [{"word_list":[,,,,], "emotion_list":[,,,,],
        #  "expressiveness":0.2},{...}]
        bml_list = []
        speech_id_start = 'speech' + str(self.speech_id)
        for response in response_list:
            speech_id = 'speech' + str(self.speech_id)
            # add speech to bml
            bml = self.words_to_bml(response["word_list"], speech_id)
            # add gestures to bml
            gesture_list = self.place_gestures(response["word_list"], response["expressiveness"], speech_id)
            bml += self.remove_none_list(gesture_list)  # TODO: careful of what we did here
            # add emotions to bml if exists
            if "emotion_list" in response:
                if response["emotion_list"] != [None] * len(response["emotion_list"]):
                    bml += self.place_emotions(response["emotion_list"], speech_id)
            # TODO: change gestures according to personality
            if mood:
                bml += self.mood_blending(mood, speech_id_start, speech_id)  # FIXME! Decide how to use mood
            bml_list.append(bml)
            self.speech_id = (self.speech_id + 1) % 10
        return bml_list
