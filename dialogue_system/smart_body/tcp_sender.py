import socket
import urllib.parse
import datetime
import logging
import time
from xml.etree import ElementTree as ET


logger = logging.getLogger(__name__)


class TCPSender:
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 8052
        self.BUFFER_SIZE = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_network(self):
        self.conn.connect((self.TCP_IP, self.TCP_PORT))

    def finit_network(self):
        self.conn.close()

    def send_msg(self, msg):
        self.conn.send(msg.encode())
        # data = self.conn.recv(BUFFER_SIZE)