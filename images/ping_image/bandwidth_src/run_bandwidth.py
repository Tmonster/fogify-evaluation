import json
import time
import logging
import threading
import os
import glob

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



BANDWIDTH_TEST_IDENTIFIER = ".b_test.json"


logger = logging.getLogger(__name__)

fh = logging.FileHandler('test_output.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


ALREADY_TESTED_FILES = set()

def get_bandwidth_test_config():
    try:
        test_files = glob.glob("*.b_test.json")
        file_name = test_files[0]
        ALREADY_TESTED_FILES.add('file_name')
        test_file = open(file_name, "r")
        bandwidth_tests = json.load(test_file)
        test_file.close()
    except FileNotFoundError as e:
        print(e)
        exit()
    return bandwidth_tests


def poll_for_bandwidth_test_config():
    while True:
        test_files = glob.glob("*.b_test.json")
        if len(test_files) > 0:
            break

def execute_tests(bandwidth_tests):
    global host_name
    config = bandwidth_tests['config']
    threads = list()
    try:
        for test in bandwidth_tests['tests']:
            b_test = bandwidth_test(
                test['server'],
                test['client'],
                test['output_file_name'],
                test['port'],
                test['time'])

            if b_test.server == host_name:
                if 'concurrent' in config and config['concurrent']:
                    # run as thread
                    logger.warning(f"starting server thread for {b_test.server}. client is {b_test.client}")
                    x = threading.Thread(target=b_test.run_server, args=())
                    x.start()
                    threads.append(x)
                else:
                    logger.warning(f"running server test for {b_test.server}. client is {b_test.client}")
                    b_test.run_server()
                    logger.warning(f"done with server test for {b_test.server}. output file is {b_test.output_file_name}")
            elif b_test.client == host_name:
                if 'concurrent' in config and config['concurrent']:
                    # run as thread
                    logger.warning(f"started client thread for {b_test.client}. server is {b_test.server}")
                    y = threading.Thread(target=b_test.run_client, args=())
                    y.start()
                    threads.append(y)
                else:
                    logger.warning(f"running client for {b_test.client}. server is {b_test.server}")
                    b_test.run_client()
                    logger.warning(f"done with client test for {b_test.client}. server was {b_test.server}")
            elif 'stagger' in config and config['stagger']:
                logger.warning(f"sleeping for test")
                time.sleep(b_test.time)
    
    except Exception as e:
        logger.warning(f"Error running tests. let's log e. {e}")

    logger.warning("Done with all bandwidth tests")
    for th in threads:
        th.join()
    logger.warning("all bandwidth tests are joined")



def run_bandwidth_test():
    poll_for_bandwidth_test_config()
    bandwidth_test_config = get_bandwidth_test_config()
    execute_tests(bandwidth_test_config)
    # give me time to get bandwidth tests out of files
    time.sleep(1000)

