from dialogue_system.survey.model.tip_history_repository import TipHistoryRepository
from dialogue_system.survey.model.tip_history import TipHistory


class TipHistoryRepositoryInMem(TipHistoryRepository):
    def __init__(self):
        self._current_category = {}
        self._history = {}

    def get_current_category(self, user_id):
        return self._current_category.get(user_id)

    def set_current_category(self, user_id, tip_category):
        self._current_category[user_id] = tip_category

    def get_current_instance(self, user_id):
        current_tip_category = self.get_current_category(user_id)
        tip_history = self._history.get(user_id)

        return tip_history.get_tip_instance(current_tip_category)

    def set_current_instance(self, user_id, tip_instance):
        self.get(user_id).set_tip_instance(tip_instance)

    def get(self, user_id):
        if self._history.get(user_id) is not None:
            return self._history.get(user_id)
        else:
            raise AttributeError

    def save(self, user_id, tip_history):
        self._history[user_id] = tip_history or TipHistory(user_id)
