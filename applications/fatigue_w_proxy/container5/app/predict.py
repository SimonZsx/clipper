import time
from datetime import datetime
def predict(received):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c5]\t", str(t1))
    
    print("\n[INFO] Received Output:%s"%(received))
    
    t2 = datetime.utcnow()
    print("[INFO]\t", "[c5]\t", str(t2))
    print("[INFO]\t", "[c5]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    
    return "\n[INFO] Fatigue Detection finished"
