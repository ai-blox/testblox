import logging
import subprocess

from unit import Unit



class Lan9514(Unit):

    def __init__(self, name):
        super(Lan9514, self).__init__(name)
        self.logger = logging.getLogger(name)
        self.logger.info('Initialize LAN9514 test unit')

    def state_0(self):
        self.logger.info('Start LAN9514 test')
        self.nextState = self.state_1

    def state_1(self):
        df = subprocess.check_output('lsusb')
        print(df)
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('LAN9514 test finished')
        self.nextState = self.request_finish



