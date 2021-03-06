import pingparsing
import time
import os

from utils.file_utils import file_exists


host_name = os.environ['HOSTNAME']

def pingparse_helper(ping_parser, ping_output, host):
    new_host_name = get_new_host_name(host)
    stdout_str = ping_output.stdout
    to_parse = stdout_str.replace(host, new_host_name)
    stats = ping_parser.parse(to_parse)
    return stats


def get_hosts():
    try:
        f = open("hosts.txt", "r")
        hosts = []
        for host in f:
            hosts += [host.rstrip()]
    except FileNotFoundError as e:
        # hosts file hasn't been initialized
        print("no host file")
        time.sleep(3)
        pass
    return hosts


# pingparser cannot parse ping output if the 
# host name has more "." or "_" than normally predicted 
def get_new_host_name(old_host):
    first_dot = old_host.find(".")
    if first_dot >= 1:
        new_host = old_host[:first_dot]
        new_host = new_host.replace("_", "-")
        return new_host
    return old_host


def poll_and_get_hosts():
    host_file_not_present = True
    while not file_exists("hosts.txt"):
        time.sleep(1)
    return get_hosts()


