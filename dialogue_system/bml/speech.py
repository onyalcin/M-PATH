from .base import BMLCommand
from xml.etree import ElementTree as et


class Mark(BMLCommand):
    def __init__(self, name):
        self.name = name


class Speech(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, type='application/ssml+xml', ref=None, id=None, text=''):
        if not self.text:
            self.text = []
        elif isinstance(self.text, str):
            self.text = [self.text]
        else:
            for i in self.text:
                assert isinstance(i, (str, Mark))

    def to_xml(self):
        el = et.Element(type(self).__name__.lower())
        for k, v in self.__dict__.items():
            if k != 'text':
                el.set(k, str(v))

        last_el = None
        for i in self.text:
            if isinstance(i, str):
                if last_el is None:
                    el.text = (el.text or '') + i
                else:
                    last_el.tail = (last_el.tail or '') + i
            else:
                sub_el = i.to_xml()
                el.append(sub_el)
                last_el = sub_el
        return el

    def __hash__(self):
        return hash((
            type(self),
            tuple((k, v) for k, v in self.__dict__.items() if k != 'text'),
            tuple(self.text or [])
        ))
