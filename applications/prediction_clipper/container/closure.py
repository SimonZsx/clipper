from __future__ import print_function
import rpc
import os
import sys
import numpy as np

IMPORT_ERROR_RETURN_CODE = 3

################### From main.py ####################################### 

import pandas as pd
import numpy as np
import time
import io

import sys
sys.path.append("/container")

from multiprocessing import Pool 

# c7 is discarded in this file, import error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#改变标准输出的默认编码, 否则print无法输出，因为有multiple byte character， 但是不影响代码运行

import c1_Stock_Price_Retriever.app.predict as c1
import c2_Twitter_Collector.app.predict as c2 
import c3_Tokenizer.app.predict as c3
import c4_Sentiment_Analysis.app.predict as c4 
import c5_LSTM_Predictor.app.predict as c5
import c6_Mem.app.predict as c6 
import c7_ARIMA.app.predict as c7 
import c8_KNN.app.predict as c8 
import c9_RandomForest.app.predict as c9 
import c10_Regression.app.predict as c10 
import c11_Conclusion.app.predict as c11 
print("Modules successfully loaded!")

def run_lstm(stock_data):
    result_lstm = c5.predict(stock_data.to_json())
    print("Prediction using LSTM FINISHED")
    #print("Here is the result:")
    #print(result_lstm)
    print("")
    return result_lstm

def run_knn(stock_data):
    result_knn = c8.predict(stock_data.to_json())
    print("Prediction using KNN FINISHED")
    #print("Here is the result:")
    #print(result_knn)
    print("")
    return result_knn

def run_random_forest(stock_data):
    result_rf = c9.predict(stock_data.to_json())
    print("Prediction using Random Forest FINISHED")
    #print("Here is the result:")
    #print(result_rf)
    print("")
    return result_rf

def run_arima(stock_data):
    result_arima = c7.predict(stock_data.to_json())
    print("Prediction using ARIMA FINISHED")
    #print("Here is the result:")
    #print(result_rf)
    print("")
    return result_arima

def run_regression(stock_data):
    result_rg = c10.predict(stock_data.to_json())
    print("Prediction using Regrerssion FINISHED")
    #print("Here is the result:")
    #print(result_rg)
    print("")
    return result_rg

def run(input_index_list_format):
    print("input format:" + str(input_index_list_format))
    input_index = int(input_index_list_format[0])

    # start = time.time()

    # l100 = ['HAS', 'IRM', 'TEL', 'EL', 'ESS', 'COP', 'KEY', 'FE', 'CBS', 'IFF', 'NOV', 'IRM', 'FL', 'BBY', 'MS', 'FAST', 'CRM', 'NUE', 'MSCI', 'MMC', 'AIG', 'WELL', 'STT', 'CMA', 'RMD', 'FB', 'FB', 'IFF', 'WU', 'USB', 'NI', 'EA', 'TRIP', 'HAL', 'EBAY', 'AON', 'MS', 'TXN', 'USB', 'IRM', 'CE', 'BK', 'ROL', 'ANTM', 'NVDA', 'SEE', 'CNC', 'DXC', 'APA', 'APA', 'UPS', 'DOW', 'CAT', 'MET', 'HIG', 'LOW', 'CAT', 'VZ', 'MSCI', 'MA', 'BEN', 'RMD', 'BEN', 'HPE', 'PGR', 'CNC', 'PH', 'PGR', 'MAC', 'NOV', 'BEN', 'ICE', 'TAP', 'ABC', 'MMC', 'ESS', 'COST', 'HD', 'CVS', 'KIM', 'CAG', 'CNC', 'UPS', 'MO', 'BEN', 'FL', 'GS', 'EL', 'CMA', 'FE', 'IP', 'KIM', 'LOW', 'CF', 'NUE', 'FL', 'USB', 'CBS', 'RF', 'CMA']

    # for s in l100:
        
    #     # CONTAINER 1: stock price retriever
    #     stock_data = pd.read_json(c1.predict(s + ":2018:1:1"))
    #     print("\nStart Predicting: ", s)
    #     print("\nStock price data Retrieval FINISHED")
    #     print("The retrieved data is in shape of ", stock_data.shape)
    #     #print("Here are the first 5 lines of retrieved data:")
    #     #print(stock_data.head())
    #     print("")

    #     returned_result_list = []
    #     p = Pool(5)
    #     returned_result_list.append(p.apply_async(run_lstm, args=(stock_data,))) 
    #     returned_result_list.append(p.apply_async(run_knn, args=(stock_data,)))
    #     returned_result_list.append(p.apply_async(run_random_forest, args=(stock_data,)))
    #     returned_result_list.append(p.apply_async(run_regression, args=(stock_data,)))
    #     returned_result_list.append(p.apply_async(run_arima, args=(stock_data,)))
    #     p.close()
    #     p.join() # p.join()方法会等待所有子进程执行完毕

    #     # CONTAINER 2: Twitter Collector
    #     tweet_number = 1000
    #     twitter_data = c2.predict(s)
    #     print("Twitter data Retrieval FINISHED")
    #     print("Successfully retrieved", tweet_number, "number of tweets.")
    #     #print("Here are the first 200 characters:")
    #     #print(twitter_data[:200])
    #     print("")

    #     # CONTAINER 3: Tokenizer
    #     tokenized_twitter_data = c3.predict(twitter_data)
    #     print("Tokenization FINISHED")
    #     print("Generated a list containing ", len(tokenized_twitter_data), " sentences")
    #     #print("The first 200 characters are :\n", tokenized_twitter_data[:200])
    #     print("")

    #     # CONTAINER 4: sentimental Analysis
    #     polarity_list = c4.predict(tokenized_twitter_data)
    #     print("Twitter data Sentiment Analysis FINISHED")
    #     print("Generated a list containing ", len(polarity_list), " results")
    #     #print("The first 200 characters are :\n", polarity_list[:200])
    #     print("")

    #     # CONTAINER 11: Weighting Algorithm
    #     final_prediction = c11.predict(str(returned_result_list))
    #     print("\n\nEntire Process FINISHED")
    #     print("Total Time:", time.time()-start)
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
