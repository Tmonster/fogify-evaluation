import subprocess
import psutil
import time

command = "top -a -l 1 | head -4 | tail -1"


def get_percent_then_number(input_str):
    percent_ind = input_str.find("%")
    prev_space = input_str[:percent_ind].rfind(" ")
    number = input_str[prev_space+1:percent_ind]
    return float(number), input_str[percent_ind+1:]


def record_cpu_usage_psutil():
    return psutil.cpu_percent()


def record_cpu_usage():
    out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = out.stdout.decode("utf-8")
    user_percent, rest = get_percent_then_number(output)
    sys_percent, rest = get_percent_then_number(rest)
    idle_percent, rest = get_percent_then_number(rest)
    print(f"user_percent = {user_percent}")
    print(f"sys_percent = {sys_percent}")
    print(f"idle_percent = {idle_percent}")
    print(f"user + sys + idle = {user_percent + sys_percent + idle_percent}")

def record_cpu_utilization(directory, test_time, stop):
    test_time = int(test_time) * 10
    while test_time > 0 and not stop():
        cpu_time = record_cpu_usage_psutil()
        f = open(directory + "/cpu_utilizations.csv", "a")
        f.write(str(cpu_time) + ",")
        f.close()
        time.sleep(0.2)
        test_time -= 1
    
