import json
import os, sys
from meta_analysor import fetch_meta

if __name__ == "__main__":
    args = sys.argv
    path = args[2]
    for _jsonfile in os.listdir(path):
        if "meta" not in _jsonfile:
            with open(''.join((path,_jsonfile))) as json_dataset:
                dataset = json.load(json_dataset)
                meta_dataset = fetch_meta(dataset)
                with open(''.join((path,"meta_"+_jsonfile)),"w+") as metafile:
                    json.dump(meta_dataset, metafile, indent=4)
    # try:
    #     path = args[2]
    #     for _jsonfile in os.listdir(path):
    #         with open(''.join(path,_jsonfile)) as json_dataset:
    #             dataset = json.load(json_dataset)
    #             print(fetch_meta(dataset))
    # except:
    #     print("""Usage: python3 meta_main.py -p /path/to/dir/json""")
    #     exit(1)