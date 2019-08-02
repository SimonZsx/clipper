# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://medium.com/explore-artificial-intelligence/introduction-to-named-entity-recognition-eda8c97c2db1

import spacy
import en_core_web_md
from timeit import default_timer as timer

load_start = timer()
nlp = en_core_web_md.load()
load_end = timer()
print("---Loading takes " + str(load_end - load_start) + "---")


def extract(s):
    doc = nlp(s)

    # Type: NORP,     Value: European
    # Type: ORG,      Value: Google
    # Type: MONEY,    Value: $5.1 billion
    # Type: DATE,     Value: Wednesday
    # Type: CARDINAL, Value: 50
    # Type: NORP,     Value: American
    # Type: DATE,     Value: the 2015 season
    # Type: ORG,      Value: The American Football Conference (AFC
    # Type: PERSON,   Value: Broncos
    # Type: ORDINAL,  Value: third
    # Type: EVENT,    Value: Super Bowl
    # Type: FAC,      Value: Levi's Stadium
    for element in doc.ents:
        print("Type: %s,\tValue: %s" % (element.label_, element))

    result = [(element.label_, element) for element in doc.ents]
    return result


def predict(input_str):
    predict_start = timer()
    result = extract(input_str)
    predict_end = timer()
    print("---Prediction takes " + str(predict_end - predict_start) + "---")
    return result


def main():
    text = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing " \
    + "its power in the mobile phone market and ordered the company to alter its practices'

    predict(text)

    text = (
        "Super Bowl 50 was an American football game to determine the champion of the National "
        + "Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion"
        + "Denver Broncos defeated the National Football Conference (NFC) champion Carolina "
        + "Panthers 24-10 to earn their third Super Bowl title. The game was played on February "
        + "7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California."
    )

    predict(text)

if __name__ == "__main__":
    main()
