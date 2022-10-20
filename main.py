import os
import sys
import argparse
import logging
import yaml
from src.lib.test_bench import TestBench


def setup_logger(debug):
    log_level = logging.DEBUG if debug else logging.WARNING
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ret_logger = logging.getLogger()
    ret_logger.setLevel(log_level)

    file_handler = logging.FileHandler('test-results.log')
    file_handler.setFormatter(log_formatter)
    ret_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    ret_logger.addHandler(console_handler)

    return ret_logger


def load_config(filename):
    config_path = "config.yml" if not filename else filename
    if not os.path.exists(config_path):
        print("ERROR: config file not found: %s" % config_path)
        return None

    with open(config_path, 'r') as ymlfile:
        ret_configuration = yaml.full_load(ymlfile)

    return ret_configuration


def create_test_bench(name, config):
    return TestBench(name, config)


if __name__ == "__main__":

    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

    parser = argparse.ArgumentParser(description='AI-BLOX test system')
    # general
    parser.add_argument('--tb', type=str, help='Select test bench: mx1010-1, mx1010-2, ...')
    parser.add_argument('--loop', action='store_true', help='Start again when test is finished')

    # reporting
    parser.add_argument('--debug', action='store_true', help='Show debug log')

    # miscellaneous
    parser.add_argument('--config', type=str, help='Specify config file')

    args = parser.parse_args()

    # Logger configuration
    logger = setup_logger(args.debug)

    # General configuration
    configuration = load_config(args.config)
    if not configuration:
        print('Failed to load configuration')
        exit(1)

    if args.tb is None:
        print('No testbench selected')
        exit(1)

    test_config = configuration['test-benches']
    if args.tb not in test_config:
        print('no such test bench: %s' % args.tb)
        exit(1)

    test_bench_config = test_config[args.tb]
    test_bench = create_test_bench(args.tb, test_bench_config)

    # -------------------------------------------
    # Test Loop
    # -------------------------------------------

    while True:

        test_bench.run_tests()

        if not args.loop:
            print('Ready to leave')
            break
