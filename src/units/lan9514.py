import logging
import subprocess
from units.base_unit import BaseUnit
from lib.usb import Usb


class Lan9514(BaseUnit):
    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize LAN9514 test unit')

        self.bus = config.get('bus', 0)
        self.device = config.get('device', 0)

        self.usb = Usb()

    def state_0(self):
        self.logger.info('Start LAN9514 test, scan usb bus')
        self.usb.scan()
        self.nextState = self.state_1

    def state_1(self):
        self.logger.info('Find LAN9514 device: bus {bus:03d}, device {device:03d}'.format(bus=self.bus, device=self.device))
        self.device = self.usb.find_by_bus(self.bus, self.device)
        if self.device:
            self.nextState = self.state_2
        else:
            self.logger.error('Device not found!')
            self.nextState = self.state_finish

    def state_2(self):
        self.logger.info('Device found, implement next step')
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('LAN9514 test finished')
        self.nextState = self.request_finish
