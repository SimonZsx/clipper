# timing
from timeit import default_timer as timer
b = timer()

# remove punctuation
import string

# stemming
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
stemmer = PorterStemmer()
stemmer.stem("")

# Lemmatization
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("") # Compiete initialization

e = timer()
print("Package loading takes " + str(e - b) + " seconds")


def timing(s, fn, *args):
    # Argument unpacking:
    # print(args)  # <class 'tuple'>
    # print(*args) # <class 'str'>, as we have only one argument

    b = timer()
    ret = fn(*args)
    e = timer()
    print("{} takes {} seconds".format(s, str(e-b)))
    return ret


def lower(s):
    return s.lower()


def remove_punc(s):
    s = s.translate(str.maketrans("", "", string.punctuation))
    return s


def remove_whitespace(s):
    return s.strip()


def stemming(s):
    tokens = word_tokenize(s)
    tokens = [stemmer.stem(word) for word in tokens]
    stemmed = " ".join(tokens)
    return stemmed


def lemmatizing(s):
    # https://stackoverflow.com/a/21243772/9057530
    tokens = word_tokenize(s)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    lemmatized = " ".join(tokens)
    return lemmatized


def preprocess(s, if_lemm=False):
    if if_lemm:
        return lemmatizing(stemming(remove_whitespace(remove_punc(lower(s)))))

    return stemming(remove_whitespace(remove_punc(lower(s))))


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
