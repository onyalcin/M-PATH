from .base import BMLCommand

class Body(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, posture=None, start=None, ready=None):
        pass
