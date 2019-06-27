import base64
import os
import time
from concurrent import futures
import threading

import argparse
import sys
import datetime

from google.protobuf.timestamp_pb2 import Timestamp

import grpc

#from clipper_admin.grpcclient import grpc_client
from clipper_admin.rpc import (management_pb2, management_pb2_grpc, model_pb2,
                               model_pb2_grpc, prediction_pb2,
                               prediction_pb2_grpc)

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)



def consume(ip, port, inputt):

    inputt = str(inputt)

    channel = grpc.insecure_channel('%s:%s'%(ip, port))
    stub = prediction_pb2_grpc.ProxyServerStub(channel)
    
    a = datetime.datetime.now()
    response = stub.downstream(prediction_pb2.request(input_ = model_pb2.input(inputType = 'string', inputStream = inputt)))
    b = datetime.datetime.now()

    print ('latency', (b-a).microseconds/1000, "ms")

    return response.status


def main():

    ip = sys.argv[1]
    port = sys.argv[2]

    #1000

    # We can use a with statement to ensure threads are cleaned up promptly
    with futures.ThreadPoolExecutor(max_workers=32) as executor:
    # Start the load operations and mark each future with its URL
        inputt_list = [i for i in range(0,1000)]

        future_to_excute = {executor.submit(consume, ip, port, inputt): inputt for inputt in inputt_list}

        for future in futures.as_completed(future_to_excute):
            inputt = future_to_excute[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (str(inputt), exc))
            else:
                print('Request %s received output:\n%s' % (str(inputt), data))


    return 



if __name__ == '__main__':
    main()
