import logging
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from .recognizer import SpeechRecResult, SpeechRecognizer


logger = logging.getLogger().getChild(__name__)


DEFAULT_LANGUAGE_CODE = 'en-US'  # a BCP-47 language tag


class GoogleSpeechRecognizer(SpeechRecognizer):
    def __init__(self, sample_rate_hertz, language_code=DEFAULT_LANGUAGE_CODE):
        self._client = speech.SpeechClient()

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code)

        self._streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

    def recognize(self, audio_stream):
        requests = (
            types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_stream
        )

        last_transcript = ''

        for interim_result in self._client.streaming_recognize(self._streaming_config, requests):
            for result in interim_result.results:
                if result.is_final:
                    logger.debug('Finished: %s', result.is_final)
                    logger.debug('Stability: %s', result.stability)
                    for alternative in result.alternatives:
                        logger.debug('Confidence: %s', alternative.confidence)
                        logger.debug('Transcript: %s', alternative.transcript)

                    # Choose the most confident alternative
                    alts = [(alt.confidence, alt) for alt in result.alternatives]
                    alts.sort(reverse=True)
                    transcript = alts[0][1].transcript if alts else ''
                    last_transcript = transcript

                    yield SpeechRecResult(transcript=transcript, final=False)

        yield SpeechRecResult(transcript=last_transcript, final=True)
