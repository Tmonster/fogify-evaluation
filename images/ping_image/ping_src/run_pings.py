import os
import sys
import time
import json
import pingparsing
import threading

from ping_src.ping_utils import poll_and_get_hosts
from ping_src.ping_utils import pingparse_helper
from utils.file_utils import make_dir

PACKET_TRASMIT_COUNT = 1

host_name = os.environ['HOSTNAME']


def save_statistics(stats):
    global host_name
    file_name = f"results/{host_name}_ping_{stats['destination']}.csv"
    file = open(file_name, 'a')
    line = ""
    line += str(host_name) + ","
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
    line += str(stats["packet_duplicate_count"]) + ","
    line += str(stats["time_since_start"]) + "\n"
    file.write(line)
    file.close()

def ping_thread(host):
    global host_name
    print(f"spawned thread")
    if host == host_name:
        # skip, no need to ping yourself
        return
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = PACKET_TRASMIT_COUNT
    time_start = time.perf_counter()
    while True:
        ping_output = transmitter.ping()
        stats = pingparse_helper(ping_parser, ping_output, host)
        time_done = time.perf_counter()
        statistics = stats.as_dict()
        statistics["destination"] = host
        statistics["time_since_start"] = time_done - time_start
        # TODO add some timestamts to the pings
        save_statistics(statistics)
        time.sleep(0.1)

def ping_hosts(hosts):
    if len(hosts) == 0:
        return
    threads = []
    make_dir("results")
    for host in hosts:
        # spawn pinging thread for each host
        # each host needs a lock though
        t = threading.Thread(target=ping_thread, args=(host,))
        t.start()
        threads.append(t)
    # threads will just run forever. 
    # after the host sleeps for the time of the test the 
    # ping_stats csv files are copied out of the containers,
    # and the test is done. The topology is eventually destroyed.


def run_ping_test():
    hosts = poll_and_get_hosts()
    ping_hosts(hosts)
    time.sleep(1000)

