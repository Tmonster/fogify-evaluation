import matplotlib.pyplot as plt
import numpy
import argparse
import json
import os
import csv

_BYTE_ = 1000
_KILOBYTES_ = 8 * 1000
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

def main():
    parser = argparse.ArgumentParser(description='plot bandwidth tests')
    parser.add_argument('directory', type=str, help="directory with bandwidth test results")
    args_ = parser.parse_args()

    experiment_name = get_experiment_name(args_)
    json_files = get_files_from_directory(args_, ".json")


    # https://matplotlib.org/2.2.5/gallery/api/two_scales.html
    fig, ax1 = plt.subplots()
    
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('MegaBytes/second')
    
    # import pdb
    # pdb.set_trace()
    for file in json_files:
        if file.find(".b_test.json") >= 0:
            # that's the test config file, doesn't have results
            continue
        json_data = get_data_from_file(file)
        json_data['file_name'] = file
        parsed_result = parse_json_data(json_data)
        mbytes = parsed_result.get_in_Mbytes_per_second()
        if len(parsed_result.results) == 0:
            continue
        ax1.plot(mbytes, linestyle = 'solid', label=parsed_result.get_label())

    ax1.legend(loc=0)
    ax2 = ax1.twinx()
    ax2.set_ylabel("cpu utilization (%)", color='tab:blue')
    ax2.set_ylim(ymin=0, ymax=100)
    cpu_utilization = get_files_from_directory(args_, ".csv")[0]



    with open(cpu_utilization) as cpu_data:
        reader = csv.reader(cpu_data, delimiter=",")
        # should only be one row
        for row in reader:
            row = row[:-1]
            x_axis = make_x_plot(len(row))
            cpu_data = list(map(lambda x: float(x), row))
            ax2.plot(x_axis, cpu_data, color='tab:blue', linestyle='dotted', label="cpu_utilization")
            ax2.tick_params(axis='y',labelcolor='tab:blue')
            

    ax2.legend(loc=1)
    plt.title(label=experiment_name.title(), loc="center")
    plt.show()



if __name__ == "__main__":
    main()