from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import quandl
import datetime
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.autograd import Variable

RANDOM_GENERATE = True
BATCH_SIZE = 16
TIME_STEP = 500
IN_CHANNEL = 60
STATE_DICT = "lstm_param.pkl"
CUDA=True

from os import path

if(path.exists(STATE_DICT)):
    FIRST_TRAIN = False
else:
    FIRST_TRAIN = True

if torch.cuda.is_available():
    if CUDA:
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
    else:
        print("WARNING: It looks like you have a CUDA device, but aren't using \
              			CUDA.  Run with --cuda for optimal eval speed.")
        torch.set_default_tensor_type('torch.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')
    CUDA = False


class LSTM_stock(nn.Module):
    def __init__(self, droprate=0.2, learningrate=0.05):
        super(LSTM_stock, self).__init__()

        self.droprate = droprate
        self.learningrate = learningrate

        self.loss_func = nn.MSELoss()

        self.net = nn.Sequential(
            nn.Dropout(self.droprate),
            nn.LSTM(
                input_size=IN_CHANNEL, 
                hidden_size=50,
                num_layers=4,
                batch_first=True
            )
        )
        self.out = nn.Linear(50,1)
        self.optimizer = Adam(self.parameters(),lr=self.learningrate)
    def forward(self, x_train): 
        out_width = x_train.size(1)
        #x_train.size() = BATCH_SIZE * TIME_STEP * IN_CHANNEL
        output, h_c_n = self.net(x_train)
        #output.size = BATCH_SIZE * TIME_STEP * IN_CHANNEL
        output = output.contiguous().view(-1,50)
        output = self.out(output)
        return output.view(-1,out_width,1), h_c_n

LSTMnet = LSTM_stock(0.2,0.05)
if(not FIRST_TRAIN):
    LSTMnet.load_state_dict(torch.load(STATE_DICT))
    LSTMnet.eval()
if CUDA:
    LSTMnet.cuda()

def single_train(stock_codes, net):
    net.train()
    all_x_sample = []
    all_y_sample = []
    if not RANDOM_GENERATE: 
	    for idx, code in enumerate(stock_codes):
                if(idx>=BATCH_SIZE):
                    break
                start = datetime.datetime(2016,1,1)
                end = datetime.date.today()
                stock_price_dataframe = quandl.get("WIKI/" + stock_code, start_date=start, end_date=end)
		# print(stock_price_dataframe.index)
                stock_price_dataframe.reset_index(inplace=True)
                stock_price_dataframe.reset_index(inplace=False)
		# print(stock_price_dataframe)
                stock_price_string = stock_price_dataframe.to_string(index=False)
                print(stock_price_string)
                df = pd.read_csv(pd.compat.StringIO(stock_price_string), sep=r'\s+');
                df = df.iloc[:, 0:11]
                print(df);
                training_set = stock_price_dataframe
                training_set_size = training_set.shape[0]

		# # Data cleaning
                training_set.isna().any()
		# Feature Scaling Normalization
                scaler = MinMaxScaler(feature_range=(0, 1))
                training_set_scaled = scaler.fit_transform(training_set)
                print("training_set_scaled.shape: " , training_set_scaled.shape)
		# # Creating a data structure with 60 timesteps and 1 output
                X_train = []
                y_train = []
                for i in range(60, training_set_size):
                    X_train.append(training_set_scaled[i-60 : i, 0])
                    y_train.append(training_set_scaled[i, 0])
                X_train, y_train = np.array(X_train), np.array(y_train)
		# X_train <= ndarray@500*60
		# Y_train <= ndarray@500*1
                all_x_sample.append(torch.FloatTensor(X_train))
                all_y_sample.append(torch.FloatTensor(y_train))
    else:
        for i in range(BATCH_SIZE):
            all_x_sample.append(torch.linspace(0,100,500*60).view(500,60))
            all_y_sample.append(torch.linspace(0,100,500).view(500,1))
    x_tensor = Variable(torch.stack(all_x_sample,dim=0))#BATCH first
    y_tensor = Variable(torch.stack(all_y_sample,dim=0)) #BATCH first

    if CUDA:
        x_tensor.cuda()
        y_tensor.cuda()
    print(x_tensor.size())
    print(y_tensor.size())
    y_hat, h_state = net(x_tensor)
    loss = net.loss_func(y_hat, y_tensor)
    net.optimizer.zero_grad()
    loss.backward()
    net.optimizer.step()
    print("Loss = ",loss)

if __name__ == "__main__":
    stock_codes = ["AAPL"]
    for i in range(50):
        single_train(stock_codes,LSTMnet)
    torch.save(LSTMnet.state_dict(),STATE_DICT)

    

        
        
