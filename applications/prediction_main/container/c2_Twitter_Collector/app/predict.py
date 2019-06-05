import io
import sys
import tweepy
import time

def predict(request): # serve as api function
	start = time.time()
	info = request.split(":")
	stockcode = info[0]
	data_path = "/container/c2_Twitter_Collector/dataset/" + stockcode + ".txt"
	with open(data_path, 'r') as file:
		result = file.read().replace('\n', '')
	end = time.time()
	print("ELASPSED TIME", end - start)
	return result




