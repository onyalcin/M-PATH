from .base import BMLCommand

class Gaze(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, target=None, start=None, direction=None, angle=None, joint_range=None, time_hint=None, priority_joint=None, joint_smooth=None):
        pass
