from .base import BMLCommand

class Saccade(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, mode=None, finish=True, direction=None, magnitude=None, duration=None):
        pass
