import logging
import datetime


class BaseUnit(object):

    def __init__(self, config):
        # Setup member variables
        self.name = config.get('name', 'NoName')
        self.logger = logging.getLogger(self.name)
        if self.name == 'NoName':
            self.logger.warning("Config parameter 'name' not found. Default to 'NoName'")

        self.config = config
        self.initialized = False

        self.start_time = None
        self.end_time = None

        self.currState = self.state_0
        self.nextState = self.currState
        self.finished = False
        self.finish_test = False
        self.error_msg = None

    def check_config_parameter(self, param, default=None, mandatory=False):
        if not (param in self.config):
            if mandatory:
                self.logger.error("Mandatory config parameter '{name}' not provided".format(name=param))
            else:
                self.logger.warning("Config parameter '{name}' not found. Default to '{default}'".format(name=param, default=default))
        return self.config.get(param, default)

    def run(self):
        self.currState = self.state_0
        self.nextState = self.currState
        self.finished = False
        self.finish_test = False
        self.error_msg = None

        self.start_time = datetime.datetime.now()
        while not self.finish_test:
            self.nextState = self.currState
            self.currState()
            self.currState = self.nextState
        self.end_time = datetime.datetime.now()
        duration = self.end_time - self.start_time
        minutes = divmod(duration.total_seconds(), 60)
        seconds = minutes[1]
        self.logger.info('Test finished, duration: {}:{}'.format(int(minutes[0]), seconds))

        self.finished = True

    def request_finish(self):
        self.finish_test = True

    def error(self, error_msg):
        self.logger.error(error_msg)
        self.error_msg = error_msg
        self.nextState = self.request_finish

    def state_0(self):
        raise NotImplementedError
