from dialogue_system.survey.model.survey_instance_repository import SurveyInstanceRepository


class SurveyInstanceRepositoryInMem(SurveyInstanceRepository):
    def __init__(self):
        self._current_survey_instances = {}
        self._instances = {}

    def get_current(self, user_id):
        return self._current_survey_instances.get(user_id)

    def set_current(self, user_id, survey_instance_id):
        self._current_survey_instances[user_id] = survey_instance_id

    def get_user_surveys(self, user_id):
        user_all = []
        for id, instance in self._instances.items():
            if instance.user_id == user_id:
                user_all.append(instance)
        return user_all

    def get(self, survey_instance_id):
        return self._instances.get(survey_instance_id)

    def save(self, survey_instance):
        self._instances[survey_instance.id] = survey_instance
