import io
import sys
import tweepy
import time

def predict(request): # serve as api function
	try:
		start = time.time()
		info = request.split(":")
		stockcode = info[0]
		data_path = "/container/dataset/" + stockcode + ".txt"
		with open(data_path, 'r', encoding='utf-8') as file:
			result = file.read().replace('\n', '')
		end = time.time()
		print("ELASPSED TIME", end - start)
		return result
	except Exception as exc:
		print('Generated an exception: %s' % (exc))




