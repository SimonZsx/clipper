# originally named stockPriceRetriever.py
# this program loads stock price data and saves to file
import quandl
import datetime
import time

quandl.ApiConfig.api_key = "ZFtsDc5JcPvNXWwFVTSR"

def retrieveStockPrice(requestInfo):
	info = requestInfo.split(":")
	stockcode = info[0]
	starting_year = int(info[1])
	starting_month = int(info[2])
	starting_day = int(info[3])
	start = datetime.datetime(starting_year, starting_month, starting_day)
	end = datetime.date.today()
	stock_price_dataframe = quandl.get("WIKI/" + stockcode, start_date=start, end_date=end) # dateframe type
	return stock_price_dataframe.to_json()

def predict(requestInfo): # serves as an api function
	try:
		start = time.time()
		to_return = retrieveStockPrice(requestInfo)
		end = time.time()
		print("ELASPSED TIME", (end-start)*1000)
		return to_return
	except Exception as exc:
		print('Generated an exception: %s' % (exc))