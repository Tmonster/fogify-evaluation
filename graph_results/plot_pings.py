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
            times = list(map(lambda x: float(x.packet_time), results))
            b = x_plot_y_plot(times, max_rtts)
            all_max_rtts.append(b)

        return all_max_rtts

    def get_avg_rtts(self):
        all_avg_rtts = []
        for dest in self.destinations:
            results = self.results[dest]
            avg_rtts = list(map(lambda x: float(x.rtt_avg), results))
            times = list(map(lambda x: float(x.packet_time), results))
            b = x_plot_y_plot(times, avg_rtts)
            all_avg_rtts.append(b)
        return all_avg_rtts

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


class x_plot_y_plot:

    def __init__(self, x, y):
        self.x_plot = x
        self.y_plot = y


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
        self.packet_time = csv_line[12]


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


def get_files_from_directory(directory, extension):
    try:
        files = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)) and f.find(extension) >= 0:
                files.append(os.path.join(directory, f))
        return files
    except Exception as e:
        print(f"directory {args_.directory} doesn't have files or threw an error")
        exit()

def make_x_plot(size_cpu_measures):
    interval = 0.2
    last = 0
    ret = []
    for i in range(size_cpu_measures):
        ret.append(last)
        last += interval
    return ret

def main():
    parser = argparse.ArgumentParser(description='plot ping test results')
    parser.add_argument('directory', type=str, help="directory with bandwidth test results")
    args_ = parser.parse_args()

    directory = args_.directory + "results/"
    files = get_files_from_directory(directory, ".csv")
    all_file_results = []
    for file in files:
        if file.find(".txt") >= 0:
            # that's the test config file, doesn't have results
            continue
        file_results = get_data_from_file(file)
        all_file_results.append(file_results)

    file_results_0 = all_file_results[0]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('rtt_avg in ms')
    ax1.set_ylim(ymin=0,ymax=70)

    # max_rtts = file_results_0.get_max_rtt()
    # for max_rtt in max_rtts:
    #     plt.plot(max_rtt, linestyle = 'solid')

    for file in all_file_results:
        rtt_avgs = file.get_avg_rtts()
        for rtt_avg in rtt_avgs:
            np_arr_x = numpy.array(rtt_avg.x_plot)
            np_arr_y = numpy.array(rtt_avg.y_plot)
            ax1.plot(np_arr_x, np_arr_y, linestyle = 'dotted')


    ax2 = ax1.twinx()
    ax2.set_ylabel("cpu utilization (%)", color='tab:blue')
    ax2.set_ylim(ymin=0, ymax=100)
    cpu_utilization = get_files_from_directory(args_.directory, ".csv")[0]        

    with open(cpu_utilization) as cpu_data:
        reader = csv.reader(cpu_data, delimiter=",")
        # should only be one row
        for row in reader:
            row = row[:-1]
            x_axis = make_x_plot(len(row))
            cpu_data = list(map(lambda x: float(x), row))
            ax2.plot(x_axis, cpu_data, color='tab:blue', linestyle='dotted', label="cpu_utilization")
            ax2.tick_params(axis='y',labelcolor='tab:blue')

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()