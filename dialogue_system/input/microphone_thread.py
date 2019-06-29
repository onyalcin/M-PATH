import logging
import pyaudio
import threading


logger = logging.getLogger().getChild(__name__)


DEFAULT_RATE = 16000
DEFAULT_CHUNK = int(DEFAULT_RATE / 1)  # 1s


class MicrophoneStreamTask:
    def __init__(self, audio_interface, rate, chunk, callback):
        self._audio_interface = audio_interface
        self._rate = rate
        self._chunk = chunk
        self._callback = callback

        self._stop_requested = threading.Event()
        self._callback_done = threading.Event()
        self._future = None

    def disable(self):
        self._stop_requested.set()

    def _run(self):
        audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._mic_callback,
        )

        self._callback_done.wait()

        audio_stream.stop_stream()
        audio_stream.close()

    def _mic_callback(self, in_data, frame_count, time_info, status_flags):
        try:
            final = self._stop_requested.is_set()

            if not self._callback(in_data, final) or final:
                self._callback_done.set()
                return None, pyaudio.paComplete
        except:
            logger.exception('Exception in microphone callback')
            self._callback_done.set()
            return None, pyaudio.paAbort

        return None, pyaudio.paContinue


class Microphone:
    def __init__(self, executor, rate=DEFAULT_RATE, chunk=DEFAULT_CHUNK):
        self._rate = rate
        self._chunk = chunk
        self._executor = executor
        self._audio_interface = None

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._audio_interface.terminate()

    def enable(self, callback):
        task = MicrophoneStreamTask(
            audio_interface=self._audio_interface,
            rate=self._rate,
            chunk=self._chunk,
            callback=callback,
        )
        task._future = self._executor.submit(task._run)
        return task
