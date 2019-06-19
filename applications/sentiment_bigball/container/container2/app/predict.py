import spacy,en_core_web_sm
import time
nlp = en_core_web_sm.load()

def predict(text_data):
    start=time.time()
    doc = nlp(text_data)

    result = ""

    for sent in doc.sents:
        result = result + str(sent) + ","

    end=time.time()
    print("\nc2 time elapsed:"+str(end-start))
    return result
