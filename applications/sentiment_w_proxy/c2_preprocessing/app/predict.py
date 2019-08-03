from preprocess import preprocess, timing
from datetime import datetime


def predict(input_str):
    t1 = datetime.utcnow()
    print("[INFO]\t[c3]\t{}".format(str(t1)))

    result = preprocess(input_str)

    t2 = datetime.utcnow()
    print("[INFO]\t[c3]\t{}".format(str(t2)))
    print(
        "[INFO]\t[c3]\tTime elapsed: {:.10f} seconds.".format((t2 - t1).total_seconds())
    )

    return result


def main():
    text = (
        "Super Bowl 50 was an American football game to determine the champion of the National "
        + "Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion"
        + "Denver Broncos defeated the National Football Conference (NFC) champion Carolina "
        + "Panthers 24-10 to earn their third Super Bowl title. The game was played on February "
        + "7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California."
    )

    print(text)
    print()
    print(timing("Preprocessing", preprocess, text, True))

    text = (
        "Super Bowl 50 was an American football game to determine the champion of the National "
        + "Denver Broncos defeated the National Football Conference (NFC) champion Carolina "
        + "7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California."
    )
    print(timing("Preprocessing", preprocess, text, True))


if __name__ == "__main__":
    main()
