from __future__ import print_function
import rpc
import os
import sys
import numpy as np

IMPORT_ERROR_RETURN_CODE = 3

################### From main.py ####################################### 

import numpy as np
import json
import sys
import os
sys.path.append("/container")
from multiprocessing import Pool
import multiprocessing
import time
# c7 is discarded in this file, import error

import container1.app.predict as c1
import container2.app.predict as c2
import container3.app.predict as c3
import container4.app.predict as c4
print("Modules successfully loaded!")

# helping function

def run_c1(index):
    result_trans = c1.predict(index)
    print("\nTranscribing Finished!")
    if result_trans==None:
        print("\n[INFO] Nothing Generated!")
    return result_trans

def run_c2(words):
    result_token = c2.predict(words)
    print("\nTokenization FINISHED")
    return result_token

def run_c3(words):
    result_senti = c3.predict(words)
    print("\nSentiment Analysis FINISHED")
    return result_senti

def run_c4(words):
    result_sub = c4.predict(words)
    print("\n[INFO] Subject Analysis FINISHED")
    return result_sub


def run(input_index_list_format):
    print("input format:" + str(input_index_list_format))
    input_index = int(input_index_list_format[0])
    
    print("\nStart Analysis: ")
    
    pipe1_result = []
    pipe2_result = []
    start=time.time()

    result1=run_c1(input_index)
    result2=run_c2(result1)
    result3=run_c3(result2)
    result4=run_c4(result2)
    pipe1_result.append(result3)
    pipe2_result.append(result4)
    end=time.time()
    print("\nResult of PIPE1:")
    print(pipe1_result)
    print("\nResult of PIPE2:")
    print(pipe2_result)
    print("\nTotal time: "+str(end-start))
    
    return ["output", "output"]

############################################################################


class PythonContainer(rpc.ModelContainerBase):
    def __init__(self, input_type):
        self.input_type = rpc.string_to_input_type(input_type)
        # modules_folder_path = "{dir}/modules/".format(dir=path)
        # sys.path.append(os.path.abspath(modules_folder_path))
        # predict_fname = "func.pkl"
        # predict_path = "{dir}/{predict_fname}".format(
        #   dir=path, predict_fname=predict_fname)
        self.predict_func = run

    def predict_ints(self, inputs):
        preds = self.predict_func(inputs)
        return [str(p) for p in preds]

    def predict_floats(self, inputs):
        preds = self.predict_func(inputs)
        return [str(p) for p in preds]

    def predict_doubles(self, inputs):
        preds = self.predict_func(inputs)
        return [str(p) for p in preds]

    def predict_bytes(self, inputs):
        preds = self.predict_func(inputs)
        return [str(p) for p in preds]

    def predict_strings(self, inputs):
        preds = self.predict_func(inputs)
        return [str(p) for p in preds]


if __name__ == "__main__":
    print("Starting Python Closure container")
    rpc_service = rpc.RPCService()
    try:
        model = PythonContainer(rpc_service.get_input_type())
        sys.stdout.flush()
        sys.stderr.flush()
    except ImportError:
        sys.exit(IMPORT_ERROR_RETURN_CODE)
    rpc_service.start(model)
