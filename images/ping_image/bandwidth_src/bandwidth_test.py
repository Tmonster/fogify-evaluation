import json
import os
import time
import subprocess
import logging
import pingparsing

class bandwidth_test:

    def __init__(self, server, client, output_file_name, port, time):
        self.server = server
        self.client = client
        self.output_file_name = output_file_name
        self.port = str(port)
        self.time = time

    # check to make sure client and server are on the same network
    # if not, output to file and empty bandwidth json result that
    # has no intervals
    def in_network(self, dest):
        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = dest
        transmitter.count = 1
        output = transmitter.ping()
        if output.stderr.find("Name does not resolve") >= 0:
            return False
        return True

    def write_empty_iperf_test(self):
        empty_iperf_result = {
          "start":  {
          },
          "intervals":  [],
          "end":  {}
        }
        with open(self.output_file_name, "w") as f:
            f.write(json.dumps(empty_iperf_result))

    def remove_file(file):
        try:
            os.remove(file)
        except FileNotFoundError as e:
            pass

    def run_server(self):
        if not self.in_network(self.client):
            self.write_empty_iperf_test()
            time.sleep(str(self.time))
            return
        port_number = self.port
        # runs iperf3 and outputs the results to a log file
        # after connection is made
        start = time.perf_counter()
        output = subprocess.run(
            ['iperf3','--json', '-s', '-1', 
             '-p', port_number, '--logfile', self.output_file_name])
        end = time.perf_counter()
        if end - start < self.time - 1:
            bandwidth_test.remove_file(self.output_file_name)
            self.run_server()


    def run_client(self):
        if not self.in_network(self.server):
            time.sleep(str(self.time))
            return
        port_number = self.port
        host = self.server
        # runs iperf3 test
        start = time.perf_counter()
        output = subprocess.run(
            ['iperf3', '-c', host, '-p', port_number, 
             '-t', str(self.time)])
        end = time.perf_counter()
        # need to run client until server is ready to listen
        # if the command immediately exits, the server wasn't yet listening
        # when this happens, wait and try again
        if end - start < self.time - 1:
            # remove created file
            # print("re-run client, server is not yet listening")
            bandwidth_test.remove_file(self.output_file_name)
            self.run_client()
        
