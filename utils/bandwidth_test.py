import argparse
import subprocess
import json
import sys
import time

from utils.docker_utils import get_container_ids_and_hosts
from utils.docker_utils import inject_file_to_all_containers
from utils.docker_utils import get_file_from_container
from utils.topology_utils import deploy_topology
from utils.topology_utils import delete_topology

def find_nth(input_str, to_find, n):
    i = 0
    found_at = -1
    while i < n:
        found_at = input_str.find(to_find, found_at + 1)
        if found_at == -1:
            break
        i += 1
    return found_at

def generate_output_filename(server_name, client_name):
    filename = ""
    second_dot = find_nth(server_name, ".", 2)
    short_server_name = server_name[:second_dot]
    second_dot = find_nth(client_name, ".", 2)
    short_client_name = client_name[:second_dot]
    filename += short_server_name + "_"
    filename += short_client_name + ".json"
    return filename

def create_test(server,
                server_readable_name, 
                client,
                client_readable_name,
                time,
                port):
    test = {}
    test['server'] = server
    test['client'] = client
    test['time'] = time 
    test['port'] = port
    test['output_file_name'] = generate_output_filename(server_readable_name, client_readable_name)
    return test

def create_test_config_file(container_ids, container_names, file_name, configs):
    test_length_in_seconds = 60
    port_start_number = 50000

    test_config = {}
    test_config['config'] = configs
    test_length_in_seconds = configs['time']

    tests = []
    for from_container in range(len(container_ids)):
        for to_container in range(from_container, len(container_ids)):
            if from_container == to_container:
                continue
            from_container_id = container_ids[from_container]
            from_container_name = container_names[from_container]
            to_container_id = container_ids[to_container]
            to_container_name = container_names[to_container]
            new_test = create_test(
                         from_container_id, from_container_name,
                         to_container_id, to_container_name,
                         test_length_in_seconds,
                         port_start_number)
            tests.append(new_test)
            port_start_number += 1
    test_config['tests'] = tests
    with open(file_name, "w") as f:
        f.write(json.dumps(test_config, indent=4))
    return len(tests)



def extract_results_from_containers(file, results_dir):
    # make the bandwidthfiles
    f = open(file, "r")
    tests = json.load(f)
    tests = tests["tests"]
    f.close()
    for test in tests:
        file = test['output_file_name']
        server = test['server']
        get_file_from_container(server, file, f"{results_dir}/{file}")
        print(f"extracted from {server}")


def make_config(args_):
    test_config = {}
    test_config['stagger'] = True
    if args_.concurrent:
        del test_config['stagger']
        test_config['concurrent'] = True
    return test_config



def run(config, results_dir):
    yaml = config["yaml_file"]
    response = deploy_topology(yaml)

    if response.status_code != 200:
        print("could not deploy the topology, skipping test")
        print(f"response is {response}")
        # possible it's because there is already a deployed instance
        # can delete topology just in case
        r = delete_topology()
        return
    try:
        test_config = {}
        test_config['time'] = 60
        if 'stagger' in config and config['stagger'] == "true":
            test_config['stagger'] = True
        if 'concurrent' in config and config['concurrent'] == "true":
            test_config['concurrent'] = True
        if 'time' in config:
            try:
                test_config['time'] = int(config['time'])
            except Exception as e:
                print(f"error parsing run time for test. Defaulting to 60s")
                

        file = f"{results_dir}/bandwidth_config_file.b_test.json"
        container_ids, container_names = get_container_ids_and_hosts()
    
        num_tests = create_test_config_file(container_ids, 
                                            container_names,
                                            file,
                                            test_config)
        inject_file_to_all_containers(container_ids, file)
        if 'stagger' in test_config:
            # sleep the amount of the test and a buffer of 10 seconds
            time.sleep(num_tests * (60 + 10))
        elif 'concurrent' in test_config:
            time.sleep(60 + 30)
        extract_results_from_containers(file, results_dir)
    except Exception as e:
        print(f"Error here. Dont know what. e = {e}")
        pass

    response = delete_topology()
    if response.status_code != 200:
        print(f"could not delete topology")

# def main():
#     parser = argparse.ArgumentParser(description='manage bandwidth test ' \
#                                     'deployment and result extraction')
#     parser.add_argument('action', type=str, help="[extract|inject|create|create_inject] bandwidth test file ")
#     parser.add_argument('file', type=str, help="name of bandwidth test file to be extracted/injected/created/created_injected")
#     parser.add_argument('--stagger', help="stagger the bandwidth test so that each pair of containers test one by one")
#     parser.add_argument('--concurrent', help="have containers run the bandwidth tests concurrently")
#     parser.add_argument('--results-dir', help="results directory for extracting tests")
#     args_ = parser.parse_args()
#     file = args_.file
#     results_dir = "bandwidth_tests"
#     if args_.results_dir:
#         results_dir = args_.results_dir

#     test_config = make_config(args_)
    

#     container_ids, container_names = get_container_ids_and_hosts()
    
#     if args_.action == "extract":
#         extract_results_from_containers(file, results_dir)
#     elif args_.action == "inject":
#         try:
#             f = open(file, 'r')
#             f.close()
#         except FileNotFoundError as e:
#             print(f"ERROR: file {file} doesn't exist")
#             exit()
#         print(f"injecting {file}...")
#         inject_test_config_to_containers(container_ids, file)
#     elif args_.action == "create":
#         create_test_config_file(container_ids, container_names, file, test_config)
#     elif args_.action == "create_inject":
#         create_test_config_file(container_ids, container_names, file, test_config)
#         try:
#             f = open(file, 'r')
#             f.close()
#         except FileNotFoundError as e:
#             print(f"ERROR: file {file} doesn't exist")
#             exit()
#         print(f"injecting {file}...")
#         inject_test_config_to_containers(container_ids, file)
   