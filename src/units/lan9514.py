import logging
import subprocess
from units.base_unit import BaseUnit
from lib.usb import Usb


class Lan9514(BaseUnit):
    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize LAN9514 test unit')

        self.bus_id = config.get('bus', 0)
        self.device_id = config.get('device', 0)

        self.usb = Usb()

    def state_0(self):
        self.logger.info('Start LAN9514 test, scan usb bus')
        self.usb.scan()
        self.nextState = self.state_1

    def state_1(self):
        self.logger.debug('Find LAN9514 Hub: bus {bus:03d}, device {device:03d}'.format(bus=self.bus_id, device=self.device_id))
        device = self.usb.find_by_bus(self.bus_id, self.device_id)
        if device:
            self.logger.info('LAN9514 Hub OK')
            self.nextState = self.state_2
        else:
            self.logger.error('LAN9514 Hub not found!')
            self.nextState = self.state_finish

    def state_2(self):
        self.device_id += 1
        self.logger.debug('Find LAN9514 Ethernet adapter: bus {bus:03d}, device {device:03d}'.format(bus=self.bus_id, device=self.device_id))
        device = self.usb.find_by_bus(self.bus_id, self.device_id)
        if device:
            self.logger.info('LAN9514 Ethernet Adapter OK')
            self.nextState = self.state_3
        else:
            self.logger.error('LAN9514 Ethernet adapter not found')
            self.nextState = self.state_finish

    def state_3(self):
        self.logger.debug('TODO: Implement next steps')
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('LAN9514 test finished')
        self.nextState = self.request_finish
