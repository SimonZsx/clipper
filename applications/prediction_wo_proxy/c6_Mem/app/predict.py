
import time

def predict(received):
	start = time.time()
	end = time.time()
	print("ELASPSED TIME", (end-start)*1000)
	print("Received Output:%s"%(received))
	return received