
class UserHistoryRepository:
    def get_all(self, user_id):
        raise NotImplementedError()

    def get_last(self, user_id):
        raise NotImplementedError()

    def save(self, user_id, user_history):
        raise NotImplementedError()
