from importlib import import_module


class TestBench:

    def __init__(self, config):
        self.unit_tests = []

        for unit in config['unit-tests']:
            module_name = 'tests.' + unit['module']
            class_name = unit['class']
            unit_module = import_module(module_name)
            unit_class = getattr(unit_module, class_name)
            self.unit_tests.append(unit_class(unit['name']))

    def run_tests(self):

        for unit in self.unit_tests:
            unit.run()
