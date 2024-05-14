from src.test_units.base import BaseUnit

class Login(BaseUnit):
    def __init__(self, config):
        super().__init__(config)

        self.logger.info('Initialize login test unit')

        self.user = self.check_config_parameter('user', mandatory=True)
        self.password = self.check_config_parameter('password', mandatory=True)

        if (self.user is None) or (self.password is None):
            self.logger.error('Failed to initialize login test unit')
            return

        self.initialized = True

    def state_0(self):
        self.logger.info('Start login test')
        self.nextState = self.state_1

    def state_1(self):
        self.logger.info('Login OK')
        self.nextState = self.state_finish

    def state_finish(self):
        self.logger.info('login test finished')
        self.nextState = self.request_finish
