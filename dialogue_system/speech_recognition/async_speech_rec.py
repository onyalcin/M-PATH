import queue
import logging


logger = logging.getLogger().getChild(__name__)


DEFAULT_AUDIO_QUEUE_SIZE = 1
DEFAULT_WAIT_DATA_TIMEOUT = 5


class SpeechRecognitionTask:
    def __init__(self, recognizer, callback):
        self._recognizer = recognizer
        self._callback = callback
        self._queue = queue.Queue(maxsize=DEFAULT_AUDIO_QUEUE_SIZE)
        self._future = None

    def submit(self, chunk, final):
        self._queue.put((chunk, final), timeout=DEFAULT_WAIT_DATA_TIMEOUT)

    def _run(self):
        logger.info('Starting speech recognition task')

        for resp in self._recognizer.recognize(self._audio_gen()):
            self._callback(resp)

        logger.info('Finishing speech recognition task')

    def _audio_gen(self):
        while True:
            try:
                chunk, final = self._queue.get(timeout=DEFAULT_WAIT_DATA_TIMEOUT)
            except queue.Empty:
                logger.debug('Waited data for too long - aborting')
                break

            yield chunk
            self._queue.task_done()

            if final:
                logger.debug('Reached the end of the stream')
                break


class AsyncSpeechRecognizer:
    def __init__(self, executor, recognizer):
        self._executor = executor
        self._recognizer = recognizer

    def start(self, callback):
        task = SpeechRecognitionTask(
            recognizer=self._recognizer,
            callback=callback,
        )
        task._future = self._executor.submit(task._run)
        return task
