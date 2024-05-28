from importlib import import_module
from src.lib.database import DataBase
import datetime
import logging


class TestBench:

    def __init__(self, test_banch_name, database):

        self.logger = logging.getLogger(test_banch_name)
        self.logger.info('Initialize %s test bench' % test_banch_name)

        self.start_time = None
        self.end_time = None

        self.test_banch_name = test_banch_name
        self.database = database

        self.drivers = []
        self.test_units = []

        for driver in database.get_test_bench_drivers(self.test_banch_name):
            print(driver)
            module_name = 'src.drivers.' + driver['module']
            self.logger.info('Import driver %s:' % module_name)
            class_name = driver['class']
            driver_module = import_module(module_name)
            driver_class = getattr(driver_module, class_name)
            driver_obj = driver_class(database)

            # Only add the unit test if the initialization was successful
            if driver_obj is not None:
                self.drivers.append(driver_obj)

        for unit in config['test-units']:
            module_name = 'src.testunits.' + unit['module']
            self.logger.info('Import module %s:' % module_name)
            class_name = unit['class']
            unit_module = import_module(module_name)
            unit_class = getattr(unit_module, class_name)
            unit_obj = unit_class(unit['config'], self)

            # Only add the unit test if the initialization was successful
            if unit_obj is not None:
                self.test_units.append(unit_obj)

    def get_driver_by_name(self, name):
        for driver in self.drivers:
            if driver.name == name:
                return driver

        return None

    def run_tests(self):

        self.start_time = datetime.datetime.now()

        for unit in self.test_units:
            if unit.initialized:
                unit.run()

        self.end_time = datetime.datetime.now()
        duration = self.end_time - self.start_time
        minutes = divmod(duration.total_seconds(), 60)
        seconds = minutes[1]
        self.logger.info('Test finished, duration: {}:{}'.format(int(minutes[0]), seconds))

        for unit in self.test_units:
            unit.exit_test()