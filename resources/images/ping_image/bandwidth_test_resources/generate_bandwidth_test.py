import subprocess
import json

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


def generate_output_filename(server_name, client_name):
    filename = ""
    filename += server_name + "_"
    filename += client_name + ".json"
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


def main():
    test_length_in_seconds = 20
    test_port = 1025

    container_ids, container_names = get_container_ids_and_hosts()
    test_config = {}
    test_config['config'] = {}
    tests = []
    for from_container in range(len(container_ids)):
        for to_container in range(from_container, len(container_ids)):
            if from_container == to_container:
                continue
            from_container_id = container_ids[from_container]
            from_container_name = container_names[from_container]
            to_container_id = container_ids[to_container]
            to_container_name = container_names[to_container]
            tests.append(create_test(from_container_id, from_container_name,
                         to_container_id, to_container_name,
                         test_length_in_seconds,
                         test_port))
    test_config['tests'] = tests
    with open("bandwidth_test_config.json", "w") as f:
        f.write(json.dumps(test_config))

if __name__ == "__main__":
    main()