class Survey:
    def __init__(self, name, questions):
        self.name = name
        self.questions = questions

    def get_question(self, question_id):
        for question in self.questions:
            if question_id == question.id:
                return question
        raise KeyError(question_id)


class Question:
    def __init__(self, question_id, question_type, utterance):
        self.id = question_id
        self.type = question_type
        self.utterance = utterance


class MultipleChoiceQuestion(Question):
    class Choice:
        def __init__(self, text, reaction, actions, sentiment):
            self.text = text
            self.reaction = reaction
            self.actions = actions
            self.sentiment = sentiment

    def __init__(self, question_id, question_type, utterance, choices):
        super().__init__(question_id, question_type, utterance)
        self.choices = choices

    def get_choice(self, choice_id):
        return self.choices[choice_id]

    def get_choices_list(self):
        sentences = []
        for choice in self.choices:
            sentences.append(choice.text.lower())
        return sentences


class OpenEndedQuestion(Question):
    def __init__(self, question_id, question_type, utterance):
        super().__init__(question_id, question_type, utterance)
