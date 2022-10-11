import logging
import subprocess
from tests.base_test import BaseTest


class Lan9514(BaseTest):
    def __init__(self, name):
        super().__init__(name)
        self.logger = logging.getLogger(name)
        self.logger.info('Initialize LAN9514 test unit')

    def state_0(self):
        self.logger.info('Start LAN9514 test')
        self.nextState = self.state_1

    def state_1(self):
        df = subprocess.check_output('lsusb')
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('LAN9514 test finished')
        self.nextState = self.request_finish
