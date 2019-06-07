import container4.app.predict as c4
import container3.app.predict as c3
import container2.app.predict as c2
import container1.app.predict as c1
from timeit import default_timer as timer
import multiprocessing
from multiprocessing import Pool
import numpy as np
import json
import sys
import os
import time
from multiprocessing import Process
sys.path.append("/container")
# c7 is discarded in this file, import error

print("Modules successfully loaded!")

# helping function


def run_c1(index):
    result_trans = c1.predict(index)
    print("\nTranscribing Finished!")
    if result_trans == None:
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
    

def run(index):
    print("\nStart Analysis: ")
    pipe1_result = []
    pipe2_result = []
    result1 = run_c1(index)
    result2 = run_c2(result1)
    p=Process(target=run_c4,args=(result2,))
    p.start()
    result3 = run_c3(result2)
    p.join() # p.join()方法会等待所有子进程执行完毕
    pipe1_result.append(result3)
    pipe2_result.append("result from r4")
    print("\nResult of PIPE1:")
    print(pipe1_result)
    print("\nResult of PIPE2:")
    print(pipe2_result)

if __name__ == "__main__":
    start=time.time()
    for i in range(100):
        run(i)
    end=time.time()
    print("\nTotal time: "+str(end-start))
