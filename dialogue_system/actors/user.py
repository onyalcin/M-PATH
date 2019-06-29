from .emotions import Emotions


class USER(Emotions):
    def __init__(self, name=None, id=1, mood=('neutral', 0.1), expressiveness=0.3):
        self.name = name
        self.id = id
        super().__init__(mood, expressiveness)
