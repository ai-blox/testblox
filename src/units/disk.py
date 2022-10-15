from src.units.base import BaseUnit
from src.lib.blockdevice import BlockDevice


class Disk(BaseUnit):

    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize disk test unit')

        self.path = self.check_config_parameter('path', mandatory=True)
        self.size = self.check_config_parameter('size', mandatory=True)
        self.partition_table = self.check_config_parameter('partition_table')

        if (self.path is None) or (self.size is None):
            self.logger.error('Failed to initialize disk test unit')
            return

        self.disk = BlockDevice(self.path)

        self.initialized = True

    def state_0(self):
        self.logger.info('Start Disk test')

        if not self.disk.read_partition_table():
            self.error("Read partition table failed")
            return
        self.nextState = self.state_1

    def state_1(self):
        if self.size is not None:
            if self.disk.check_partition_size(1, self.size):
                self.logger.info("Disk has the right size: {}".format(self.size))
                self.nextState = self.state_3
            else:
                self.logger.error("Disk has the wrong size: {} instead of {}".format(disk_size, self.size))
                self.nextState = self.state_finish

    def state_3(self):
        if self.partition_table is None:
            self.logger.info("No partition table provided, done for now")
            self.nextState = self.state_finish
        else:
            self.logger.info("Applying partition table")
            self.nextState = self.state_4

    def state_4(self):
        if self.disk.apply_partition_table(self.partition_table):
            self.logger.info("Partition table successful applied")
            self.nextState = self.state_5
        else:
            self.error("Applying partition table failed")

    def state_5(self):
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('uSDCard test finished')
        self.nextState = self.request_finish