import re
from nltk import TweetTokenizer

from dialogue_system.emotion_recognition.word_recognition import NRC_AffectIntensity


class SentenceParser:
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.emo_parser = NRC_AffectIntensity()

    def parse_sent(self, str_response, expressiveness=0.3):  # TODO:Remove later on
        response_list = []
        for sent in re.split('[?.!]', str_response):
            word_list = [word for word in self.tokenizer.tokenize(sent)]
            if word_list:
                d = {"word_list": word_list,
                     "expressiveness": expressiveness}
                response_list.append(d)
        return response_list

    def return_emotions(self, word_list):
        emotion_list = []
        for word in word_list:
            # {'value': data[k]['value'], 'emotion': data[k]['emotion']}
            emotion_list.append(self.emo_parser.get_affect(word))
        return emotion_list

    def return_mood(self, word_list, mood):
        emotion_list = [None]*len(word_list)
        emotion_list[int(len(word_list)/2)] = {'value': mood[1], 'emotion': mood[0]}
        return emotion_list

    def parse_emo_sent(self, str_response, expressiveness=0.3):
        response_list = []
        d = {"word_list": [], "expressiveness": expressiveness, "emotion_list": []}
        for sent in re.split('[?.!]', str_response):
            for word in self.tokenizer.tokenize(sent):
                d["word_list"].append(word)
                d["emotion_list"].append(self.emo_parser.get_affect(word))
            d["word_list"].append(' . ')
        if d["word_list"]:
            response_list.append(d)
        return response_list

    def parse_mood_sent(self, str_response, expressiveness=0.3, mood=('joy', 1.0)):
        # This makes all sentence with a certain mood, regardless of word based sentiment
        responses = self.parse_sent(str_response, expressiveness=expressiveness)
        for response in responses:
            response['emotion_list'] = self.return_mood(response['word_list'], mood)
        return responses
