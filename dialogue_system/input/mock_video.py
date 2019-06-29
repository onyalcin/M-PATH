import logging


logger = logging.getLogger(__name__)


class MockVideo:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self):
        logger.debug('Initiating video')
