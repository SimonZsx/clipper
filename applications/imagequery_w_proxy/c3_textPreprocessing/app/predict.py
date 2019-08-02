# from datetime import datetime
# from preprocess import preprocess
# import spacy
# nlp = spacy.load("en_core_web_sm")

# def predict(input_str):
#     t1 = datetime.utcnow()
#     print("[INFO]\t[c3]\t{}".format(str(t1)))

#     c1_output, c2_output = str(input_str).split("|")
#     reconstructed = str(c1_output) + str(c2_output)
#     preprocessed = preprocess(reconstructed)
#     # print(preprocessed)

#     doc = nlp(preprocessed)
#     noun_list = [chunk.text for chunk in doc.noun_chunks]
#     verb_list = [token.lemma_ for token in doc if token.pos_ == "VERB"]

#     noun_str = ", ".join(noun_list)
#     verb_str = ", ".join(verb_list)

#     # print(noun_str + "-" + verb_str)

#     t2 = datetime.utcnow()
#     print("[INFO]\t[c3]\t{}".format(str(t2)))
#     print("[INFO]\t[c3]\tTime elapsed: {:.10f} seconds.".format((t2-t1).total_seconds()) )

#     return noun_str + "-" + verb_str

# if __name__ == '__main__':
#     predict("please call Stella ask her to bring. |a small propeller plane sitting on top of a field.")
#     predict("please call Stella ask her to bring. |a small cat sitting on top of a house.")

# print("c3 started!")

from preprocess import preprocess, timing

def main():
    text = "Super Bowl 50 was an American football game to determine the champion of the National " \
        + "Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion" \
        + "Denver Broncos defeated the National Football Conference (NFC) champion Carolina "\
        + "Panthers 24-10 to earn their third Super Bowl title. The game was played on February " \
        + "7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California."

    print(text)
    print()
    print(timing("Preprocessing", preprocess, text, True))


if __name__ == "__main__":
    main()
