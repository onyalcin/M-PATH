import json
import random

class SurveyHandler(object):
    def __init__(self):
        self.user_surveys = []
        self.survey_history = {}
        self.current_survey = None
        self.survey_structure = None
        self.survey_tips = None
        with open('data/survey_db/reactions.json') as data:
            self.reactions = json.load(data)

    def trigger_survey(self, survey):
        with open('data/survey_db/' + survey + '.json') as data:
            self.survey_structure = json.load(data)
        with open('data/survey_db/' + survey + '_tips.json') as data:
            self.survey_tips = json.load(data)
        if survey not in self.user_surveys:
            self.user_surveys.append(survey)
            self.survey_history[survey] = {"questions":[], "tips":[]}
        # TODO else: if survey was conducted before or cancelled
        self.current_node = None  # TODO check if survey left undone
        self.current_tip = None  # TODO check if same tips were given before
        self.current_survey = survey
        self.continue_survey()

    def continue_survey(self):
        while True:
            if self.current_node is None: # TODO: randomize questions?
                self.current_node = "1"
            elif self.current_node not in self.survey_structure:
                self.survey_done()
                break  # TODO ??
            else:
                # TODO add finished question to the history
                node_dict = self.survey_structure[self.current_node]
                self.process_node(node_dict)
                self.current_node = str(int(self.current_node) + 1)

    def process_node(self, node_dict):
        utterance = node_dict["utterance"]
        triggers = node_dict["trigger"]
        responses = node_dict["responses"]
        for u in utterance:
            self._send_message(u)
        self.consume_triggers(triggers, responses)

    def consume_triggers(self, triggers, responses):
        type = responses["type"]
        if type == 'multipleChoice':
            score = self._createMultipleChoice(responses["choices"])
        elif type == 'openEnded':
            score = self._openEnded()

        reaction, trigger = triggers[score]
        self._reaction(reaction)
        self._trigger(trigger)

    def _openEnded(self):
        response = input('>') # TODO how to handle open-ended
        # do stuff
        score = None
        return score

    def _createMultipleChoice(self, choices):
        request_choice = 'Text me back the numbers to let me know.\n'
        a = 0
        for choice in choices:
            a += 1
            request_choice += str(a) + '.' + choice + '\t'
        selection = str(input(request_choice + '\n')).strip()
        score = int(selection)/a #change the score to dict matching
        # TODO handle cases that they answer sth else this better for recurring cases
        if score <= 0.6:
            return 0
        else:
            return 1

    def _offerTips(self):
        available_tips = set(self.survey_tips.keys()) - set(self.survey_history[self.current_survey]["tips"])
        if available_tips != set():
            current_tip = available_tips.pop()
            self.process_node(self.survey_tips[current_tip])
            self.survey_history[self.current_survey]["tips"].append(current_tip)
        else:
            self._send_message('Tips are done. You can always ask me for more tips anytime you want.')

    def _trigger(self, trigger):
        if trigger == 'offerTips':
            self._offerTips()
        elif trigger == 'offerProgram':
            self._offerProgram()
        elif trigger == 'nextQuestion':
            pass

    def _reaction(self, type):
        reaction = random.choice(self.reactions[type])
        self._send_message(reaction)

    def survey_done(self):
        print("Thank you for taking time to answer the questions! Let me know if I can help in any other way.")
        self.current_survey = None
        return True
        # TODO: exit module? how to break?

    def _send_message(self, utterance):
        print(utterance)
