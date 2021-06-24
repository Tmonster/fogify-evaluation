import os
import sys
import time
import json
import pingparsing

from ping_src.ping_utils import poll_and_get_hosts
from ping_src.ping_utils import pingparse_helper
from ping_src.ping_utils import save_statistics

PACKET_TRASMIT_COUNT = 5

host_name = os.environ['HOSTNAME']

def ping_hosts(hosts):
    if len(hosts) == 0:
        return
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    for host in hosts:
        if host == host_name:
            # skip, no need to ping yourself
            continue
        transmitter.destination = host
        transmitter.count = PACKET_TRASMIT_COUNT
        ping_output = transmitter.ping()
        stats = pingparse_helper(ping_parser, ping_output, host)
        statistics = stats.as_dict()
        statistics["destination"] = host
        # TODO add some timestamts to the pings
        save_statistics(statistics)


def run_ping_test():
    hosts = poll_and_get_hosts()
    while True:
        ping_hosts(hosts)
        time.sleep(3)

