# USAGE
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import numpy as np
import dlib
import cv2
import os
import json
import time
from datetime import datetime
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

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

EYE_AR_THRESH = 0.28
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('/container/shape_predictor_68_face_landmarks.dat')

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

COUNT=0

# imagestring is a serialized .jpg encoded image string
def predict(imagestring):      
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c2]\t", str(t1))
    
    if imagestring is None:
        print("\n[INFO] Drowsiness Detection FINISHED!")
        
        t2 = datetime.utcnow()
        print("[INFO]\t", "[c2]\t", str(t2))
        print("[INFO]\t", "[c2]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
        
        return False
    frame=string_image(imagestring)
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)
    drowsiness=False
    for rect in rects:
        print("\n[INFO] Successfully detected faces!")
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0
        
        if ear<EYE_AR_THRESH:
            drowsiness=True
            t2 = datetime.utcnow()
            print("[INFO]\t", "[c2]\t", str(t2))
            print("[INFO]\t", "[c2]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
            COUNT=COUNT+1
           
        else:
            drowsiness=False
            t2 = datetime.utcnow()
            print("[INFO]\t", "[c2]\t", str(t2))
            print("[INFO]\t", "[c2]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
            COUNT=COUNT-1
    return "drowiness detection finished"
            
            

#         cv2.destroyAllWindows()




