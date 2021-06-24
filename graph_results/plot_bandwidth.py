import matplotlib.pyplot as plt
import numpy
import argparse
import json
import os

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
    parser = argparse.ArgumentParser(description='plot bandwidth tests')
    parser.add_argument('directory', type=str, help="directory with bandwidth test results")
    args_ = parser.parse_args()

    files = get_files_from_directory(args_)
    for file in files:
        json_data = get_data_from_file(file)
        json_data['file_name'] = file
        parsed_result = parse_json_data(json_data)
        mbytes = parsed_result.get_in_Mbytes_per_second()
        plt.plot(mbytes, linestyle = 'solid', label=parsed_result.get_label())

    plt.xlabel("time")
    plt.ylabel("Megabytes/second")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    main()