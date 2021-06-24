import subprocess


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
    

def get_file_from_container(container, container_file, host_file):
    container_file = container + f":/code/{container_file}"
    output = subprocess.run(["sudo", "docker", "cp", container_file, host_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)


def inject_file_in_container(container, file_to_inject):
    inject_path = container + ":/code/"
    output = subprocess.run(["sudo", "docker", "cp", file_to_inject, inject_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    print(f"deployed to {container}")


def inject_file_to_all_containers(container_ids, file_to_inject):
    for _id in container_ids:
        inject_file_in_container(_id, file_to_inject)
        
