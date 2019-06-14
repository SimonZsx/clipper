import spacy,en_core_web_sm

from datetime import datetime

nlp = en_core_web_sm.load()

def predict(text_data):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c2]\t", str(t1))
    doc = nlp(text_data)

    result = ""

    for sent in doc.sents:
        result = result + str(sent) + ","

    t2 = datetime.utcnow()
    print("[INFO]\t", "[c2]\t", str(t2))
    print("[INFO]\t", "[c2]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    
    return result
