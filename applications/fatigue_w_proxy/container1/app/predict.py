# Import libraries
import os
import cv2
import numpy as np
import json
import time 
from datetime import datetime
# Read the model
model = cv2.dnn.readNetFromCaffe('/container/deploy.prototxt','/container/weights.caffemodel')

#imagestring is a serialized .jpg encoded image string

def image_string(image):
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


def predict(imagestring):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c1]\t", str(t1))
    
    image=string_image(imagestring)
#    image=cv2.imread('simple.jpg')  
    count = 0
    (h,w)=image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    detections = model.forward()

    # Identify each face
    for i in range(0, detections.shape[2]):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        confidence = detections[0, 0, i, 2]
        if (confidence > 0.5):
            count += 1
            frame = image[startY:endY, startX:endX]
            image_str=image_string(frame)
            
            t2 = datetime.utcnow()
            print("[INFO]\t", "[c1]\t", str(t2))
            print("[INFO]\t", "[c1]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
            return image_str
        
    t2 = datetime.utcnow()
    print("[INFO]\t", "[c1]\t", str(t2))
    print("[INFO]\t", "[c1]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    return None


