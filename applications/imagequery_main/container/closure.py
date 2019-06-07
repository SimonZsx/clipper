from __future__ import print_function
import rpc
import os
import sys
import numpy as np

IMPORT_ERROR_RETURN_CODE = 3

################### From main.py ####################################### 

from multiprocessing import Pool
from timeit import default_timer as timer


import c0_entryContainer.predict as entry_container
import c1_speechRecognition.predict as speech_recognizer
import c2_imageCaptionGenerator.predict as caption_generator
import c3_nlpMappingGenerator.predict as mapping_generator
import c4_questionAnswering.predict as question_answerer
print("---Modules successfully imported---")


def run_speech_recognition(input_index):
    speech_text = speech_recognizer.predict(input_index)
    return speech_text


def generate_image_caption(input_index):
    captions = caption_generator.predict(input_index)
    return captions
		
def run(input_index_list_format):

    print("input format:" + str(input_index_list_format))

    input_index = int(input_index_list_format[0])

    # CONTAINER 0
    input_index = entry_container.predict(input_index)

    # CONTAINER 1, 2: Multi Threading
    p = Pool(1) # use only one subprocess, run TF session in main process
    returned_result1 = p.apply_async(run_speech_recognition, args=(input_index,))
    # returned_result2 = p.apply_async(generate_image_caption, args=(input_index,))
    result2 = generate_image_caption(input_index)
    p.close()
    p.join() # p.join()方法会等待所有子进程执行完毕

    # CONTAINER 3
    result1 = returned_result1.get()[0]
    text = result1 + "|" + result2
    result3 = mapping_generator.predict(text)

    # Container 4
    question = "Verb"
    result4 = question_answerer.predict(result3)

    return [ str(result1) + str(result2) + str(result3) + str(result4) , str(result1) + str(result2) + str(result3) + str(result4)]

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
