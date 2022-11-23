import argparse
import parse_datasets as parse
from globals import datasets

# Below is defined to parse command line arguments.

parser = argparse.ArgumentParser(description = "Dataset Parser for DL Engine\n" + 
											"For usage: datasets['dataset_name'] will return the corresponding dataset dictionary gathered from the file.\n" +
										    "From the dataset dictionary, by using column names of the datasets as indexes, " +
										    "one can gather corresponding data points.", formatter_class = argparse.RawTextHelpFormatter)
required_arguments = parser.add_argument_group("Required Arguments")
required_arguments.add_argument("-path", type = str, help = "A path to the folder that contains datasets", required = True)
args = parser.parse_args()

# Main function links datasets to the global dictionary defined for future use.

def main(path_to_dir):
	global datasets
	dataset = parse.parse_dataset(path_to_dir)
	dataset_cnt, dataset_names = 0, []
	for idx in range(len(dataset)):
		dataset_name = parse.get_key(dataset, idx)
		datasets[dataset_name] = dataset[dataset_name]
		dataset_cnt = dataset_cnt + 1
		dataset_names.append(dataset_name)
	print(f"Read {dataset_cnt} datasets, corresponding file names are: {dataset_names}")


if __name__ == "__main__":
	main(args.path)