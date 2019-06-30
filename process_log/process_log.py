import re
import os 
import argparse

def process_bigball_log(is_imagequery=False):
    timebook = []
    num_requests = 0
    num_containers = 5 # should read from json

    for _ in range(num_containers):
        timebook.append([])

    f = open("./process_log/image_bigball.log", "r")
    for line in f:
        if "Time elapsed:" in line:
            container_id_str = str(line[10])
            if container_id_str.isdigit():
                container_id = int(container_id_str)
                if container_id < num_containers:
                    container_time = float(re.findall(r"[-+]?\d*\.\d+|\d+", line[11:])[0])
                    timebook[container_id].append(container_time)
                    if container_id == 0: 
                        num_requests+=1
                        
    # if is_imagequery:
    #     timebook[2] = timebook[2][1:]

    for i, container_time_list in enumerate(timebook):
        print("Container{} average latency: {:.3f} miliseconds.".format(i, 1000 * sum(timebook[i]) / num_requests))

    

def process_w_proxy_log():
    avg_latency = 0.0
    num_requests = 0

    f = open("./process_log/w_proxy.log", "r")
    for line in f:
        if "time:" in line:
            num_requests += 1
            time = float(re.findall(r"[-+]?\d*\.\d+|\d+", line[line.index("time: "):])[0])
            avg_latency += time
    
    print("Throughput: {:.3f} request per second".format(num_requests * 1000 / avg_latency))
    avg_latency /= num_requests
    print("Average latency: {:.3f} miliseonds".format(avg_latency))



def process_wo_proxy_log():
    num_requests = 0

    f = open("./process_log/wo_proxy.log", "r")
    for line in f:
        if line[:5] == "Input":
            num_requests += 1
        elif str(line[0]).isdigit():
            try:
                total_time = float(line)
                print("Throughput: {:.3f} request per second".format(num_requests / total_time))
                print("Average latency: {:.3f} miliseconds".format(total_time * 1000 / num_requests))
            except Exception as e:
                print(e)
     

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log processor')

    parser.add_argument('--is_imagequery', nargs=1, type=str, help="true/false")
    parser.add_argument('--system', nargs=1, type=str, help="w_proxy/wo_proxy/bigball")
    parser.add_argument('--log_file', nargs=1, type=str, help="Path to log file")
                       
    args = parser.parse_args()

    is_imagequery = args.is_imagequery[0]
    system = args.system[0]
    log_file = args.log_file[0]

    # print(is_imagequery, system)

    process_bigball_log(is_imagequery=True)
    process_w_proxy_log()
    process_wo_proxy_log()


