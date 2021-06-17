import pathlib
import subprocess
import datetime

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


def make_final_location():
    # make folder for date
    try:
        pathlib.Path(f"./test_results").mkdir()
    except FileExistsError as e:
        # ignore that test_results already exists
        pass
    today = datetime.date.today()
    folder_name = str(today)
    try:
        pathlib.Path(f"./test_results/{folder_name}").mkdir()
    except FileExistsError as e:
        pass
    now = datetime.datetime.now()
    current_time_str = now.strftime("%Hh-%Mm-%Ss")
    pathlib.Path(f"./test_results/{folder_name}/{current_time_str}").mkdir()
    return f"./test_results/{folder_name}/{current_time_str}/"


def get_file_from_host(host, final_location):
    host_file = host + ":/code/ping_stats.csv"
    final_file_name = final_location + host + "_test_pings.csv"
    output = subprocess.run(["sudo", "docker", "cp", host_file, final_file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

def main():
    container_ids, container_names = get_container_ids_and_hosts()
    file_location = make_final_location()
    for name in container_names:
        print(f"transferring from {name} to {file_location}")
        get_file_from_host(name, file_location)


if __name__ == "__main__":
    main()