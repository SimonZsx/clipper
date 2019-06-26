# A dummpy container that just returns whatever is feeded into it

import time

def predict(info):
	start = time.time()
	end = time.time()
	print("ELASPSED TIME", (end-start)*1000)
	return info


