
class TipHistoryRepository:
    def get_current(self, user_id):
        raise NotImplementedError

    def set_current(self, user_id, tip_category):
        raise NotImplementedError

    def get(self, user_id):
        raise NotImplementedError()

    def save(self, user_id, tip_instance):
        raise NotImplementedError()
