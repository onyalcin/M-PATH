import logging
import cv2
import threading


logger = logging.getLogger().getChild(__name__)


class VideoInput:
    def __init__(self, executor):
        self._executor = executor
        self._video_capture = None
        self._stop_requested = threading.Event()
        self._future = None

    def __enter__(self):
        logger.debug('Initializing video capture')
        self._video_capture = cv2.VideoCapture(0)
        if not self._video_capture.isOpened():
            raise Exception('Failed to initialize camera')

        # Read one frame to initialize the camera
        self._video_capture.read()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._future:
            self.stop().result(timeout=1)
        self._video_capture.release()
        self._video_capture = None

    def start(self, callback):
        assert not self._future, 'Thread is already running'
        logger.info('Starting video thread')
        self._stop_requested.clear()
        self._future = self._executor.submit(self._run, callback)

    def stop(self):
        assert self._future, 'Thread is not running'
        logger.info('Stopping video thread')
        self._stop_requested.set()
        f = self._future
        self._future = None
        return f

    def _run(self, callback):
        logger.debug('_run')
        try:
            while not self._stop_requested.is_set():
                logger.debug('read')
                ret, frame = self._video_capture.read()
                if ret & self._video_capture.isOpened():
                    logger.debug('frame')
                    callback(frame)
                    logger.debug('callback done')
                else:
                    logger.debug('no frame')
        except Exception:
            logger.exception('Unhandled error in the video thread')
            raise
