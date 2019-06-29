from .base import BMLCommand

class Constraint(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, lexeme=None, type=None, stroke=None):
        pass
