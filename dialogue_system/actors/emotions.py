class Emotions:
    def __init__(self, mood=None, expressiveness=None):
        self._mood = mood
        self.expressiveness = expressiveness
        self._emotions = {"joy": 0.1, "sad": 0.1, "anger": 0.1, "fear": 0.1,
                          "surprise": 0.1, "disgust": 0.1, "neutral": 0.1}
        self._init_emotions()

    def _init_emotions(self):
        self._emotions[self._mood[0]] += self._mood[1]
        self._normalize(self._emotions)

    def _set_mood(self):
        max_emotion = max(self._emotions, key=self._emotions.get)
        value = self._emotions[max_emotion]
        self._mood = (max_emotion, value)

    def get_mood(self):
        self._set_mood()
        return self._mood

    def add_emotion(self, emotion, value=0.2):
        # positive, negative, neutral
        if emotion.startswith('positive'):  # FIXME: these should be generalized to all emotions
            emotion = 'joy'
        elif emotion.startswith('negative'):
            emotion = 'sad'

        if emotion in self._emotions.keys():
                self._emotions[emotion] += value
                self._normalize(self._emotions)
                return (emotion, self._emotions[emotion])
        else:
            raise KeyError('Given emotion do not exist %s', emotion)

    def _normalize(self, d):
        sum_values = sum(d.values())
        for i, k in d.items():
            try:
                d[i] = k / sum_values
            except ZeroDivisionError:
                pass
