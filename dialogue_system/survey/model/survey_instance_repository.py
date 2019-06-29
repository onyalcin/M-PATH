
class SurveyInstanceRepository:
    def get_current(self, user_id):
        raise NotImplementedError()

    def set_current(self, user_id, survey_instance_id):
        raise NotImplementedError()

    def get(self, survey_instance_id):
        raise NotImplementedError()

    def save(self, survey_instance):
        raise NotImplementedError()
