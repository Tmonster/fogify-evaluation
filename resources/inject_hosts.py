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
    


def make_printf_command(container_names):
    command = ""
    command += "printf \""
    for name in container_names:
        command += name + "\n"
    command += "\" > hosts.txt"
    return command

def deploy_hosts_to_containers(container_ids, printf_command):
    for _id in container_ids:
        output = subprocess.run(["sudo", "docker", "exec", "-i", _id, "sh", "-c", printf_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        print(f"deployed to {_id}")


def main():
    container_ids, container_names = get_container_ids_and_hosts()
    printf_command = make_printf_command(container_names)
    deploy_hosts_to_containers(container_ids, printf_command)

if __name__ == "__main__":
    main()