import logging
import datetime


class DriverBase(object):

    def __init__(self, config):
        # Setup member variables
        self.name = config.get('name', 'NoName')
        self.logger = logging.getLogger(self.name)
        if self.name == 'NoName':
            self.logger.warning("Config parameter 'name' not found. Default to 'NoName'")

        self.config = config

    def check_config_parameter(self, param, default=None, mandatory=False):
        if not (param in self.config):
            if mandatory:
                self.logger.error("Mandatory config parameter '{name}' not provided".format(name=param))
            else:
                self.logger.warning("Config parameter '{name}' not found. Default to '{default}'".format(name=param,
                                                                                                         default=default))
        return self.config.get(param, default)