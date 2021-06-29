import subprocess
import time
import threading

from utils.docker_utils import inject_file_to_all_containers
from utils.docker_utils import get_file_from_container
from utils.docker_utils import get_container_ids_and_hosts
from utils.topology_utils import deploy_topology
from utils.topology_utils import delete_topology
from utils.cpu_utils import record_cpu_utilization
from utils.file_utils import make_dir


def make_hosts_file(container_ids, hosts_file):
    with open(hosts_file, "w") as f:
        for _id in container_ids:
            f.write(_id + "\n")
    f.close() 

def extract_ping_results(container_ids, test_dir):
    final_location = f"{test_dir}/results"
    make_dir(final_location)
    for _id in container_ids:
        get_file_from_container(_id, "results/.", final_location)

def run(test_config, test_dir):
    yaml = test_config["yaml_file"]
    response = deploy_topology(yaml)
    if response.status_code != 200:
        print("could not deploy the topology, skipping test")
        print(f"response is {response}")
        return

    stop_thread = False
    thread_args = (
        test_dir,
        test_config["time"],
        lambda : stop_thread)
    cpu_metrics_thread = threading.Thread(target=record_cpu_utilization, 
        args=thread_args)
    try:
        container_ids, container_names = get_container_ids_and_hosts()
        hosts_file = test_dir + "/hosts.txt"
        make_hosts_file(container_ids, hosts_file)
        cpu_metrics_thread.start()
        inject_file_to_all_containers(container_ids, hosts_file)
        time.sleep(int(test_config['time']) + 3)
        stop_thread = True
        print("test done. stopping thread")
        cpu_metrics_thread.join()
        extract_ping_results(container_ids, test_dir)
    except Exception as e:
        pass

    response = delete_topology()
    if response.status_code != 200:
        print(f"could not delete topology")
