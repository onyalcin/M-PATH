from .recognizer import SpeechRecResult


class MockSpeechRecognizer(object):
    def __init__(self):
        pass

    def recognize(self, audio_stream):
        for _ in audio_stream:
            pass

        yield SpeechRecResult(final=True, transcript='hello')
