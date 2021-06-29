import requests
import subprocess
import time
import yaml

__FOGIFY_URL__ = "http://127.0.0.1"
__FOGIFY_PORT__ = "5000"


def get_topology_url():
    return __FOGIFY_URL__ + ":" + __FOGIFY_PORT__ + "/topology/"

def topology_deployed(yaml_path):
    topology_status = True
    try:
        f = open(yaml_path, "r")
        deployment = yaml.safe_load(f)
        topology = deployment['x-fogify']['topology']
        num_nodes = 0
        for node in topology:
            num_nodes += node['replicas']
        output = subprocess.run(["sudo", "docker", "stack", "ps", "fogify"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output_decoded = output.stdout.decode('utf-8')
        lines = output_decoded.split("\n")

        if len(lines) > 1:
            header = True
            state_index = -1
            for status in lines:
                if header or len(status):
                    header = False
                    continue
                else:
                    attrs = status.split()
                    if len(attrs) == 0:
                        # empty line (probably just a \n)
                        continue
                    if attrs[4] != "Running":
                        topology_status = False
                        break
        else:
            # if only 1 line is topology_deployedutput, nothing is found
            # in the stack, and the topology is most likely broken
            topology_status = False
    except Exception as e:
        print(f"error checking if topology is deployed. {e}")
    return topology_status


def topology_deleted():
    output = subprocess.run(["sudo", "docker", "stack", "ps", "fogify"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output_decoded = output.stderr.decode('utf-8')
    if output_decoded.find("nothing found in stack") >= 0:
        return True
    return False


def wait_for_topology_action():
    time.sleep(30)

def deploy_topology(yaml_path):
    files = {
        'file': open(yaml_path, 'rb')
    }
    url = get_topology_url()
    response = requests.post(url, files=files)
    if response.status_code == 500:
        import pdb
        pdb.set_trace()
        print(f"response content is {response.content}. Going to delete a topology")
    wait_for_topology_action()
    for i in range(5):
        if topology_deployed(yaml_path):
            return response
        else:
            wait_for_topology_action()
    print("Topology wasn't deployed. Going to delete and try again")
    r = delete_topology()
    return deploy_topology(yaml_path)

def prune_networks():
    subprocess.run(["sudo", "docker", "network", "prune", "--force"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

def delete_topology():
    url = get_topology_url()
    response = requests.delete(url)
    prune_networks()
    wait_for_topology_action()
    if not topology_deleted():
        return delete_topology()
    return response

# deploy_topology("yamls/bandwidth_tests/two_containers.yaml")
# delete_topology()