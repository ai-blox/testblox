from src.units.base import BaseUnit
from src.lib.usb import Usb


class SdCard(BaseUnit):

    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize sdcard test unit')

        self.blk_id = self.check_config_parameter('blk_id', 'mmcblk1')

    def state_0(self):

        self.nextState = self.state_1

    def state_1(self):

        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('mmc test finished')
        self.nextState = self.request_finish