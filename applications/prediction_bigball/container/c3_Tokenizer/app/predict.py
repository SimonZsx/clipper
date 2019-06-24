import spacy,en_core_web_sm
import time

global nlp

nlp = en_core_web_sm.load()

def predict(text_data):

	start = time.time()

	doc = nlp(text_data)

	result = ""

	for sent in doc.sents:
		result += "|||" + str(sent) 

	end = time.time()
	
	print("c3 ELASPSED TIME", end - start)

	return result