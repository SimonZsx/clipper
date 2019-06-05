import numpy as np
import tensorflow as tf
import re

batchSize = 24
lstmUnits = 64
numClasses = 2
numDimensions=50
maxSeqLength=250
strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

wordVectors = np.load('/container/container3/app/wordVectors.npy')
wordsList = np.load('/container/container3/app/wordsList.npy')
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

sess=tf.Session()
saver=tf.train.Saver()
saver.restore(sess,tf.train.latest_checkpoint('/container/container3/app/models/'))

#paragraph is a string
def predict(paragraph):
    ids = np.zeros((1, maxSeqLength), dtype='int32')
    indexCounter = 0
    for word in paragraph:
        try:
            ids[0][indexCounter] = wordsList.index(word)
        except ValueError:
            ids[0][indexCounter] = 399999 #Vector for unkown words
        indexCounter = indexCounter + 1
        if indexCounter >= maxSeqLength:
            break

    inputdt=np.zeros([batchSize,maxSeqLength])
    lb=[]
    for i in range(batchSize):
        lb.append([1,0])
        inputdt[i]=ids[0]
    Prediction=sess.run(correctPred[0], {input_data: inputdt, labels: lb})
    print("\n[INFO] Prediction: ", Prediction)
    if Prediction:
        return True;
    else:
        return False;
