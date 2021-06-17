import subprocess
import sys

def get_container_ids_and_hosts():
    output = subprocess.run(["sudo", "docker", "container", "ls", "--filter", "name=fogify_*"],
     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_decoded = output.stdout.decode('utf-8')
    container_info = output_decoded.rstrip().split('\n')[1:]
    container_ids = []
    container_names = []
    for container in container_info:
        split_vals = container.split(' ')
        container_ids += [split_vals[0]]
        container_names += [split_vals[-1]]
    return container_ids, container_names
    


def deploy_hosts_to_containers(container_ids, file_to_inject):
    for _id in container_ids:
        inject_path = _id + ":/code/"
        output = subprocess.run(["sudo", "docker", "cp", file_to_inject, inject_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        print(f"deployed to {_id}")


def main():
    file_to_inject = sys.argv[1]
    try:
        f = open(file_to_inject, 'r')
        f.close()
    except FileNotFoundError as e:
        print(f"ERROR: file {file_to_inject} doesn't exist")
        exit()
    container_ids, container_names = get_container_ids_and_hosts()
    deploy_hosts_to_containers(container_ids, file_to_inject)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: please include config file name to inject")
        exit()
    main()