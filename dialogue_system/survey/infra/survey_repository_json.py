# loading surveys from repository
import os
import json
from dialogue_system.survey.model.survey_repository import SurveyRepository
from dialogue_system.survey.model.survey import *


class SurveyRepositoryJson(SurveyRepository):
    def __init__(self, survey_dir):
        self._survey_dir = survey_dir

    def get_survey(self, survey_name):
        path = os.path.join(self._survey_dir, survey_name + '.json')
        with open(path) as f:
            data = json.load(f)
        questions = []
        for item in data["questions"]:
            questions.append(self.parse_question(item))

        s = Survey(survey_name, questions)
        return s

    def parse_question(self, question_dict):
        id = question_dict["id"]
        q_type = question_dict["type"]
        utterance = question_dict["utterance"]
        if q_type == "multiple_choice":
            choices_list = question_dict["choices"]
            choices = [MultipleChoiceQuestion.Choice(c['text'], c['reaction'], c['actions'], c['sentiment']) for c
                       in choices_list]  # should this be here or in the survey.py
            return MultipleChoiceQuestion(id, q_type, utterance, choices)
        elif q_type == "open_ended":
            return OpenEndedQuestion(id, q_type, utterance)
