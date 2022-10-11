import logging
import datetime


class BaseTest(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)

        self.start_time = None
        self.end_time = None

        self.start_time = None
        self.end_time = None

        self.currState = self.state_0
        self.nextState = self.currState
        self.finished = False
        self.finish_test = False
        self.error_msg = None

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
