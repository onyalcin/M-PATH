import json

class TipHandler(object):
    def __init__(self):
        self.tips = None
        self.tip_history = {}

    def trigger_tips(self, topic):
        with open('data/survey_db/' + topic + '_tips.json') as data:
            self.tips = json.load(data)

        if topic not in self.tip_history:
            self.tip_history[topic] = []
        self._offerTips()

    def _offerTips(self):
        if self.current_tip == None:
            self.current_tip = 0
        self.current_tip +=1
        if self.current_tip in self.tip_history[self.current_survey]:
            self._send_message(self.tip_history[self.current_survey][self.current_tip])
            self.tip_history[self.current_survey].append(self.current_tip)
        else:
            self.tips_done()

    def tips_done(self):
        self.current_tip = None
        self.tips = None
        self._send_message('Tips are done. You can always ask me for more tips anytime you want.')