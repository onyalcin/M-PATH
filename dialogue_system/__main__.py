import os
import logging
from concurrent.futures import ThreadPoolExecutor

from .ui import app_kivy
from .controller import Controller

from .input.microphone_thread import Microphone, DEFAULT_RATE

from .speech_recognition.google_speech_rec import GoogleSpeechRecognizer
from .speech_recognition.mock_speech_rec import MockSpeechRecognizer
from .speech_recognition.async_speech_rec import AsyncSpeechRecognizer

from .input.video_thread import VideoInput
from .emotion_recognition.video_recognition import Emo_VideoRecognizer

from .dialogue import db_utils
from .dialogue.simple_search import SimpleSearch

from .smart_body.smart_body import SmartBody
from .smart_body.mock_body import MockBody
from .agent.agent_queue import Agent
from .gesture import gs_utils
from .gesture.gesture_manager import GestureManager

# survey imports
from .survey import model
from .survey.infra.survey_repository_json import SurveyRepositoryJson
from .survey.infra.survey_instance_repository_inmem import \
    SurveyInstanceRepositoryInMem
from .survey.infra.tip_repository_json import TipRepositoryJson
from .survey.infra.tip_history_inmem import TipHistoryRepositoryInMem
from .survey.survey_controller import SurveyController

import config as cfg
from .actors.eca import ECA
from .actors.user import USER

logger = logging.getLogger().getChild(__package__)


if __name__ == '__main__':
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    from kivy.logger import Logger
    from kivy.config import Config
    Logger.setLevel(logging.INFO)
    Config.set('kivy', 'log_dir', 'D:\\kivy_logs\\')

    logger.info('\nagent: %s \nuser: %s', cfg.agent, cfg.user)

    eca = ECA(**cfg.agent)
    user = USER(**cfg.user)

    with ThreadPoolExecutor() as executor:
        speech_recognizer = GoogleSpeechRecognizer(sample_rate_hertz=DEFAULT_RATE)
        mock_speech_recognizer = MockSpeechRecognizer()

        async_speech_recognizer = AsyncSpeechRecognizer(
            executor=executor,
            recognizer=speech_recognizer)

        video_input = VideoInput(executor)
        video_emotion_recognizer = Emo_VideoRecognizer()

        db_search, db_learn = db_utils.load_dbs(os.path.join('.', 'data', eca.db))
        simple_search = SimpleSearch(db_search=db_search, db_learn=db_learn)

        gesture_db, gesture_categories, emotion_categories, au_categories = gs_utils.load_gesture_dbs(eca.body)
        gesture_manager = GestureManager(gesture_db, gesture_categories, emotion_categories, au_categories)

        # initiate survey service
        survey_repository = SurveyRepositoryJson('./data/survey_db')
        survey_instance_repository = SurveyInstanceRepositoryInMem()
        survey_service = model.SurveyService(
            survey_repository=survey_repository,
            survey_instance_repository=survey_instance_repository)

        tip_repository = TipRepositoryJson('./data/survey_db')  # FIXME arrange repositories
        tip_history_repository = TipHistoryRepositoryInMem()
        tip_service = model.TipService(tip_repository, tip_history_repository)

        reaction_service = model.ReactionService()

        survey_controller = SurveyController(survey_service=survey_service,
                                             reaction_service=reaction_service,
                                             tip_service=tip_service,
                                             goals=eca.goals)

        with \
                Microphone(executor) as microphone, \
                SmartBody() as character, \
                Agent(character, gesture_manager) as agent, \
                Controller(
                    agent=agent,
                    microphone=microphone,
                    speech_recognizer=async_speech_recognizer,
                    video_input=video_input,
                    video_emotion_recognizer=video_emotion_recognizer,
                    search_adapter=simple_search,
                    gesture_manager=gesture_manager,
                    survey_controller=survey_controller,
                    eca=eca,
                    user=user) as controller:
            app_kivy.run(controller)
