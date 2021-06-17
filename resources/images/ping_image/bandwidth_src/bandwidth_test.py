import json
import os
import time
import subprocess

class bandwidth_test:

    def __init__(self, server, client, output_file_name, port, time):
        self.server = server
        self.client = client
        self.output_file_name = output_file_name
        self.port = str(port)
        self.time = time

    def run_server(self):
        port_number = self.port
        # runs iperf3 and outputs the results to a log file
        # after connection is made
        output = subprocess.run(
            ['iperf3','--json', '-s', '-1', 
             '-p', port_number, '--logfile', self.output_file_name])
        
    def run_client(self):
        port_number = self.port
        host = self.server
        # runs iperf3 test and outputs the results to a log file
        start = time.perf_counter()
        output = subprocess.run(
            ['iperf3', '--json', '-c', host, '-p', port_number, 
             '-t', str(self.time)])
        end = time.perf_counter()
        # need to run client until server is ready to listen
        # if the command immediately exits, the server wasn't yet listening
        # when this happens, wait and try again
        if end - start < self.time:
            # remove created file
            # print("re-run client, server is not yet listening")
            # os.remove(self.output_file_name)
            time.sleep(2)
            self.run_client()

        
