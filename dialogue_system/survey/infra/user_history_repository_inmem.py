from dialogue_system.survey.model.user_history_repository import UserHistoryRepository


class UserHistoryRepositoryInMem(UserHistoryRepository):
    def __init__(self):
        self._all_user_history = {}
        self._history_instance = []

    def get_all(self, user_id):
        return self._all_user_history.get(user_id)

    def get_last(self, user_id):
        return self._all_user_history.get(user_id)[-1]

    def save_instance(self, user_id, user_history):
        self._all_user_history[user_id].append(user_history)

