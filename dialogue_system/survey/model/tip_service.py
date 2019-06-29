import random
from .tip_history import TipHistory


class TipService:
    def __init__(self, tip_repository, tip_history_repository):
        self._tip_repository = tip_repository
        self._tip_history_repository = tip_history_repository

    def initiate_tip(self, user_id, tip_name):
        # TODO: what if these tips were already given
        try:
            tip_history = self._tip_history_repository.get(user_id)
        except AttributeError:
            tip_history = TipHistory(user_id=user_id)
        tip_history.set_tip_instance(tip_name)
        self._tip_history_repository.save(user_id, tip_history)
        self._tip_history_repository.set_current_category(user_id, tip_name)

    def get_next_tip(self, user_id, question_id):
        all_tips = self.get_current_tip_list(user_id)
        all_tips_for_question = [i.text for i in all_tips if i.id==str(question_id)][0] #combinedTip
        all_tip_ids = set('_'.join([str(question_id), str(text_id)]) for text_id in range(len(all_tips_for_question))) #combinedTip
        #all_tip_ids = set(i.id for i in all_tips)
        current_category = self._tip_history_repository.get_current_category(user_id)
        current_instance = self._tip_history_repository.get_current_instance(user_id)
        given_tips = current_instance.given_tips

        available_tips = list(all_tip_ids - set(given_tips))
        if not available_tips:
            return None

        tip_id = random.choice(available_tips)
        current_instance.add_tip(tip_id)
        self._tip_history_repository.set_current_instance(user_id, current_instance)
        tip_category = self._tip_repository.get_tips(current_category)

        return tip_category.get_tip_combined(tip_id) #combinedTip
        #return tip_category.get_tip(tip_id).text

    def get_current_tip_list(self, user_id):
        current_tip_category = self._tip_history_repository.get_current_category(user_id)
        current_tip_list = self._tip_repository.get_tips(current_tip_category).tips
        return current_tip_list
