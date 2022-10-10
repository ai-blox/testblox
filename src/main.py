import os
import sys
import argparse
import logging


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

def create_test_bench(args, configuration):
    test_bench_type = configuration['test-benches']


if __name__ == "__main__":

    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

    parser = argparse.ArgumentParser(description='AI-BLOX test system')
    # general
    parser.add_argument('--tb', action='store_true', help='Select test bench: mx1010-1, mx1010-2, ...')
    parser.add_argument('--loop', action='store_true', help='Start again when test is finished')

    # reporting
    parser.add_argument('--debug', action='store_true', help='Show debug log')

    args = parser.parse_args()

    # Logger configuration
    logger = setup_logger(args.debug)

    # -------------------------------------------
    # Test Loop
    # -------------------------------------------

    while True:

        if not args.loop:
            print('Ready to leave')
            break
