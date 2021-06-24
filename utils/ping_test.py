import subprocess
import time

from utils.docker_utils import inject_file_to_all_containers
from utils.docker_utils import get_file_from_container
from utils.docker_utils import get_container_ids_and_hosts
from utils.topology_utils import deploy_topology
from utils.topology_utils import delete_topology


def make_hosts_file(container_ids, hosts_file):
    with open(hosts_file, "w") as f:
        for _id in container_ids:
            f.write(_id + "\n")
    f.close() 

def extract_ping_results(container_ids, test_dir):
    for _id in container_ids:
        final_location = f"{test_dir}/{_id}_ping_stats.csv"
        get_file_from_container(_id, "ping_stats.csv", final_location)

def run(test_config, test_dir):
    yaml = test_config["yaml_file"]
    response = deploy_topology(yaml)
    if response.status_code != 200:
        print("could not deploy the topology, skipping test")
        print(f"response is {response}")
        return

    try:
        container_ids, container_names = get_container_ids_and_hosts()
        hosts_file = test_dir + "/hosts.txt"
        make_hosts_file(container_ids, hosts_file)
        inject_file_to_all_containers(container_ids, hosts_file)
        time.sleep(int(test_config['time']) + 10)
        extract_ping_results(container_ids, test_dir)
    except Exception as e:
        pass

    response = delete_topology()
    if response.status_code != 200:
        print(f"could not delete topology")
