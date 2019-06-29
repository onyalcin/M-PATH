class SpeechRecResult:
    def __init__(self, transcript, final=True):
        self.transcript = transcript
        self.final = final


class SpeechRecognizer:
    def recognize(self, audio_stream):
        raise NotImplementedError()
