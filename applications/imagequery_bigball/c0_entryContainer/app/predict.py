from datetime import datetime

def predict(input):
    t1 = datetime.utcnow()
    print("[INFO]\t[c0]\t{}".format(str(t1)))

    t2 = datetime.utcnow()
    print("[INFO]\t[c0]\t{}".format(str(t2)))
    print("[INFO]\t[c0]\tTime elapsed: {:.10f} seconds.".format((t2-t1).total_seconds()) )
    return input

