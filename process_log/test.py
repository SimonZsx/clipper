import argparse
import re

log_file = "imagequery_withProxy_c1.log"

def main():
    avg_latency = 0.0
    num_requests = 0

    f = open(log_file, "r")
    for line in f:
        if "[INFO]" in line and "Time elapsed:" in line:
            num_requests += 1
            time = float(re.findall(r"[-+]?\d*\.\d+|\d+", line[line.index("elapsed: "):])[0])
            avg_latency += time
    
    # print("Throughput: {:.3f} request per second".format(num_requests * 1000 / avg_latency))
    # tp = num_requests * 1000 / avg_latency
    avg_latency /= num_requests
    print("Average latency: {:.3f} milliseconds".format(avg_latency))

if __name__ == '__main__':
    main()
