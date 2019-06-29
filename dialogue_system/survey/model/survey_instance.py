import uuid


class SurveyInstance:
    def __init__(self, user_id, survey_name, current_question=None,
                 is_completed=False, answers=(), id=None):
        self.id = id or uuid.uuid4()
        self.user_id = user_id
        self.survey_name = survey_name
        self.is_completed = is_completed
        self.current_question_id = current_question
        self.answers = list(answers)

    def set_answer(self, question_id, answer_text):
        a = Answer(question_id, answer_text)
        self.answers.append(a)


class Answer:
    def __init__(self, question_id, answer_text):
        self.question_id = question_id
        self.answer_text = answer_text
