from textblob import TextBlob

def predict(input_str):
    tb_str = TextBlob(input_str)
    return (tb_str.sentiment, tb_str.subjectivity)


def main():
    s = "A wiki is run using wiki software, otherwise known as a wiki engine. A wiki engine is a type of content management system, but it differs from most other such systems, including blog software, in that the content is created without any defined owner or leader, and wikis have little inherent structure, allowing structure to emerge according to the needs of the users."
    print(predict(s))

    s = "Wikipedia is not a single wiki but rather a collection of hundreds of wikis, with each one pertaining to a specific language. In addition to Wikipedia, there are tens of thousands of other wikis in use, both public and private, including wikis functioning as knowledge management resources, notetaking tools, community websites, and intranets."
    print(predict(s))


if __name__ == "__main__":
    main()