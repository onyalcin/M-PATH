import logging


logger = logging.getLogger(__name__)


class MockBody:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, bml_list):
        logger.debug('Executing BML commands:\n%s', bml_list)
