from __future__ import print_function
import rpc
import os
import sys
import numpy as np

IMPORT_ERROR_RETURN_CODE = 3

###########################################
import sys
import time
import tensorflow as tf
from keras.models import load_model
sys.path.append("/container")

from multiprocessing import Pool

try:
    import c0_Entry_Point.app.predict as entry
    import c1_Image_Preprocessing.app.predict as preprocessing
    import c2_Obstacle_Detection.app.predict as obstacle_detection
    import c3_Route_Planning.app.predict as route_planning
    import c4_Algo1.app.predict as algo1
    import c5_Algo2.app.predict as algo2
    import c6_Conclusion.app.predict as conclusion
except Exception as exc:
    print('Generated an exception: %s' % (exc))

print("Modules successfully imported!")
		
def run(input_index_list_format):
    print("input format:" + str(input_index_list_format))
    input_index = int(input_index_list_format[0])

    try:
        start = time.time()
        c0_output = entry.predict(str(input_index) + "***7***7")
        print(c0_output)
        c1_output = preprocessing.predict(c0_output)
        print("Image Preprocessing Finished")
        c2_output = obstacle_detection.predict(c1_output)
        print("Obstacle Detection Finished")
        c3_output = route_planning.predict(c2_output)
        print("Route Planning Finished")
        returned_result_list = []
        returned_result_list.append(algo1.predict(c3_output))
        returned_result_list.append(algo2.predict(c3_output))
        print("Angle Prediction Finished")
        print(returned_result_list)
        print("Total Time:", time.time()-start)
    except Exception as exc:
        print('Generated an exception: %s' % (exc))
    
    return ["output", "output"]
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
