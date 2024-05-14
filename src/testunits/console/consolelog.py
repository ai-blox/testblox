from src.testunits.baseunit import BaseUnit
import time

class ConsoleLog(BaseUnit):
    def __init__(self, config, test_bench):
        super().__init__(config, test_bench)

        self.logger.info('Initialize InitConsoleLog test unit')

        self.serial_port = self.check_config_parameter('serial_port', mandatory=True)

        if (self.serial_port is None) :
            self.logger.error('Failed to initialize  test unit')
            return