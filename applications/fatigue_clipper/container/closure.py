import container4.app.predict as c4
import container3.app.predict as c3
import container2.app.predict as c2
import container1.app.predict as c1
import random
import time
import multiprocessing
from multiprocessing import Pool
import json
import cv2
from __future__ import print_function
import rpc
import os
import sys
import numpy as np

IMPORT_ERROR_RETURN_CODE = 3

###########################################
sys.path.append("/container")
# c7 is discarded in this file, import error

print("Modules successfully loaded!")

# helping function


def image_string(image):
    image_encode = cv2.imencode('.jpg', image)[1]
    imagelist = image_encode.tolist()
    image_string = json.dumps(imagelist)
    return image_string


def string_image(imagestring):
    image_list = json.loads(imagestring)
    arr = np.array(image_list)
    arr = np.uint8(arr)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return image


def run_c1(imstr):
    result_fa = c1.predict(imstr)
    print("\nFace Extraction FINISHED")
    if result_fa == None:
        print("\n[INFO] No Person Detected In This Image!")
    return result_fa


def run_c2(imstr):
    result_drowsiness = c2.predict(imstr)
    print("\nFacial Point Detection FINISHED")
    return result_drowsiness


def run_c3(imstr):
    result_hu = c3.predict(imstr)
    print("\nHuman Segmentation FINISHED")
    if result_hu == None:
        print("\n[INFO] No Person Detected In This Image!")
    return result_hu


def run_c4(imstr):
    result_sleep = c4.predict(imstr)
    print("\n[INFO] Pose Analysis FINISHED")
    return result_sleep


def pipe1(imstr):
    result = run_c1(imstr)
    if result == None:
        return "No Person!"
    drowsiness = run_c2(result)
    if drowsiness:
        return "Drowsiness!"
    else:
        return "No Drowsiness!"


def pipe2(imstr):
    result = run_c3(imstr)
    if result == None:
        return "No Person!"
    sleep = run_c4(result)
    if sleep:
        return "Sleeping!"
    else:
        return "No Sleeping"

filelist = [f for f in os.listdir( "/container/part1") if f.endswith(".jpg")]

def run(input_index_list_format):
    print("input format:" + str(input_index_list_format))
    index = int(input_index_list_format[0])
    pipe1_result = []
    pipe2_result = []
    print("\nStart Detection: ")
    start = time.time()
    imag = cv2.imread("/container/part1/"+filelist[index])
    imgstr = image_string(imag)
    p = Pool(1)
    pipe1_result.append(p.apply_async(pipe1, args=(imgstr,)).get())
    pipe2_result.append(pipe2(imgstr))
    p.close()
    p.join()  # p.join()方法会等待所有子进程执行完毕
    end = time.time()
    print("\nResult of PIPE1:")
    print(pipe1_result)
    print("\nResult of PIPE2:")
    print(pipe2_result)
    print("\n Total time: "+str(end-start))

    return [str(pipe1_result) + str(pipe2_result), str(pipe1_result) + str(pipe2_result) ]

###########################################


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
