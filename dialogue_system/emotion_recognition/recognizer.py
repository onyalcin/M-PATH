class VideoRecResult:
    def __init__(self, emotion, value, valence, au):
        self.emotion = emotion
        self.value = value
        self.valence = valence
        self.au = au


class VideoRecognizer:
    def recognize(self, frame):
        raise NotImplementedError()


class AudioRecognizer:
    def recognize(self, chunk):
        raise NotImplementedError()
