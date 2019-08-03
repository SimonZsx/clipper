import numpy as np
import tensorflow as tf
import re
from datetime import datetime
batchSize = 24
lstmUnits = 64
numClasses = 2
numDimensions=50
maxSeqLength=250
strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
lb=[]
for i in range(batchSize):
    lb.append([1,0])





def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

wordVectors = np.load('/container/wordVectors.npy')
wordsList = np.load('/container/wordsList.npy')
print('\n[INFO]Loaded the word list!')
wordsList = wordsList.tolist() #Originally loaded as numpy array
wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8

tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [24, numClasses])
input_data = tf.placeholder(tf.int32, [24, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(wordVectors,input_data)

lstmCell = tf.nn.rnn_cell.LSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)
correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))

###### Specify GPU allocation to avoid CUDA_ERROR_OUT_OF_MEMORY #####
# Reference1: https://blog.csdn.net/wangkun1340378/article/details/72782593
# config = tf.ConfigProto(allow_soft_placement=True)

# 最多占gpu资源的30%
# gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)

# #开始不会给tensorflow全部gpu资源 而是按需增加
# config.gpu_options.allow_growth = True
# sess = tf.Session(config=config, graph=g)

# Reference2: https://github.com/tensorflow/tensorflow/issues/14475
# gpu_fraction = 0.1
# gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
# sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))


sess=tf.Session()
# sess = tf.Session(config=config)
saver=tf.train.Saver()
saver.restore(sess,tf.train.latest_checkpoint('/container/models/'))




#paragraph is a string
def predict(paragraph):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c3]\t", str(t1))
    
    ids = np.zeros((1, maxSeqLength), dtype='int32')
    indexCounter = 0
    paragraph=paragraph.split(" ")
    for word in paragraph:
        try:
            ids[0][indexCounter] = wordsList.index(word)
        except ValueError:
            ids[0][indexCounter] = 399999 #Vector for unkown words
        indexCounter = indexCounter + 1
        if indexCounter >= maxSeqLength:
            break

    inputdt=np.zeros([batchSize,maxSeqLength])
    for i in range(batchSize):
        inputdt[i]=ids[0]
    Prediction=sess.run(correctPred[0], {input_data: inputdt, labels: lb})
    print("\n[INFO] Prediction: ", Prediction)
    
    t2 = datetime.utcnow()
    print("[INFO]\t", "[c3]\t", str(t2))
    print("[INFO]\t", "[c3]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    if Prediction:
        return "True";
    else:
        return "False";
    
    
def batch_predict(input_list):
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[c3]\t", str(t1))
    
    output_list = []
    
    # use this loop to get **i** as each inputs
    i=0
    ids = np.zeros((batchSize, maxSeqLength), dtype='int32')
    for input in input_list: 
        print("model received input", input)
        indexCounter = 0
        input=input.split(" ")
        for word in input:
            try:
                ids[i][indexCounter] = wordsList.index(word)
            except ValueError:
                ids[i][indexCounter] = 399999 #Vector for unkown words
            indexCounter = indexCounter + 1
            if indexCounter >= maxSeqLength:
                break
        i = i + 1 
    Prediction=sess.run(correctPred, {input_data: ids, labels: lb})
    for res in Prediction:
        output_list.append(str(res))
    print("\nPrediction is: "+str(Prediction))
    t2 = datetime.utcnow()
    print("[INFO]\t", "[c3]\t", str(t2))
    print("[INFO]\t", "[c3]\tTime elapsed: ", (t2-t1).total_seconds(), " seconds." )
    
    return output_list

