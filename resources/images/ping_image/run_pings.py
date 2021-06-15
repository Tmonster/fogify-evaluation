import os
import time
import json
import pingparsing

PACKET_TRASMIT_COUNT = 5

HOSTS = []
host_check = 0

def poll_for_hosts():
    global HOSTS, host_check
    if len(HOSTS) == 0 or host_check % 5 == 0:
        get_hosts()
    host_check += 1

def get_hosts():
    print("getting hosts")
    try:
        f = open("hosts.txt", "r")
        global HOSTS
        HOSTS = []
        for host in f:
            HOSTS += [host.rstrip()]
    except FileNotFoundError as e:
        # hosts haven't been 
        print("no host file")
        pass

# pingparser cannot parse ping output if the 
# host name has more "." or "_" than normally predicted 
def get_new_host_name(old_host):
    first_dot = old_host.find(".")
    if first_dot >= 1:
        new_host = old_host[:first_dot]
        new_host = new_host.replace("_", "-")
        return new_host
    return old_host

def pingparse_helper(ping_parser, ping_output, host):
    new_host_name = get_new_host_name(host)
    stdout_str = ping_output.stdout
    to_parse = stdout_str.replace(host, new_host_name)
    stats = ping_parser.parse(to_parse)
    return stats

def ping_hosts():
    global HOSTS
    if len(HOSTS) == 0:
        return
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    for host in HOSTS:
        transmitter.destination = host
        transmitter.count = PACKET_TRASMIT_COUNT
        ping_output = transmitter.ping()
        stats = pingparse_helper(ping_parser, ping_output, host)
        statistics = stats.as_dict()
        statistics["destination"] = host
        # TODO add some timestamts to the pings
        save_statistics(statistics)
        


def save_statistics(stats):
    file = open('ping_stats.csv', 'a')
    line = ""
    line += str(stats["destination"]) + ","
    line += str(stats["packet_transmit"]) + ","
    line += str(stats["packet_receive"]) + ","
    line += str(stats["packet_loss_rate"]) + ","
    line += str(stats["packet_loss_count"]) + ","
    line += str(stats["rtt_min"]) + ","
    line += str(stats["rtt_avg"]) + ","
    line += str(stats["rtt_max"]) + ","
    line += str(stats["rtt_mdev"]) + ","
    line += str(stats["packet_duplicate_rate"]) + ","
    line += str(stats["packet_duplicate_count"]) + "\n"
    file.write(line)
    file.close()

while True:
    poll_for_hosts()
    ping_hosts()
    time.sleep(3)

