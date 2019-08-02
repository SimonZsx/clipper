# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://medium.com/explore-artificial-intelligence/introduction-to-named-entity-recognition-eda8c97c2db1

import spacy
import en_core_web_md
nlp = en_core_web_md.load()


def extract(s):
    doc = nlp(s)

    for element in doc.ents:
        print('Type: %s,\tValue: %s' % (element.label_, element))
