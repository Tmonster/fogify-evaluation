import json
import time
import os

from bandwidth_src.bandwidth_test import bandwidth_test
from utils.enums import image_roles
from utils.file_utils import file_exists


host_name = "host1"
try:
    host_name = os.environ['HOSTNAME']
except KeyError as e:
    pass
try:
    if host_name == "host1":
        host_name = os.environ['USER']
except KeyError as e:
    pass

BANDWIDTH_TEST_CONFIG = "bandwidth_test_config.json"

def get_bandwidth_test_config():
    try:
        test_file = open(BANDWIDTH_TEST_CONFIG, "r")
        bandwidth_tests = json.load(test_file)
        test_file.close()
    except FileNotFoundError as e:
        print(e)
        exit()
    return bandwidth_tests


def poll_for_bandwidth_test_config():
    while not file_exists(BANDWIDTH_TEST_CONFIG):
        time.sleep(2)


def execute_tests(bandwidth_tests):
    global host_name
    for test in bandwidth_tests['tests']:
        b_test = bandwidth_test(
            test['server'],
            test['client'],
            test['output_file_name'],
            test['port'],
            test['time'])
        
        if b_test.server == host_name and help_:
            b_test.run_server()
        elif b_test.client == host_name:
            b_test.run_client()

def run_bandwidth_test():
    poll_for_bandwidth_test_config()
    bandwidth_test_config = get_bandwidth_test_config()
    execute_tests(bandwidth_test_config)
    # give me time to get bandwidth tests out of files
    time.sleep(1000)

