import logging
from dialogue_system import bml
from .stomp_sender import StompSender


#logger = logging.getLogger(__name__)
logger = logging.getLogger().getChild(__name__)

class SmartBody:
    def __init__(self, character_name='ChrBrad'):
        self._stomp = None
        self._character_name = character_name

    def __enter__(self):
        self._stomp = StompSender()
        self._stomp.init_network()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stomp.finit_network()

    def execute(self, bml_list):
        #logger.debug('Executing BML commands:\n%s', bml_list)
        xml = bml.to_xml(bml_list)
        return self._stomp.send_BML(self._character_name, xml)

    def check_done(self, job_id):
        done = False
        while not done:
            try:
                if self._stomp.check_msg_done(job_id):
                    done = True
            except Exception:
                done = True
                logger.debug('Exception\n')
            except:
                logger.debug('Pass\n')
                pass

    def check(self, job_id):
        if self._stomp.check_msg_done(job_id):
            return True
        else:
            return False

    def execute_and_check(self, bml_list):
        return self.check_done(self.execute(bml_list))

    def clear_messages(self):
        self._stomp.clear_messages()
