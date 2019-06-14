# Import libraries
import os
import cv2
import json
import random
import numpy
import time
from datetime import datetime
def image_string(image):
    if image is None:
        return None
    image_encode=cv2.imencode('.jpg',image)[1]
    imagelist=image_encode.tolist()
    image_string=json.dumps(imagelist)
    return image_string

def string_image(imagestring):
    image_list=json.loads(imagestring)
    arr=np.array(image_list)
    arr=np.uint8(arr)
    image=cv2.imdecode(arr,cv2.IMREAD_COLOR)
    return image

filelist=[f for f in os.listdir("/container/part1") if f.endswith(".jpg")]
def predict(index):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c0]\t", str(t1))
    
    index=int(index)
    random_image=cv2.imread("/container/part1/"+str(filelist[index]))
    print("\n[INFO] Output a Input Request!")
    inputstring=image_string(random_image)
    inputstring=str(inputstring)
    
    t2 = datetime.utcnow()
    print("[INFO]\t", "[c0]\t", str(t2))
    print("[INFO]\t", "[c0]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )

    return inputstring





