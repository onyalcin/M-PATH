from .emotions import Emotions


class ECA(Emotions):
    def __init__(self, name='Matt', db='matt', body='smartbody',
                 goals=None, mood=('joy', 1.0), expressiveness=0.3):
        super().__init__(mood, expressiveness)
        self.name = name
        self.db = db
        self.body = body
        self.goals = goals
