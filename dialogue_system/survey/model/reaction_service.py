import random
import json


class ReactionService:
    def __init__(self):
        with open("./data/survey_db/reactions.json") as f:
            self.reactions = json.load(f)

    def return_reaction(self, reaction):
        r = random.choice(self.reactions[reaction])
        return r

    # TODO: add generation of reactions if there are none, or modifying according to the emotions