# loading tips from repository
import os
import json
from dialogue_system.survey.model.tip_repository import TipRepository
from dialogue_system.survey.model.tip import *

class TipRepositoryJson(TipRepository):
    def __init__(self, tip_dir):
        self._tip_dir = tip_dir

    def get_tips(self, tip_name):
        path = os.path.join(self._tip_dir, tip_name + '_tips.json')
        with open(path) as f:
            data = json.load(f)
        tips = TipCategory(
            name=tip_name,
            tips=[
                Tip(tip_id=item, tip_text=value)
                for item, value in data.items()
            ]
        )
        return tips
