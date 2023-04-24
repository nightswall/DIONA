import pandas as pd
from warnings import simplefilter


class DataLoader():
    def initalize_training_data(__self__, dataset_path):
        training_set = pd.read_csv(dataset_path)

        class_names = training_set.target.unique()
        training_set = training_set.astype("category")
        category_columns = training_set.select_dtypes(["category"]).columns

        training_set[category_columns] = training_set[category_columns].apply(lambda x : x.cat.codes)

        x_columns = training_set.columns.drop("target")
        x_training = training_set[x_columns].values
        y_training = training_set["target"]

        return x_training, y_training

    def initialize_test_data(__self__, dataset_path):
        testing_set = pd.read_csv(dataset_path)

        class_names = testing_set.target.unique()
        testing_set = testing_set.astype("category")
        category_columns = testing_set.select_dtypes(["category"]).columns

        testing_set[category_columns] = testing_set[category_columns].apply(lambda x : x.cat.codes)

        x_columns = testing_set.columns.drop("target")
        x_testing = testing_set[x_columns].values
        y_testing = testing_set["target"]

        return x_testing, y_testing