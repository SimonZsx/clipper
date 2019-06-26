import pandas as pd
import numpy as np
import time
import io
from concurrent import futures
import threading

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


def data(s):

    # CONTAINER 1: stock price retriever
    stock_data = pd.read_json(c1.predict(s + ":2018:1:1"))
    print("\nStart Predicting: ", s)
    print("\nStock price data Retrieval FINISHED")
    print("The retrieved data is in shape of ", stock_data.shape)
    #print("Here are the first 5 lines of retrieved data:")
    #print(stock_data.head())
    print("")

    returned_result_list = []
    p = Pool(5)
    returned_result_list.append(p.apply_async(run_lstm, args=(stock_data,))) 
    returned_result_list.append(p.apply_async(run_knn, args=(stock_data,)))
    returned_result_list.append(p.apply_async(run_random_forest, args=(stock_data,)))
    returned_result_list.append(p.apply_async(run_regression, args=(stock_data,)))
    returned_result_list.append(p.apply_async(run_arima, args=(stock_data,)))
    p.close()
    p.join()
    print("result list with len", len(returned_result_list), "is", returned_result_list)
    return returned_result_list

def twitter(s):
    # CONTAINER 2: Twitter Collector
    twitter_data = c2.predict(s + ":2018:1:1")
    print("Twitter data Retrieval FINISHED")
    #print("Here are the first 200 characters:")
    #print(twitter_data[:200])
    print("")

    # CONTAINER 3: Tokenizer
    tokenized_twitter_data = c3.predict(twitter_data)
    print("Tokenization FINISHED")
    print("Generated a list containing ", len(tokenized_twitter_data), " sentences")
    #print("The first 200 characters are :\n", tokenized_twitter_data[:200])
    print("")

    # CONTAINER 4: sentimental Analysis
    polarity_list = c4.predict(tokenized_twitter_data)
    print("Twitter data Sentiment Analysis FINISHED")
    print("Generated a list containing ", len(polarity_list), " results")
    #print("The first 200 characters are :\n", polarity_list[:200])
    print("")
    return polarity_list


def run():

    start = time.time()

    l98 = ['HAS', 'IRM', 'TEL', 'EL', 'ESS', 'COP', 'KEY', 'FE', 'CBS', 'IFF', 'NOV', 'IRM', 'FL', 'BBY', 'MS', 'FAST', 'CRM', 'NUE', 'MSCI', 'MMC', 'AIG', 'WELL', 'STT', 'CMA', 'RMD', 'FB', 'FB', 'IFF', 'WU', 'USB', 'NI', 'EA', 'TRIP', 'EBAY', 'AON', 'MS', 'TXN', 'USB', 'IRM', 'CE', 'BK', 'ROL', 'ANTM', 'NVDA', 'SEE', 'CNC', 'DXC', 'APA', 'APA', 'UPS', 'DOW', 'CAT', 'MET', 'HIG', 'LOW', 'CAT', 'VZ', 'MSCI', 'MA', 'BEN', 'RMD', 'BEN', 'HPE', 'PGR', 'CNC', 'PH', 'PGR', 'MAC', 'NOV', 'BEN', 'ICE', 'TAP', 'ABC', 'MMC', 'ESS', 'COST', 'HD', 'CVS', 'KIM', 'CAG', 'CNC', 'UPS', 'MO', 'BEN', 'FL', 'GS', 'EL', 'CMA', 'FE', 'IP', 'KIM', 'LOW', 'CF', 'NUE', 'FL', 'USB', 'CBS', 'CMA']

    l100 = ['HAS', 'IRM', 'TEL', 'EL', 'ESS', 'COP', 'KEY', 'FE', 'CBS', 'IFF', 'NOV', 'IRM', 'FL', 'BBY', 'MS', 'FAST', 'CRM', 'NUE', 'MSCI', 'MMC', 'AIG', 'WELL', 'STT', 'CMA', 'RMD', 'FB', 'FB', 'IFF', 'WU', 'USB', 'NI', 'EA', 'TRIP', 'HAL', 'EBAY', 'AON', 'MS', 'TXN', 'USB', 'IRM', 'CE', 'BK', 'ROL', 'ANTM', 'NVDA', 'SEE', 'CNC', 'DXC', 'APA', 'APA', 'UPS', 'DOW', 'CAT', 'MET', 'HIG', 'LOW', 'CAT', 'VZ', 'MSCI', 'MA', 'BEN', 'RMD', 'BEN', 'HPE', 'PGR', 'CNC', 'PH', 'PGR', 'MAC', 'NOV', 'BEN', 'ICE', 'TAP', 'ABC', 'MMC', 'ESS', 'COST', 'HD', 'CVS', 'KIM', 'CAG', 'CNC', 'UPS', 'MO', 'BEN', 'FL', 'GS', 'EL', 'CMA', 'FE', 'IP', 'KIM', 'LOW', 'CF', 'NUE', 'FL', 'USB', 'CBS', 'RF', 'CMA']


    # for s in l98:
    #     with futures.ThreadPoolExecutor(max_workers=2) as executor:
    #         inputt_list = l98
    #         future_to_excute = [executor.submit(data, s), executor.submit(twitter, s)]
    #         for future in futures.as_completed(future_to_excute):
    #             try:
    #                 data = future.result()
    #             except Exception as exc:
    #                 print('%s generated an exception: %s' % (str(inputt), exc))
    #             else:
    #                 print('Request %s received output:\n%s' % (str(inputt), data))
    start = time.time()
    for s in l98:
        p0 = Pool(2)
        p0.apply_async(data, args=(s,))
        p0.apply_async(twitter, args=(s,))
        p0.close()
        p0.join()
        print("Total time", time.time()-start)


if __name__ == "__main__":
    run()