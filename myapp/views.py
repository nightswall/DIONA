from django.shortcuts import render
from django.http import JsonResponse
from io import StringIO
import os
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import json

from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import TensorDataset, DataLoader
from django.views.decorators.csrf import csrf_exempt

class LSTMNet(nn.Module):
	def __init__(self, input_dim, hidden_dim, output_dim, n_layers, drop_prob=0.2):
		super(LSTMNet, self).__init__()
		self.hidden_dim = hidden_dim
		self.n_layers = n_layers

		self.lstm = nn.LSTM(input_dim, hidden_dim, n_layers, batch_first=True, dropout=drop_prob)
		self.fc = nn.Linear(hidden_dim, output_dim)
		self.relu = nn.ReLU()
		
	def forward(self, x, h):
		out, h = self.lstm(x, h)
		out = self.fc(self.relu(out[:,-1]))
		return out, h
	
	def init_hidden(self, batch_size):
		weight = next(self.parameters()).data
		hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device),
				  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device))
		return hidden
		
		
device =torch.device('cpu')
all_data=list()
model = LSTMNet(6, 256, 1, 2)
lookback = 90
inputs = np.zeros((1,lookback,6))
model.load_state_dict(torch.load('/home/mrt/Desktop/diona/myproject/myapp/lstm_model.pt',map_location=device))
s_data=pd.read_csv('/home/mrt/Desktop/diona/myproject/myapp/Occupancy_source.csv',parse_dates=[0])
s_data['hour'] = s_data.apply(lambda x: x['date'].hour,axis=1)
s_data['dayofweek'] = s_data.apply(lambda x: x['date'].dayofweek,axis=1)
s_data['month'] = s_data.apply(lambda x: x['date'].month,axis=1)
s_data['dayofyear'] = s_data.apply(lambda x: x['date'].dayofyear,axis=1)
s_data = s_data.sort_values('date').drop('date',axis=1)
s_data = s_data.drop('Light',axis=1)
s_data = s_data.drop('Humidity',axis=1)
s_data = s_data.drop('CO2',axis=1)
s_data = s_data.drop('HumidityRatio',axis=1)
sc = MinMaxScaler()
sc.fit(s_data.values)
label_sc = MinMaxScaler()
@csrf_exempt
def predict_temperature(request):
	def evaluate(model, test_x, label_scaler):
		model.eval()
		outputs = []
		#print(len(test_x))
		start_time = time.time()
		#print(test_x,test_y)
		inp = torch.from_numpy(np.array(test_x))
		
		#labs = torch.from_numpy(np.array(test_y))
		h = model.init_hidden(inp.shape[0])
		out, h = model(inp.to(device).float(), h)
		outputs.append(label_scaler.inverse_transform(out.cpu().detach().numpy()).reshape(-1))
		#print(outputs)
		#print(labs)
		#targets.append(label_scaler.inverse_transform(labs.numpy().reshape(-1,1)))
		#print("Evaluation Time: {}".format(str(time.time()-start_time)))
		#MSE = 0
		#for i in range(len(outputs)):
		#	MSE += np.square(np.subtract(targets[i],outputs[i])).mean()
		#print(outputs[i][0],targets[i][0])
		#print("MSE: {}%".format(MSE*100))
		return outputs
	#model.eval()
	temp_data = request.POST.get("data")
	#print(temp_data)
	csv_data = StringIO("{}".format(temp_data))
	#csv_data = "/home/mrt/Desktop/diona/myproject/myapp/Occupancy.csv"
	# The scaler objects will be stored in this dictionary so that our output test data from the model can be re-scaled during evaluation
	test_x = {}
	test_y = {}
	# Store json file in a Pandas DataFrame
	columns=['date','Temperature','Humidity','Light','CO2','HumidityRatio','Occupancy']
	df = pd.read_csv(csv_data,header=None,names=columns,parse_dates=[0])
	#df = df.sort_values('Humidity').drop('Humidity',axis=1)
	# Processing the time data into suitable input formats
	df['hour'] = df.apply(lambda x: x['date'].hour,axis=1)
	df['dayofweek'] = df.apply(lambda x: x['date'].dayofweek,axis=1)
	df['month'] = df.apply(lambda x: x['date'].month,axis=1)
	df['dayofyear'] = df.apply(lambda x: x['date'].dayofyear,axis=1)
	df = df.sort_values('date').drop('date',axis=1)
	df = df.drop('Light',axis=1)
	df = df.drop('Humidity',axis=1)
	df = df.drop('CO2',axis=1)
	df = df.drop('HumidityRatio',axis=1)
	# Scaling the input data
	#print(df.values)
	data = sc.transform(df.values)
	#print(data)
	# Obtaining the Scale for the labels(usage data) so that output can be re-scaled to actual value during evaluation
	label_sc.fit(df.iloc[:,0].values.reshape(-1,1))
	all_data.append(data)
	#print(all_data)
	count = len(all_data)-1
	#print(count)
	if(len(all_data)>lookback):
		inputs = np.array(all_data[count-lookback:count])
		prediction = evaluate(model,inputs,label_sc)
		json_prediction = str(prediction[0][0])
		#print(prediction[0][0].value())
		#print(json_prediction)
		#print((df['Temperature'].values)[0])
		if float(json_prediction)-float((df['Temperature'].values)[0]) > 2.5:
			anomaly="Yes"
		else:
			anomaly="No"
		return JsonResponse({"prediction":json_prediction,"actual":str(float((df['Temperature'].values)[0])),"is_anomaly":anomaly})
	else:
		return JsonResponse({"available_after":(90-len(all_data))})#(90-len(all_data))
# Create your views here.
