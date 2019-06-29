from io import BytesIO
from xml.etree import ElementTree as ET
from .base import BMLCommand


def to_xml(bml_commands):
    root = ET.Element('act')
    bml_tree = ET.SubElement(root, 'bml')
    for cmd in bml_commands:
        bml_tree.append(cmd.to_xml())

    buffer = BytesIO()
    ET.ElementTree(root).write(buffer, encoding='utf-8', xml_declaration=True)
    return buffer.getvalue().decode('utf-8')

# clean xml that only have bml for unity
def to_xml_clean(bml_commands):
    root = ET.Element('bml')
    for cmd in bml_commands:
        root.append(cmd.to_xml())

    buffer = BytesIO()
    ET.ElementTree(root).write(buffer, encoding='utf-8', xml_declaration=True)
    return buffer.getvalue().decode('utf-8')

def from_xml(xml, partial=False):
    types = {
        c.__name__.lower(): c
        for c in BMLCommand.__subclasses__()
    }

    if partial:
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><act><bml>' + xml + '</bml></act>'

    commands = []
    act = ET.fromstring(xml)
    bml = act[0]

    for el in bml:
        typ = types.get(el.tag.lower())
        if typ is None:
            raise Exception('Unknown BML command: {}'.format(el.tag))

        cmd = typ.from_xml(el)
        commands.append(cmd)

    return commands
