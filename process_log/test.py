from datetime import datetime

def predict():
    t1 = datetime.utcnow()
    print("[INFO]\t[c4]\t{}".format(str(t1)))
    t2 = datetime.utcnow()
    print("[INFO]\t[c4]\t{}".format(str(t2)))
    print("[INFO]\t[c4]\tTime elapsed: {:.10f} seconds.".format((t2-t1).total_seconds()) )

predict()