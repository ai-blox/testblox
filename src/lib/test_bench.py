from importlib import import_module
import datetime
import logging


class TestBench:

    def __init__(self, name, config):

        self.logger = logging.getLogger(name)
        self.logger.info('Initialize %s test bench' % name)

        self.start_time = None
        self.end_time = None

        self.unit_tests = []

        for unit in config['unit-tests']:
            module_name = 'src.units.' + unit['module']
            class_name = unit['class']
            unit_module = import_module(module_name)
            unit_class = getattr(unit_module, class_name)
            unit_obj = unit_class(unit['config'])

            # Only add the unit test if the initialization was successful
            if unit_obj is not None:
                self.unit_tests.append(unit_obj)

    def run_tests(self):

        self.start_time = datetime.datetime.now()

        for unit in self.unit_tests:
            if unit.initialized:
                unit.run()

        self.end_time = datetime.datetime.now()
        duration = self.end_time - self.start_time
        minutes = divmod(duration.total_seconds(), 60)
        seconds = minutes[1]
        self.logger.info('Test finished, duration: {}:{}'.format(int(minutes[0]), seconds))


