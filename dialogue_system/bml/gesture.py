from .base import BMLCommand
from enum import Enum


class Lexeme(Enum):
    YOU, ME, LEFT, RIGHT, NEGATION, CONTRAST, ASSUMPTION, RHETORICAL, INCLUSIVITY, QUESTION, OBLIGATION, GREETING, CONTEMPLATE = range(13)


class Gesture(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, lexeme=None, mode=None, type=None, name=None, style=None, target=None,
                 start=None, ready=None, stroke_start=None, stroke=None, stroke_end=None, relax=None, end=None,
                 joint_range=None, frequency=None, scale=None, emotion=None, additive=None): 
        pass
