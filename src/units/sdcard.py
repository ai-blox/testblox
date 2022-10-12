from src.units.base import BaseUnit
from src.lib.disk import Disk


class SdCard(BaseUnit):

    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize uSDCard test unit')

        self.blk_id = self.check_config_parameter('blk_id', 'mmcblk1')
        self.blk_size = self.check_config_parameter('blk_size', None)

        self.disk = Disk()

    def state_0(self):
        self.logger.info('Start uSDCard test')
        if not self.disk.lsblk():
            self.logger.error('lsblk failed')
            self.nextState = self.state_finish

        self.nextState = self.state_1

    def state_1(self):
        block = self.disk.find_block_device(self.blk_id)

        if block is None:
            self.logger.error("{} not found. uSDCard not working".format(self.blk_id))
            self.nextState = self.state_finish
        else:
            self.logger.info("{} found. uSDCard is working".format(self.blk_id))
            self.nextState = self.state_2

    def state_2(self):
        if self.blk_size is not None:
            if self.disk.check_block_device_size(self.blk_id, self.blk_size):
                self.logger.info("uSDCard has the right size: {}{}".format(self.blk_size['size'], self.blk_size['unit']))
                self.nextState = self.state_finish
            else:
                disk_size = self.disk.get_block_device_size(self.blk_id)
                self.logger.error("uSDCard has the wrong size: {}{} instead of {}{}".format(disk_size['size'], disk_size['unit'], self.blk_size['size'], self.blk_size['unit']))
                self.nextState = self.state_finish


    def state_finish(self):
        self.logger.info('uSDCard test finished')
        self.nextState = self.request_finish