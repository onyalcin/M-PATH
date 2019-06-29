import time
import random
import logging
import threading
from enum import Enum
from dialogue_system import bml


logger = logging.getLogger().getChild(__name__)


class State(Enum):
    Idle = 0
    Listening = 1
    Thinking = 2
    Speaking = 3


class Agent(threading.Thread):
    def __init__(self, character, gesture_manager):
        super().__init__(name='Agent')
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._character = character
        self._gesture_manager = gesture_manager
        self._initial_state = State.Idle
        self._transition_queue = []

    def run(self):
        state = self._initial_state

        while not self._stop_event.is_set():
            new_state, param = self._get_next_state()

            if new_state is not None and new_state != state:
                logging.debug('Agent state transition: %s -> %s', state, new_state)
                state = new_state

            if state == State.Idle:
                self._state_idle()
            elif state == State.Listening:
                self._state_listening()
            elif state == State.Thinking:
                self._state_thinking()
            elif state == State.Speaking:
                self._state_speaking(param)

    def stop(self):
        self._stop_event.set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.join()

    def _transition(self, new_state, param=None, force=False):
        with self._lock:
            if force:
                self._transition_queue.clear()
            self._transition_queue.append((new_state, param))

    def send_bml(self, bml_list):  # FIXME : Does this belong here?
        self._character.execute(bml_list)

    def transition_idle(self):
        self._transition(State.Idle, force=True)

    def transition_listening(self):
        self._transition(State.Listening, force=True)

    def transition_thinking(self):
        self._transition(State.Thinking, force=True)

    def transition_speaking(self, response):
        assert isinstance(response, list)
        #for el in response:
        #    assert isinstance(el[0], bml.Speech)
        self._transition(State.Speaking, response)

    def set_mood(self, event):  # FIXME: Check if we dont need this
        self._character.execute(event)

    def _state_idle(self):
        if self._state_interrupted():
            return

        # FIXME: This is so horrible I cant even look at it
        if self._character.__class__.__name__ == 'SmartBody':
            self._character.execute([bml.Body(posture='ChrBrad@Idle01')])
        elif self._character.__class__.__name__ == 'UnityBody':
            self._character.execute([bml.Gesture(name='idle-pondering')])

        while not self._state_interrupted():
            time.sleep(0.01)

    def _state_listening(self):
        self._random_actions(state=State.Listening)

    def _state_thinking(self):
        self._random_actions(state=State.Thinking)

    def _state_speaking(self, response):
        if response is None:
            # If still in Speaking state but ran out of things to say
            self.transition_idle()
            return

        for part in response:
            self._character.execute_and_check(part)
        #self._character.execute_and_check(response[-1])

    def _random_actions(self, state=None, emotion=None, pad=None):
        while not self._state_interrupted():
            bml_list = self._gesture_manager.gesture_selection(state.name, emotion, pad)
            self._character.execute_and_check(bml_list)

    def _get_next_state(self):
        new_state, param = None, None

        with self._lock:
            if self._transition_queue:
                new_state, param = self._transition_queue.pop(0)

        return new_state, param

    def _state_interrupted(self):
        if self._stop_event.is_set():
            return True

        with self._lock:
            if self._transition_queue:
                return True

        return False
