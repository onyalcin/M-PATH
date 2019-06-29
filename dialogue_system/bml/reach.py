from .base import BMLCommand

class Reach(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, target=None, action=None, handle=None, foot_ik=None,
                 reach_finish=None, reach_velocity=None, reach_duration=None,
                 start=None):
        pass
