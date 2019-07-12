import re
import os 
import argparse
import csv
from datetime import datetime

testingTime = datetime.now().strftime("%y-%m-%d-%H%M%S") 

def store_in_csv(row_data):
    with open("./data.csv", 'a') as of:
        of_csv = csv.DictWriter(of,fieldnames=row_data.keys())
        of_csv.writerow(row_data)

def process_bigball_log(log_file, num_containers, is_imagequery=False):
    timebook = []
    avg_timebook = []
    num_requests = 0

    for _ in range(num_containers):
        timebook.append([])

    f = open(log_file, "r")
    for line in f:
        if "[c" in line and "Time elapsed:" in line: # add "[c" to avoid matching "[main]"
            container_id_str = str(line[10]) # slice out the digit in "[cx]"
            if container_id_str.isdigit():
                container_id = int(container_id_str)
                if container_id < num_containers:
                    container_time = float(re.findall(r"[-+]?\d*\.\d+|\d+", line[11:])[0])
                    timebook[container_id].append(container_time)
                    if container_id == 0: 
                        num_requests += 1
                        
    if is_imagequery:
        timebook[2] = timebook[2][1:]

    for i, container_time_list in enumerate(timebook):
        avg_time_millisec = 1000 * sum(timebook[i]) / num_requests
        print("Container{} average latency: {:.3f} miliseconds.".format(i, 1000 * sum(timebook[i]) / num_requests))
        avg_timebook.append(avg_time_millisec)
        store_in_csv({"TimeStamp":testingTime,
                      "AppName":log_file.split('/')[-1].split('_')[0]+"Container{}".format(i),
                      "Mode":log_file.split('/')[-1].split('_')[1],
                      "Request":str(num_requests),
                      "Throughput":"N/A",
                      "Latency":str(avg_time_millisec)})

    

def process_w_proxy_log(log_file):
    avg_latency = 0.0
    num_requests = 0

    f = open(log_file, "r")
    for line in f:
        if "; time:" in line:
            num_requests += 1
            time = float(re.findall(r"[-+]?\d*\.\d+|\d+", line[line.index("time: "):])[0])
            avg_latency += time
    
    print("Throughput: {:.3f} request per second".format(num_requests * 1000 / avg_latency))
    tp = num_requests * 1000 / avg_latency
    avg_latency /= num_requests
    print("Average latency: {:.3f} miliseonds".format(avg_latency))
    store_in_csv({"TimeStamp":testingTime,
                  "AppName":log_file.split('/')[-1].split('_')[0]+"-Entire",
                  "Mode":log_file.split('/')[-1].split('_')[1],
                  "Request":str(num_requests),
                  "Throughput":str(tp),
                  "Latency":str(avg_latency)})



def process_wo_proxy_log(log_file):
    num_requests = 0

    f = open(log_file, "r")
    for line in f:
        if line[:5] == "Input":
            num_requests += 1
        elif str(line[0]).isdigit():
            try:
                total_time = float(line)
                print("Throughput: {:.3f} request per second".format(num_requests / total_time))
                print("Average latency: {:.3f} miliseconds".format(total_time * 1000 / num_requests))
                store_in_csv({"TimeStamp":testingTime,
                            "AppName":log_file.split('/')[-1].split('_')[0]+"Entire",
                            "Mode":log_file.split('/')[-1].split('_')[1],
                            "Request":str(num_requests),
                            "Throughput":"{:.3f}".format(num_requests / total_time),
                            "Latency":"{:.3f}".format(total_time * 1000 / num_requests)})
            except Exception as e:
                print(e)


def analyze_log(is_imagequery, system, log_file, num_containers):
    print(is_imagequery, system, log_file)
    print(os.getcwd())

    """ 
    system: clipper, bigball, withoutProxy, withProxy
    """

    if system == "bigball":
        process_bigball_log(log_file, num_containers, is_imagequery=True)
    elif system == "withoutProxy":
        process_wo_proxy_log(log_file)
    elif system == "withProxy":
        process_w_proxy_log(log_file)
    else:
        print("Cannot handle this mode!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log processor')

    parser.add_argument('--is_imagequery', type=bool, help="true/false")
    parser.add_argument('--system', type=str, help="withoutProxy/withProxy/bigball")
    parser.add_argument('--log_file', type=str, help="Path to log file")
    parser.add_argument('--num_containers', type=int, help="number of containers")
                       
    args = parser.parse_args()
    is_imagequery = args.is_imagequery
    system = args.system
    log_file = args.log_file
    num_containers = args.num_containers

    analyze_log(is_imagequery, system, log_file, num_containers)




