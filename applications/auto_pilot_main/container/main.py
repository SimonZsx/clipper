import sys
import time
import tensorflow as tf
from keras.models import load_model
sys.path.append("/container")

from multiprocessing import Pool

try:
    import c0_Entry_Point.app.predict as entry
    import c1_Image_Preprocessing.app.predict as preprocessing
    import c2_Obstacle_Detection.app.predict as obstacle_detection
    import c3_Route_Planning.app.predict as route_planning
    import c4_Algo1.app.predict as algo1
    import c5_Algo2.app.predict as algo2
    import c6_Conclusion.app.predict as conclusion
except Exception as exc:
    print('Generated an exception: %s' % (exc))

print("Modules successfully imported!")
		
def run():
    try:
        start = time.time()
        for i in range(100):
            c0_output = entry.predict(str(i) + "***7***7")
            print(c0_output)
            c1_output = preprocessing.predict(c0_output)
            print("Image Preprocessing Finished")
            c2_output = obstacle_detection.predict(c1_output)
            print("Obstacle Detection Finished")
            c3_output = route_planning.predict(c2_output)
            print("Route Planning Finished")
            returned_result_list = []
            returned_result_list.append(algo1.predict(c3_output))
            returned_result_list.append(algo2.predict(c3_output))
            print("Angle Prediction Finished")
            print(returned_result_list)
        print("Total Time:", time.time()-start)
    except Exception as exc:
        print('Generated an exception: %s' % (exc))

if __name__ == "__main__":
    run()
