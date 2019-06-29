import logging
import functools

from .dialogue import text_normalization
from .dialogue.sentence_preparation import SentenceParser

from .empathy_mechanism.empathy_mechanism import Empathy


logger = logging.getLogger().getChild(__name__)


class Controller:
    def __init__(self, agent, microphone, speech_recognizer,
                 video_input, video_emotion_recognizer, search_adapter,
                 gesture_manager, survey_controller, eca, user):
        self._microphone = microphone
        self._microphone_task = None

        self._speech_recognizer = speech_recognizer

        self._video_input = video_input
        self._video_emotion_recognizer = video_emotion_recognizer

        self._microphone_thread = None
        self._speech_rec_thread = None

        self._agent = agent

        self._context = None
        self._intent = None

        self._search_adapter = search_adapter
        self._sentence_parser = SentenceParser()  # TODO: is this okay to pass it like this?

        self._gesture_manager = gesture_manager
        self._empathy_mechanisms = Empathy()

        # survey service
        self._survey_controller = survey_controller

        self.eca = eca
        self.user = user

    def __enter__(self):
        self._microphone.__enter__()
        self._video_input.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._microphone.__exit__(exc_type, exc_val, exc_tb)
        self._video_input.__exit__(exc_type, exc_val, exc_tb)
        pass

    def process_text_input(self, text):
        self._on_input(text)

    def start_listening(self):
        if self._microphone_task:
            return

        logger.info('Starting to listen')
        self._agent.transition_listening()

        speech_rec_task = self._speech_recognizer.start(
            callback=self._on_speec_rec_result)

        self._microphone_task = self._microphone.enable(
            callback=functools.partial(self._on_microphone_data, speech_rec_task))

        self._video_input.start(
            callback=self._on_frame)

    def stop_listening(self):
        if not self._microphone_task:
            return

        logger.info('Stopping to listen')

        self._microphone_task.disable()
        self._microphone_task = None

        self._video_input.stop()

        self._agent.transition_thinking()

    def _on_microphone_data(self, sr_task, chunk, final):
        logger.debug('Audio chunk received, final: %s', final)
        sr_task.submit(chunk, final)
        # TODO: add another task submission to the audio emo rec or pause detection queue
        return True

    def _on_speec_rec_result(self, rec_result):
        logger.debug('Speech recognition result received')
        if rec_result.final:
            self._on_input(rec_result.transcript)

    def _on_frame(self, frame):
        emotions = self._video_emotion_recognizer.recognize(frame)
        emotion, value = self._empathy_mechanisms.affect_match(emotions)
        logger.info("EMOTION RECOGNITION RESULTS: %s, %s", emotion, value)
        # TODO:send the results to the emotion fusion as a queue
        if emotion is not None:
            bml_list = self._gesture_manager.return_emotion_bml_list(emotion, amount=value)
            self._agent.send_bml(bml_list)

    def _on_input(self, text):
        logger.info('Processing input: %s', text)
        # TODO: adding word/face based emotion recognition here
        # check if it is a trigger
        if self._survey_controller.check_goal_done(self.user.id):  # If goal is done, do post-survey
            user_mood = self.user.get_mood()
            self._survey_controller.on_input(self.user.id, '@survey test')
            responses = self._survey_controller.on_input(self.user.id, user_mood[0])
        else:
            responses = self._survey_controller.on_input(self.user.id, text)
        if responses is not None:
            self._context = 'survey'
            self._on_survey(responses)
        else:
            self._on_input_qa(text)

    def _on_survey(self, responses):
        logger.info("Response: %s", responses)
        if responses['reaction']:
            emotion = self.user.add_emotion(responses['reaction'][1])
            self._send_response(responses['reaction'][0], emotion)
        if responses['coping']:
            self._send_response(responses['coping'])
        if responses['next']:
            self._send_response(responses['next'])
        else:
            self._send_response('Thank you so much for taking the survey!')

    def _on_input_qa(self, text):
        clean_query = text_normalization.clean(text)

        response, intent, context = self._search_adapter.get_response(clean_query, self._intent, self._context)
        self._intent = intent
        self._context = context

        self._send_response(response)

        # Consuming actions from the intent
        if intent.startswith('@'):
            self._on_input(intent)  # FIXME add nex survey selection

    def _get_bml_response(self, response, mood=None):
        parsed_response = self._sentence_parser.parse_emo_sent(response, expressiveness=0.3)
        bml_response = self._gesture_manager.get_bml_speech_response(parsed_response, mood)
        return bml_response

    def _send_bml_response(self, bml_response):
        self._agent.transition_speaking(bml_response)

    def _send_response(self, response, mood=None):
        if not mood:
            mood = self.eca.get_mood()
        logger.info('Current mood: %s', mood)
        logger.info('Response: %s', response)
        bml_response = self._get_bml_response(response, mood=mood)
        logger.debug('Bml response: %s', bml_response)
        self._send_bml_response(bml_response)
