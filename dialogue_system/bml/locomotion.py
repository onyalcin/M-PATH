from .base import BMLCommand

class Locomotion(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, target=None, type=None, manner=None, facing=None, speed=None,
                 follow=None, proximity=None, accel=None, scootaccel=None, angleaccel=None, numsteps=None):
        pass