import random
from .survey_instance import SurveyInstance
from ...dialogue.similarity_model import LikertSimilarity

import logging

logger = logging.getLogger().getChild(__name__)


class SurveyService:
    def __init__(self, survey_repository, survey_instance_repository):
        self._survey_repository = survey_repository
        self._survey_instance_repository = survey_instance_repository
        self.similarity_model = LikertSimilarity()

    def start_new_survey(self, user_id, survey_name):
        # TODO: check the survey is not already started
        logger.info('Getting survey %s for user %s', user_id, survey_name)
        survey = self._survey_repository.get_survey(survey_name)
        new_survey_instance = SurveyInstance(
            user_id=user_id,
            survey_name=survey.name)

        self._survey_instance_repository.save(new_survey_instance)

        self._survey_instance_repository.set_current(
            user_id, new_survey_instance.id)

        return new_survey_instance

    def get_next_question(self, survey_instance):
        past_questions = set(
            answer.question_id for answer in survey_instance.answers)

        survey = self._survey_repository.get_survey(survey_instance.survey_name)
        all_questions = set(q.id for q in survey.questions)

        available_questions = list(all_questions - past_questions)
        try:
            #question_id = random.choice(available_questions)  # TODO: decide on whether we want random or sequential
            question_id = available_questions[0]

            survey_instance.current_question_id = question_id
            self._survey_instance_repository.save(survey_instance)
            return survey.get_question(question_id)
        except IndexError:
            return None

    def get_current_survey_instance(self, user_id):
        logger.debug('Getting survey instance for user %s', user_id)
        current_survey = self._survey_instance_repository.get_current(user_id)
        current_instance = self._survey_instance_repository.get(current_survey)
        return current_instance

    def set_answer(self, survey_instance, answer_text):
        # TODO validate answer is relevant
        survey_instance.set_answer(
            survey_instance.current_question_id, answer_text)
        self._survey_instance_repository.save(survey_instance)

    def check_answer(self, question, answer_text):
        if question.type == "multiple_choice":
            choices_text = question.get_choices_list()
            if answer_text in choices_text:
                answer_match = answer_text
            else:
                answer_match = self.similarity_model.predict(answer_text)
            if answer_match:
                return choices_text.index(answer_match)
            else:
                return None  # TODO! sentiment?
        elif question.type == "open_ended":
            return None  # TODO: send to sentiment analysis and return answer with sentiment score

    def check_and_return(self, survey_instance, answer_text):
        survey = self._survey_repository.get_survey(survey_instance.survey_name)
        question = survey.get_question(survey_instance.current_question_id)

        choice_id = self.check_answer(question, answer_text)
        if choice_id is not None:
            choice = question.get_choice(choice_id)
            return choice, survey_instance.current_question_id
        else:
            return None, survey_instance.current_question_id

    def end_survey(self, survey_instance):
        survey_instance.is_completed = True  # TODO: differentiate between complete and finished?
        survey_instance.current_question_id = None

        self._survey_instance_repository.set_current(
            survey_instance.user_id, None)
        self._survey_instance_repository.save(survey_instance)

    def _get_user_surveys(self, user_id):
        # checks all - check finished only -
        user_all = self._survey_instance_repository.get_user_surveys(user_id)
        return user_all

    def get_done_survey_names(self, user_id):
        finished = []
        user_all = self._get_user_surveys(user_id)
        for survey_instance in user_all:
            if survey_instance.is_completed:
                finished.append(survey_instance.survey_name)
        return finished  # Just returns the names

    def get_unfinished_surveys(self, user_id):
        unfinished = []
        user_all = self._get_user_surveys(user_id)
        for survey_instance in user_all:
            if not survey_instance.is_completed:
                unfinished.append(survey_instance)
        return unfinished  # This returns the instance list
