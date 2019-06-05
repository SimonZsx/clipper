import io
import sys
import tweepy
import time
import os.path
from tweepy import *

def getData(keyword, limit):
	# consumer_key='PLzMzrEMZOTi256ghZoTnY3S7'
	# consumer_secret='Lql8oLrvhWnZQUhTMw7DImQJr5C0zlNpUker6sqIWNxaDsQPfI'
	# access_token='1114411093160419328-YHKv2l7lcnzNdp6eOJOIaAayL3vNrw'
	# access_token_secret='JxiiUA8aPth8cLr4PR35wEBW6HkJCwoiABFUpb98E75zh'


	consumer_key = "XZCWDs8jGm9ez5OfZ2GK2NKOo"
	consumer_secret = "lglShCFjK8vHElD31cg64r8uPhCN0BWjEoCwap5guFipDTYwcx"
	access_token =  "964053177262784512-FjkAyDCkXcxxrAGkTxRdePrDymQLqcn"
	access_token_secret = "6YtStVb4tGTNdmA7Re07cIJd9BrxmfWWyowAVxWk8qe6V"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
	#改变标准输出的默认编码, 否则print无法输出，因为有multiple byte character， 但是不影响代码运行

	tweets_string = ""
	for tweet in tweepy.Cursor(api.search, q = keyword, lang = "en" ).items(limit):
		tweets_string += tweet.text
		tweets_string += "\n"

	return tweets_string

def predict(request): # serve as api function
	start = time.time()
	info = request.split(":")
	stockcode = info[0]
	limit = 100
	to_return = getData(stockcode, limit)
	end = time.time()
	return to_return

l100 = ['HAS', 'IRM', 'TEL', 'EL', 'ESS', 'COP', 'KEY', 'FE', 'CBS', 'IFF', 'NOV', 'IRM', 'FL', 'BBY', 'MS', 'FAST', 'CRM', 'NUE', 'MSCI', 'MMC', 'AIG', 'WELL', 'STT', 'CMA', 'RMD', 'FB', 'FB', 'IFF', 'WU', 'USB', 'NI', 'EA', 'TRIP', 'EBAY', 'AON', 'MS', 'TXN', 'USB', 'IRM', 'CE', 'BK', 'ROL', 'ANTM', 'NVDA', 'SEE', 'CNC', 'DXC', 'APA', 'APA', 'UPS', 'DOW', 'CAT', 'MET', 'HIG', 'LOW', 'CAT', 'VZ', 'MSCI', 'MA', 'BEN', 'RMD', 'BEN', 'HPE', 'PGR', 'CNC', 'PH', 'PGR', 'MAC', 'NOV', 'BEN', 'ICE', 'TAP', 'ABC', 'MMC', 'ESS', 'COST', 'HD', 'CVS', 'KIM', 'CAG', 'CNC', 'UPS', 'MO', 'BEN', 'FL', 'GS', 'EL', 'CMA', 'FE', 'IP', 'KIM', 'LOW', 'CF', 'NUE', 'FL', 'USB', 'CBS', 'CMA']

x = []
for s in l100:
	if os.path.exists(s+".txt"):
		x.append(s)

print(x)


