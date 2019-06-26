from datetime import datetime

def predict(input):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c0]\t", str(t1))

    t2 = datetime.utcnow()
    print("[INFO]\t", "[c0]\t", str(t2))
    print("[INFO]\t", "[c0]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    return input

