import stomp
import urllib.parse
import datetime
import logging
import time
from xml.etree import ElementTree as ET


logger = logging.getLogger().getChild(__name__)


class StompSender:
    def __init__(self):
        self.headers = {}
        self.headers['ELVISH_SCOPE'] = 'DEFAULT_SCOPE'
        self.headers['MESSAGE_PREFIX'] = 'vrSpeak'
        self.listener = stomp.listener.TestListener()
        host_and_ports = [('localhost', 61613)]
        self.conn = stomp.Connection(host_and_ports=host_and_ports)
        self.conn.set_listener("", self.listener)

    def init_network(self):
        self.conn.start()
        self.conn.connect(username='admin', passcode='password', wait=True, timeout=5)
        self.conn.auto_content_length = False

    def finit_network(self):
        self.conn.disconnect()

    def on_disconnected(self):
        print('disconnected')
        self.init_network(self.conn)

    def send_BML(self, char_name, msg):
        """ send BML message. Assumes message is complete xml statement including prefix/suffix """
        str_id = '{:%M%S%f}'.format(datetime.datetime.now())
        msg = char_name + " ALL " + str_id + " " + msg
        self.send_msg("vrSpeak", msg, str_id)
        #print(msg)
        return str_id

    def send_SB(self, msg):
        """ send SmartBody python command """
        self.send_msg("sb", msg)

    def send_msg(self, prefix, msg, str_id):
        self.conn.subscribe(destination='/topic/DEFAULT_SCOPE', id=str_id, ack='auto')
        msg = prefix + " " + urllib.parse.quote_plus(msg)
        try:
            self.conn.send(body=msg, headers=self.headers, destination='/topic/DEFAULT_SCOPE', persistent= True)
            self.listener.wait_for_message()
        except:
            raise Exception

    def send_Unity(self, char_name, msg):
        """ send BML message. Assumes message is complete xml statement including prefix/suffix """
        self.conn.send(body=msg, headers=self.headers, destination='/topic/UNITY_BML')

    def send_JSON(self, msg):
        """ send SmartBody python command """
        self.conn.send(body=msg, headers=self.headers, destination='/topic/UNITY_JSON')

    def send_file(self, msg):
        pass

    def check_msg_done(self, str_id): # TODO: tie this to the smartbody for the next event
        for msg in list(self.listener.message_list):
            #if msg[0]['subscription'] == str_id:
            if str_id+'+end+complete' in msg[1]:
                #self.listener.message_list.clear() # clearing might not be a good idea, remove(msg) is prob better
                logger.debug('Completed:%s\n', msg[1])
                self.listener.message_list.clear()
                return True
            elif 'Remote+speech+process+timed+out' in msg[1]:
                self.listener.message_list.clear()
                raise Exception
            self.listener.message_list.remove(msg)  # FIXME: am i ugly?
        return False

    def clear_messages(self):
        self.listener.message_list.clear()
