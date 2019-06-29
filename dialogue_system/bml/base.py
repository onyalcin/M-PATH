import inspect
import functools
from xml.etree import ElementTree as et


class BMLCommand:
    name_mapper = {
        'target_pos': 'sbm:target-pos',  # gaze
        'joint_range': 'sbm:joint-range',  # gaze and gesture
        'priority_joint': 'sbm:priority-joint',  # gaze
        'handle': 'sbm:handle',  # gaze, reach, constraint,
        'joint_speed': 'sbm:joint-speed',  # gaze
        'joint_smooth': 'sbm:joint-smooth',  # gaze
        'fade_in': 'sbm:fade-in',  # gaze
        'fade_out': 'sbm:fade-out',  # gaze
        'style': 'sbm:style',  # gesture
        'frequency': 'sbm:frequency',  # gesture
        'scale': 'sbm:scale',  # gesture
        'additive': 'sbm:additive',  # gesture
        'smooth': 'sbm:smooth',  # head
        'period': 'sbm:period',  # head
        'warp': 'sbm:warp',  # head
        'accel': 'sbm:accel',  # head and locomotion
        'pitch': 'sbm:pitch',  # head
        'decay': 'sbm:decay',  # head
        'time_hint': 'sbm:time-hint',  # head
        'duration': 'sbm:duration',  # gaze
        # 'action': 'sbm:action',  # reach
        # 'foot_ik':'sbm:foot-ik',  # reach
        # 'reach_finish':'sbm:reach-finish',  # reach
        # 'reach_velocity':'sbm:reach-velocity',  # reach
        # 'reach_duration':'sbm:reach-duration',  # reach
        # 'follow':'sbm:follow',  # locomotion
        # 'scootaccel':'sbm:scootaccel',  # locomotion
        # 'angleaccel':'sbm:angleaccel',  # locomotion
        # 'numsteps':'sbm:numsteps',  # locomotion
        # 'root':'sbm:root',  # constraint
        # 'effector_root':'sbm:effector-root',  # constraint
        # 'constraint_type':'sbm:constraint-type',  # constraint
        # 'pos_x':'pos-x',  # constraint
        # 'pos_y':'pos-y',  # constraint
        # 'pos_z':'pos-z',  # constraint
        # 'rot_x':'rot-x',  # constraint
        # 'rot_y':'rot-y',  # constraint
        # 'rot_z':'rot-z',  # constraint
                   }

    @staticmethod
    def init_fields(fun):
        defaults = {
            prm.name: prm.default
            for prm in inspect.signature(fun).parameters.values()
            if prm.default is not inspect.Parameter.empty
        }

        @functools.wraps(fun)
        def _wrapper(self, **kwargs):
            attrs = {}
            attrs.update(defaults)
            attrs.update(kwargs)

            for k, v in attrs.items():
                if v is not None:
                    setattr(self, k, v)

            return fun(self, **kwargs)

        return _wrapper

    def to_xml(self):
        name = getattr(type(self), 'tag', type(self).__name__.lower())
        el = et.Element(name)
        for k, v in self.__dict__.items():
            if k in self.name_mapper.keys():
                el.set(self.name_mapper[k], str(v))
            else:
                el.set(k, str(v))
        return el

    @classmethod
    def from_xml(cls, el):
        return cls(**el.attrib)

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            ', '.join(
                '{}={}'.format(k, v)
                for k, v in self.__dict__.items()
            )
        )

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        if len(self.__dict__) != len(other.__dict__):
            return False

        for k, v in self.__dict__.items():
            if v != other.__dict__[k]:
                return False

        return True

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((
            type(self),
            tuple((k, v) for k, v in self.__dict__.items())
        ))
