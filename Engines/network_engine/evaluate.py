import matplotlib.pyplot as plt
from model import Model
from data_loader import DataLoader
from sklearn import metrics
from warnings import simplefilter
import numpy as np

model = Model()
data_loader = DataLoader()

results = []
model_checkpoints = ["checkpoints/cp70.ckpt", "checkpoints/cp70_reduced.ckpt", "checkpoints/cp70_augmented.ckpt"]

def test30(checkpoint_path):
    global results
    testing_path = "drive/MyDrive/test30.csv"
    simplefilter(action = "ignore", category = FutureWarning)
    seed = 7

    x_test, y_test = data_loader.initialize_test_data(testing_path)
    detector = model.load_model(detector, checkpoint_path)

    y_pred = detector.predict(x_test)
    y_pred = np.argmax(y_pred, axis = 1)
    loss, acc = detector.evaluate(x_test, y_test, verbose=2)

    model_name = checkpoint_path.split("/")

    result = {"Dataset": "test30", "Model": model_name[1], "Accuracy": [metrics.accuracy_score(y_test, y_pred), 100 * acc], "F1 Score": metrics.f1_score(y_test, y_pred, average = "weighted")}
    results.append(result)

def test30_reduced(checkpoint_path):
    global results
    testing_path = "drive/MyDrive/test30_reduced.csv"
    simplefilter(action = "ignore", category = FutureWarning)
    seed = 7

    x_test, y_test = data_loader.initialize_test_data(testing_path)
    detector = model.load_model(detector, checkpoint_path)

    y_pred = detector.predict(x_test)
    y_pred = np.argmax(y_pred, axis = 1)
    loss, acc = detector.evaluate(x_test, y_test, verbose=2)

    model_name = checkpoint_path.split("/")

    result = {"Dataset": "test30_reduced", "Model": model_name[1], "Accuracy": [metrics.accuracy_score(y_test, y_pred), 100 * acc], "F1 Score": metrics.f1_score(y_test, y_pred, average = "weighted")}
    results.append(result)

def test30_augmented(checkpoint_path):
    global results
    testing_path = "drive/MyDrive/test30_augmented.csv"
    simplefilter(action = "ignore", category = FutureWarning)
    seed = 7

    x_test, y_test = data_loader.initialize_test_data(testing_path)
    detector = model.load_model(detector, checkpoint_path)

    y_pred = detector.predict(x_test)
    y_pred = np.argmax(y_pred, axis = 1)
    loss, acc = detector.evaluate(x_test, y_test, verbose=2)

    model_name = checkpoint_path.split("/")

    result = {"Dataset": "test30_augmented", "Model": model_name[1], "Accuracy": [metrics.accuracy_score(y_test, y_pred), 100 * acc], "F1 Score": metrics.f1_score(y_test, y_pred, average = "weighted")}
    results.append(result)

for predictor in model_checkpoints:
    print("Testing started with model: %s " % (predictor.split("/")[1]))
    test30(predictor)
    test30_reduced(predictor)
    test30_augmented(test30_augmented)

print(results)