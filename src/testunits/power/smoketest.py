from src.testunits.baseunit import BaseUnit
import time

class SmokeTest(BaseUnit):
    def __init__(self, config, test_bench):
        super().__init__(config, test_bench)

        self.logger.info('Initialize SmokeTest test unit')

        self.voltage = self.check_config_parameter('voltage', mandatory=True)
        self.current = self.check_config_parameter('current', mandatory=True)
        self.max_current = self.check_config_parameter('max_current', mandatory=True)
        self.min_current = self.check_config_parameter('min_current', mandatory=True)
        self.power_up_delay = self.check_config_parameter('power_up_delay', 1)
        self.test_time = self.check_config_parameter('test_time', 5)
        self.leave_state = self.check_config_parameter('leave_state', True)
        self.power_supply = self.check_config_parameter('power_supply', mandatory=True)

        if (self.voltage is None) or (self.current is None) \
                or (self.max_current is None) or (self.min_current is None) \
                or (self.power_up_delay is None) or (self.test_time is None) \
                or (self.leave_state is None) or (self.power_supply is None):
            self.logger.error('Failed to initialize SmokeTest test unit')
            return

        self.tenma = self.test_bench.get_driver_by_name(self.power_supply)

        if (self.tenma is None):
            self.logger.error('Could not find the Tenma driver: %s' % self.power_supply)
            return

        self.initialized = True

    def state_0(self):
        self.logger.info('Start SmokeTest test')
        self.next_state = self.state_1

    def state_1(self):
        self.logger.info('Setup power supply')
        self.tenma.power_off()
        self.tenma.set_voltage(self.voltage)
        self.tenma.set_current(self.current)
        self.next_state = self.state_2

    def state_2(self):
        self.logger.info('Wait %d seconds' % self.power_up_delay)
        time.sleep(self.power_up_delay)
        self.next_state = self.state_3

    def state_3(self):
        self.logger.info('Turn on power supply')
        self.tenma.power_on()
        self.next_state = self.state_4

    def state_4(self):
        self.logger.info('Wait %d seconds before do measurement' % self.test_time)
        time.sleep(self.test_time)
        self.next_state = self.state_5

    def state_5(self):
        self.actual_current = self.tenma.get_actual_current()
        self.logger.info('Measured Current: %f', self.actual_current)


        if (self.leave_state == False):
            self.logger.info('Leave state == False, turnoff power supply')
            self.tenma.power_off()

        self.next_state = self.state_6

    def state_6(self) -> None:
        if (self.actual_current < self.min_current) or (self.actual_current > self.max_current):
            self.logger.error('Measure current is not within borders: %f < %f < %f' % (self.min_current, self.actual_current, self.max_current))
            self.tenma.power_off()

        self.next_state = self.state_finish

    def state_finish(self) -> None:
        self.logger.info('SmokeTest finished')
        self.next_state = self.request_finish
