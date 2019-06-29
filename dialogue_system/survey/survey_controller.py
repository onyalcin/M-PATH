import logging

logger = logging.getLogger().getChild(__name__)


class SurveyController:
    def __init__(self, survey_service, reaction_service, tip_service, goals):
        self._mode = None
        self._survey_service = survey_service
        self._reaction_service = reaction_service
        self._tip_service = tip_service
        self._goals = goals
        self._responses = None

    def _init_responses(self):
        self._responses = {'reaction': None, 'coping': None, 'next': None}

    def on_input(self, user_id, text):
        # check if it is a trigger
        self._init_responses()
        if text.startswith('@'):
            return self._process_trigger(user_id, text[1:].split(' '))
        elif self._mode == 'survey':
            return self._on_input_survey(user_id, text)
        else:
            return None

    def _process_trigger(self, user_id, trigger):
        if trigger[0] == 'survey':
            self._mode = 'survey'
            if len(trigger) == 1:
                return self._start_survey(user_id, self._check_next_survey(user_id))
            else:
                return self._start_survey(user_id, trigger[1])
        elif trigger[0] == 'continue':
            if self._mode == 'survey':
                self._responses['next'] = self._next_survey_question(
                    self._survey_service.get_current_survey_instance(user_id))
                return self._responses
            else:
                return None  # FIXME: Follow up this path
        elif trigger[0] == 'end':
            if self._mode == 'survey':
                self._end_survey(self._survey_service.get_current_survey_instance(user_id))
                return None
        else:
            pass

    def _start_survey(self, user_id, survey_name):
        if not survey_name:
            return None
        survey_instance = self._survey_service.start_new_survey(
            user_id, survey_name)
        self._tip_service.initiate_tip(user_id, survey_name)
        self._responses['next'] = self._next_survey_question(survey_instance)
        return self._responses

    def _on_input_survey(self, user_id, answer_text):
        logger.debug('Processing survey answer')
        survey_instance = self._survey_service.get_current_survey_instance(user_id)
        choice, question_id = self._survey_service.check_and_return(survey_instance, answer_text)
        logger.debug('Processing choice')
        if choice is not None:
            self._survey_service.set_answer(survey_instance, choice.text)
            logger.debug('Set choice %s', choice.text)
            #responses.append(self._reaction_service.return_reaction(choice.reaction))
            self._responses['reaction'] = (self._reaction_service.return_reaction(
                choice.reaction), choice.reaction)
            logger.debug('Set reaction %s', choice.reaction)
            #self._append_responses(responses, self._process_actions(user_id, choice.actions, question_id))
            coping = self._process_actions(user_id, choice.actions, question_id)
            self._responses['coping'] = coping
            logger.debug('Set actions %s', choice.actions)
            #self._append_responses(responses, self._next_survey_question(survey_instance))
            self._responses['next'] = self._next_survey_question(survey_instance)
            return self._responses
        else:
            return None

    def _next_survey_question(self, survey_instance):
        if not survey_instance.is_completed:
            question = self._survey_service.get_next_question(survey_instance)
            if question is not None:
                return question.utterance
            else:
                self._end_survey(survey_instance)
                return None
        else:
            return None  # TODO: what happens if is completed

    def _end_survey(self, survey_instance):
        self._survey_service.end_survey(survey_instance)
        self._mode = None

    def _process_actions(self, user_id, actions, question_id):
        action_responses = []
        for action in actions:
            if action == 'offer_tips':
                text = self._tip_service.get_next_tip(user_id, question_id)
                action_responses.append(text)
            elif action.startswith('@'):
                self._append_responses(action_responses, self._process_trigger(user_id, action[1:].split(' ')))
        if action_responses:
            return ' . '.join(action_responses)
        else:
            return None

    def _append_responses(self, response_list, new_response):
        if new_response is not None:
            return response_list.extend(new_response)
        else:
            return response_list

    def _check_next_survey(self, user_id):
        done = self._survey_service.get_done_survey_names(user_id)
        remain = list(set(self._goals) - set(done))
        if remain:
            return remain[0]
        else:
            return None

    def check_goal_done(self, user_id):
        if self._survey_service.get_done_survey_names(user_id) == self._goals:
            return True
        else:
            return False