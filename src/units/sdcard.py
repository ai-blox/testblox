from src.units.base import BaseUnit
from src.lib.disk import Disk


class SdCard(BaseUnit):

    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize uSDCard test unit')

        self.blk_id = self.check_config_parameter('blk_id', None)
        if self.blk_id is None:
            self.logger.info('Mandatory parameter: blk_id not provided')

        self.blk_size = self.check_config_parameter('blk_size', None)
        if self.blk_size is None:
            self.logger.info('Mandatory parameter blk_size not provide')

        self.partition_table = self.check_config_parameter('partition_table', None)

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
                self.nextState = self.state_3
            else:
                disk_size = self.disk.get_block_device_size(self.blk_id)
                self.logger.error("uSDCard has the wrong size: {}{} instead of {}{}".format(disk_size['size'], disk_size['unit'], self.blk_size['size'], self.blk_size['unit']))
                self.nextState = self.state_finish

    def state_3(self):
        if self.partition_table is None:
            self.logger.info("No partition table provided, done for now")
            self.nextState = self.state_finish
        else:
            self.logger.info("Applying partition table")
            self.nextState = self.state_4

    def state_4(self):
        if self.disk.apply_partition_table(self.blk_id, self.partition_table):
            self.logger.info("Partition table successful applied")
            self.nextState = self.state_5
        else:
            self.logger.error("Applying partition table failed")
            self.nextState = self.state_finish

    def state_5(self):
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('uSDCard test finished')
        self.nextState = self.request_finish