import json
import os
from numpy import array
from numpy import median

def temperature_readings():
	result = []
	with open(".." + os.sep + "outputs/smoke_detection_iot.json") as file:
		sensor_readings = json.loads(file.read())
		dataset_keys = sensor_readings.keys()
		for key in dataset_keys:
			if "Temperature" in key or "Fire" in key:
				result.append(sensor_readings[key])
		file.close()
		return result

def convert_data(temperature_data = None):
	if temperature_data is not None:
		for idx in range(len(temperature_data[0])):
			temperature_data[0][idx] = float(temperature_data[0][idx])
			temperature_data[1][idx] = False if int(temperature_data[1][idx]) == 0 else True
		return temperature_data

temperature_data = convert_data(temperature_readings())

"""
	The split_readings function is coded in the tutorial, so the exact same function can be found
	with its nice explanation on the corresponding URL: https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
"""
def split_readings(temperature_data = None, n_steps = 0):
	X, y = list(), list()
	for i in range(len(temperature_data[0])):
		end_ix = i + n_steps
		if end_ix > len(temperature_data[0]) - 1:
			break
		seq_x, seq_y = temperature_data[0][i:end_ix], median(temperature_data[0][i:end_ix])
		X.append(seq_x); y.append(seq_y)
	return array(X), array(y)

# We have our data and its length is about >60k.
# Taking n-steps for our splitting process large would be
# better in our case since we need to construct a normal
# from this data. I will be taking n-steps as 250, since 250^2 = 62500
# and it is nearly equal to the overall time steps we have.
n_steps = 250
temperature_inputs, temperature_outputs = split_readings(temperature_data, n_steps) # We have divided our sensor reading in 250 arrays, each nearly having 250 elements.
for i in range(len(temperature_inputs)):
	print(i)