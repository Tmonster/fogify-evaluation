import matplotlib.pyplot as plt
import numpy
import argparse
import json
import os
import csv

from legend_helper import MulticolorPatch 
from legend_helper import MulticolorPatchHandler


# This is the first important line:
from matplotlib import rcParams

_BYTE_ = 1000
_KILOBYTES_ = 8 * 1000
_MEGA_ = 1000 * 1000
_MEGABYTES_ = 8 * 1000 * 1000


class FullTest:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def get_in_Mbytes_per_second(self):
        ret = []
        for res in self.results:
            ret.append(res.get_Mbytes_per_second())
        return numpy.array(ret[:-1])

    def get_in_megabits_per_second(self):
        ret = []
        for res in self.results:
            ret.append(res.get_megabits_per_second())
        return numpy.array(ret[1:-1])

    def add_label(self, label):
        self.label = label

    def get_label(self):
        return self.label



class interval_result:

    def __init__(self, start, end, seconds, bytes_, bits_per_second):
        self.start = start
        self.end = end
        self.seconds = seconds
        self.bytes = bytes_
        self.bits_per_second = bits_per_second

    def get_Mbytes_per_second(self):
        return float(self.bits_per_second) / float(_MEGABYTES_)

    def get_megabits_per_second(self):
        return float(self.bits_per_second) / float(_MEGA_)



def parse_label_from_filename(file_name):
    extension_ind = file_name.rfind(".")
    start_of_file_name = file_name.rfind("/") + 1
    just_file_name = file_name[start_of_file_name:extension_ind]
    fogify_1 = just_file_name.find("fogify")
    fogify_2 = just_file_name.find("fogify", fogify_1 + 1)
    first_node = just_file_name[fogify_1 + 7: fogify_2 -1]
    second_node = just_file_name[fogify_2 + 7:]
    return f"{first_node} {second_node}"


def get_data_from_file(file):
    try:
        f = open(file, 'r')
        json_data = json.load(f)
        return json_data
    except FileNotFoundError as e:
        print(f"file {file} doesn't exist. Exiting")
        exit()

def parse_json_data(json_data):
    intervals = json_data['intervals']
    full_test = FullTest()
    for interval in intervals:
        new_result = interval_result(
            interval['sum']['start'],
            interval['sum']['end'],
            interval['sum']['seconds'],
            interval['sum']['bytes'],
            interval['sum']['bits_per_second'])
        full_test.add_result(new_result)
    label_name = parse_label_from_filename(json_data['file_name'])
    full_test.add_label(label_name)
    return full_test


def get_files_from_directory(args_, extension):
    try:
        directory = args_.directory
        files = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)) and \
                f.find(extension) >= 0:
                files.append(os.path.join(directory,f))
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

def get_experiment_name(args_):
    # in case the last char is a /, cut it off
    directory = args_.directory
    if directory[-1] == "/":
        directory = directory[:-1]
    exp_name_start = directory.rfind("/")
    exp_name = directory[exp_name_start+1:]
    exp_name = exp_name.replace("_", " ")
    return exp_name


def print_stats(all_y):
    # print standard deviation
    print(f"standard deviation: {numpy.std(all_y)}")
    print(f"variance: {numpy.var(all_y)}")
    # print 90th, 95th percentile
    print(f"90th percentile: {numpy.percentile(all_y, 0.9)}")
    print(f"95th percentile: {numpy.percentile(all_y, 0.95)}")
    # print number of 
    # print(f"number of pings recorded: {len(all_y)}")
    # print(f"number of pings > 45ms {len(all_y[all_y > 45])}")


def main():
    parser = argparse.ArgumentParser(description='plot bandwidth tests')
    parser.add_argument('directory', type=str, help="directory with bandwidth test results")
    args_ = parser.parse_args()

    experiment_name = get_experiment_name(args_)
    json_files = get_files_from_directory(args_, ".json")


    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"

    # https://matplotlib.org/2.2.5/gallery/api/two_scales.html
    fig, ax1 = plt.subplots()
    
    ax1.set_xlabel('Time (s)', fontsize=12)
    ax1.set_ylabel('MegaBits/second', fontsize=12)
    

    all_bytedata = numpy.array([])
    # import pdb
    # pdb.set_trace()
    for file in json_files:
        if file.find(".b_test.json") >= 0:
            # that's the test config file, doesn't have results
            continue
        json_data = get_data_from_file(file)
        json_data['file_name'] = file
        parsed_result = parse_json_data(json_data)
        mbytes = parsed_result.get_in_megabits_per_second()
        all_bytedata = numpy.append(all_bytedata, mbytes)
        if len(parsed_result.results) == 0:
            continue
        ax1.plot(mbytes, linestyle = 'solid', label=parsed_result.get_label())

    # ax1.legend(loc=4)
    ax1.xaxis.set_ticks(numpy.arange(0,70,5))
    ax1.yaxis.set_ticks(numpy.arange(0,250,50))
    ax2 = ax1.twinx()
    ax2.set_ylabel("CPU utilization (%)", color='tab:blue', fontsize=12)
    ax2.set_ylim(ymin=0, ymax=100)
    cpu_utilization = get_files_from_directory(args_, ".csv")[0]



    with open(cpu_utilization) as cpu_data:
        reader = csv.reader(cpu_data, delimiter=",")
        # should only be one row
        for row in reader:
            row = row[:-1]
            x_axis = make_x_plot(len(row))
            cpu_data = list(map(lambda x: float(x), row))
            ax2.plot(x_axis, cpu_data, color='tab:blue', linestyle='dotted', label="CPU utilization")
            ax2.tick_params(axis='y',labelcolor='tab:blue')
            
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()


    colors = []

    for h in lines_1:
        colors.append(h.get_color())
    
    color_patch = MulticolorPatch(colors, 'rect')
    handles = [color_patch, lines_2[0]]


    ax2.legend(handles, ["bandwidth connection", labels_2[0]], loc=0, 
        handler_map={MulticolorPatch: MulticolorPatchHandler()})


    print_stats(all_bytedata)
    # plt.title(label=experiment_name.title(), loc="center", fontsize=14)
    plt.subplots_adjust(top=0.98)
    plt.show()



if __name__ == "__main__":
    main()