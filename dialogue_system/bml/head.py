from .base import BMLCommand

class Head(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, type=None, repeats=None, velocity=None, amount=None,
                 smooth=None, period=None, warp=None, accel=None, pitch=None, decay=None,
                 start=None, stroke=None, relax=None, end=None):
        pass
