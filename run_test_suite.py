import argparse
import requests
import pathlib
import json
import datetime

from utils import ping_test
from utils import bandwidth_test

__PING_TESTS_CONFIG__ = "ping_tests_config.json"
__BANDWIDTH_TEST_CONFIG__ = "bandwidth_tests_config.json"



def run_ping_tests(ping_results_dir):
    f = open(__PING_TESTS_CONFIG__, "r")
    ping_test_config = json.load(f)
    tests = ping_test_config.keys()
    for test in tests:
        print(f"executing PING test: {test}")
        test_config = ping_test_config[test]
        test_results_dir = f"{ping_results_dir}/{test}"
        make_dir(test_results_dir)
        ping_test.run(test_config, test_results_dir)
        print(f"DONE.")


def run_bandwidth_tests(bandwidth_results_dir):

    f = open(__BANDWIDTH_TEST_CONFIG__, "r")
    bandwidth_test_config = json.load(f)
    tests = bandwidth_test_config.keys()
    for test in tests:
        print(f"executing BANDWIDTH test: {test}")
        test_config = bandwidth_test_config[test]
        test_results_dir = f"{bandwidth_results_dir}/{test}"
        make_dir(test_results_dir)
        bandwidth_test.run(test_config, test_results_dir)
        print(f"DONE.")

def make_dir(results_dir):
    try:
        pathlib.Path(f"./{results_dir}").mkdir()
    except FileExistsError as e:
        # ignore that test_results already exists
        print(f"could not make directory {results_dir}. Exiting")


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