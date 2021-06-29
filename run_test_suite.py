import argparse
import requests
import pathlib
import json
import datetime
import threading

from utils import ping_test
from utils import bandwidth_test
from utils.cpu_utils import record_cpu_utilization
from utils.file_utils import make_dir

from bandwidth_tests_config import bandwidth_tests_config
from ping_tests_config import ping_tests_config

def run_ping_tests(ping_results_dir):
    tests = ping_tests_config.keys()
    for test in tests:
        print(f"executing PING test: {test}")
        test_config = ping_tests_config[test]
        test_results_dir = f"{ping_results_dir}/{test}"
        make_dir(test_results_dir)
        ping_test.run(test_config, test_results_dir)
        # t runs for twice the test time, in case the test takes too long
        # and we don't want to just kill the thread so we will just join 
        # it with a timeout
        print(f"DONE.")


def run_bandwidth_tests(bandwidth_results_dir):
    tests = bandwidth_tests_config.keys()
    
    for test in tests:
        print(f"executing BANDWIDTH test: {test}")
        test_config = bandwidth_tests_config[test]
        test_results_dir = f"{bandwidth_results_dir}/{test}"
        make_dir(test_results_dir)
        bandwidth_test.run(test_config, test_results_dir)
        print(f"DONE.")

def get_results_dir_name(args_):
    if args_.results_dir:
        results_dir = args_.results_dir
        return results_dir

    today = datetime.date.today()
    folder_name = str(today)
    now = datetime.datetime.now()
    current_time_str = now.strftime("%Hh-%Mm-%Ss")
    results_dir_name = f"{folder_name}-{current_time_str}"
    return results_dir_name

def main():
    parser = argparse.ArgumentParser(description='Script to run whole test suite')
    parser.add_argument('--results-dir', help="results directory for extracting tests")
    args_ = parser.parse_args()

    results_dir = get_results_dir_name(args_)
    bandwidth_results_dir = results_dir + "/" + "bandwidth_tests"
    ping_results_dir = results_dir + "/" + "ping_tests"

    make_dir(results_dir)

    make_dir(bandwidth_results_dir)
    make_dir(ping_results_dir)

    run_bandwidth_tests(bandwidth_results_dir)
    run_ping_tests(ping_results_dir)


if __name__ == "__main__":
    main()