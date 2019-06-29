from .base import BMLCommand

class Face(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, type=None, side=None, au=None,
                 start=None, ready=None, stroke=None, relax=None, end=None, amount=None):
        pass