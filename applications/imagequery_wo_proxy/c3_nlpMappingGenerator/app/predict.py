from datetime import datetime
from preprocess import preprocess
import spacy
nlp = spacy.load("en_core_web_sm")

def predict(input_str):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c3]\t", str(t1))

    c1_output, c2_output = str(input_str).split("|")
    reconstructed = str(c1_output) + str(c2_output)
    # print(reconstructed)
    preprocessed = preprocess(reconstructed)
    # print(preprocessed)

    doc = nlp(preprocessed)
    noun_list = [chunk.text for chunk in doc.noun_chunks]
    verb_list = [token.lemma_ for token in doc if token.pos_ == "VERB"]

    noun_str = ", ".join(noun_list)
    verb_str = ", ".join(verb_list)

    # print(noun_str + "-" + verb_str)

    t2 = datetime.utcnow()
    print("[INFO]\t", "[c3]\t", str(t2))
    print("[INFO]\t", "[c3]\t", "Time elapsed: ", (t2-t1).total_seconds(), " seconds.")

    return noun_str + "-" + verb_str

if __name__ == '__main__':
    predict("please call Stella ask her to bring. |a small propeller plane sitting on top of a field .")
    predict("please call Stella ask her to bring. |a small cat sitting on top of a house .")
