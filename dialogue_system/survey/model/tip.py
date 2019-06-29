class TipCategory:
    def __init__(self, name, tips=()):
        self.name = name
        self.tips = list(tips)

    def get_tip(self, tip_id):
        for tip in self.tips:
            if tip_id == tip.id:
                return tip
        raise KeyError(tip_id)

    def get_tip_combined(self, combined_tip_id): # adding
        question_id, tip_id = [int(i) for i in combined_tip_id.split('_')]
        tip_list = self.get_tip(str(question_id)).text
        if len(tip_list) >= tip_id:
            return tip_list[tip_id]
        else:
            raise KeyError(combined_tip_id)

class Tip:
    def __init__(self, tip_id, tip_text):
        self.id = tip_id
        self.text = tip_text
