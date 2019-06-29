
class TipHistory:
    """Tip history of one person"""

    def __init__(self, user_id, instances=None):
        self.user_id = user_id
        self.instances = instances or {}

    def get_tip_instance(self, tip_category):
        if tip_category in self.instances.keys():
            return self.instances[tip_category]
        else:
            raise KeyError(tip_category)

    def set_tip_instance(self, tip_category, given_tips=()):
        t = TipInstance(tip_category, given_tips)
        self.instances[tip_category] = t


class TipInstance:
    """An instance of tips given the category"""

    def __init__(self, tip_category, given_tips=()):
        self.name = tip_category
        self.given_tips = list(given_tips)

    def add_tip(self, tip_id):
        self.given_tips.append(tip_id)
