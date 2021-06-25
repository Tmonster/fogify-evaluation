import matplotlib.pyplot as plt
import numpy
import argparse
import json
import os
import copy
import csv


HOST_NAME_TO_READABLE_NAME = {}

class all_tests_one_file:
    def __init__(self):
        self.destinations = []
        self.results = {}

    def add_dest(self, dest_name):
        if dest_name not in self.destinations:
            self.destinations.append(dest_name)
            self.results[dest_name] = []

    def add_result(self, ping_pair):
        if ping_pair.desintation in self.destinations:
            self.results[ping_pair.desintation].append(ping_pair)

    def get_max_rtt(self):
        all_max_rtts = []
        for dest in self.destinations:
            results = self.results[dest]
            max_rtts = list(map(lambda x: float(x.rtt_max), results))
            all_max_rtts.append(max_rtts)
        return all_max_rtts

    def get_avg_rtts(self):
        all_max_rtts = []
        for dest in self.destinations:
            results = self.results[dest]
            rtt_avgs = list(map(lambda x: float(x.rtt_avg), results))
            all_max_rtts.append(rtt_avgs)
        return all_max_rtts

    # normalize the tests so they all have the same lenght
    def normalize_tests(self):
        max_len = 0
        for dest in self.destinations:
            if len(self.results[dest]) > max_len:
                max_len = len(self.results[dest])
        for dest in self.destinations:
            if len(self.results[dest]) < max_len:
                # import pdb
                # pdb.set_trace()
                while len(self.results[dest]) < max_len:
                    first_result = self.results[dest][0]
                    self.results[dest].append(copy.deepcopy(first_result))



class ping_pair:

    def __init__(self, csv_line):
        self.source = HOST_NAME_TO_READABLE_NAME[csv_line[0]]
        self.desintation = HOST_NAME_TO_READABLE_NAME[csv_line[1]]
        self.packet_transmit = csv_line[2]
        self.packet_receive = csv_line[3]
        self.packet_loss_rate = csv_line[4]
        self.packet_loss_count = csv_line[5]
        self.rtt_min = csv_line[6] 
        self.rtt_avg = csv_line[7]
        self.rtt_max = csv_line[8]
        self.rtt_mdev = csv_line[9]
        self.packet_duplicate_rate = csv_line[10]
        self.packet_duplicate_count = csv_line[11]


def get_data_from_file(file):
    file_results = all_tests_one_file()
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                ping_result = parse_csv_data(row)
                file_results.add_dest(ping_result.desintation)
                file_results.add_result(ping_result)
    except FileNotFoundError as e:
        print(f"file {file} doesn't exist. Exiting")
        exit()
    return file_results

def parse_csv_data(csv_line):
    result = {}
    
    if csv_line[0] not in HOST_NAME_TO_READABLE_NAME:
        new_host_name = "host_" + str(len(HOST_NAME_TO_READABLE_NAME.keys()))
        HOST_NAME_TO_READABLE_NAME[csv_line[0]] = new_host_name

    if csv_line[1] not in HOST_NAME_TO_READABLE_NAME:
        new_host_name = "host_" + str(len(HOST_NAME_TO_READABLE_NAME.keys()))
        HOST_NAME_TO_READABLE_NAME[csv_line[1]] = new_host_name
    
    result = ping_pair(csv_line)
    return result


def get_files_from_directory(args_):
    try:
        directory = args_.directory
        files = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)):
                files.append(os.path.join(directory,f))
        return files
    except Exception as e:
        print(f"directory {args_.directory} doesn't have files or threw an error")
        exit()

def main():
    parser = argparse.ArgumentParser(description='plot ping test results')
    parser.add_argument('directory', type=str, help="directory with bandwidth test results")
    args_ = parser.parse_args()

    files = get_files_from_directory(args_)
    all_file_results = []
    for file in files:
        if file.find(".txt") >= 0:
            # that's the test config file, doesn't have results
            continue
        file_results = get_data_from_file(file)
        all_file_results.append(file_results)

    # for res in all_file_results:
    #     res.normalize_tests()


    file_results_0 = all_file_results[0]

    max_rtts = file_results_0.get_max_rtt()
    for max_rtt in max_rtts:
        plt.plot(max_rtt, linestyle = 'solid')

    # rtt_avgs = file_results_0.get_avg_rtts()
    # for rtt_avg in rtt_avgs:
    #     np_arr = numpy.array(rtt_avg)
    #     plt.plot(np_arr, linestyle = 'solid')

    plt.xlabel("time")
    plt.ylabel("rtt_avg in ms")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()