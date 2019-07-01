from __future__ import print_function
from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as python_deployer
import json
import requests
from datetime import datetime
import time
import numpy as np
import signal
import sys
import argparse




# Stop Clipper on Ctrl-C
def signal_handler(signal, frame):
    print("Stopping Clipper...")
    clipper_conn = ClipperConnection(DockerContainerManager())
    clipper_conn.stop_all()
    sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter the dag name')
    parser.add_argument('--dag', '-d', help='File Path of DAG file', dest='dag_graph')
    parser.add_argument('--name','-n', help='Name of the DAG',       dest='dag_name')

    signal.signal(signal.SIGINT, signal_handler)
    clipper_conn = ClipperConnection(DockerContainerManager())
    clipper_conn.start_clipper()


    f = open(parser.parse_args().dag_graph,"r")
    dag_description = f.read()
    f.close()
    
    clipper_conn.connect_host("202.45.128.174", "2375")
    clipper_conn.connect_host("202.45.128.175", "2375")

    clipper_conn.deploy_DAG(parser.parse_args().dag_name, "test", dag_description, runtime="nvidia")


    #time.sleep(2)

    # For batch inputs set this number > 1
    # batch_size = 1

    # try:
    #     while True:
    #         if batch_size > 1:
    #             predict(
    #                 clipper_conn.get_query_addr(),
    #                 [list(np.random.random(200)) for i in range(batch_size)],
    #                 batch=True)
    #         else:
    #             predict(clipper_conn.get_query_addr(), np.random.random(200))
    #         time.sleep(0.2)
    # except Exception as e:
    #     clipper_conn.stop_all()
