import datetime
import copy
import sys
import re
import math
from difflib import SequenceMatcher

# dateformat = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d.%m.%Y", "%Y.%m.%d", "%d %m %Y", "%Y %m %d"]
# datetimehmformat = [_tf+" %H:%M" for _tf in dateformat]
# datetimehmsformat = [_tf+":%S" for _tf in datetimehmformat]
# datetimehmsmformat = [_tf+".%f" for _tf in datetimehmsformat]

dateformatre = [
    "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}", "^[0-9]{4}\\/[0-9]{1,2}\\/[0-9]{1,2}",
    "^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}", "^[0-9]{4}\\.[0-9]{1,2}\\.[0-9]{1,2}",
    "^[0-9]{1,2}\\s[0-9]{1,2}\\s[0-9]{4}", "^[0-9]{4}\\s[0-9]{1,2}\\s[0-9]{1,2}",
    "^[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", "^[0-9]{4}\\-[0-9]{1,2}\\-[0-9]{1,2}"
]

repat = ["/", ".", " ", "-"]

common_types = {
    "STR": {
        "occurrence": 0,
        "keywords": {}
    },
    "INT": {
        "occurrence": 0,
        "min": sys.maxsize,
        "max": -sys.maxsize,
        "avg": None
    },
    "NUMBER": {
        "occurrence": 0,
        "min": sys.maxsize,
        "max": -sys.maxsize,
        "avg": None
    },
    "DATE": {
        "occurrence": 0,
        "min": sys.maxsize,
        "max": -sys.maxsize,
        "min_str": None,
        "max_str": None,
    }
}

def datetime_reformatter(datetime: str) -> str:
    for pattern in dateformatre:
        res = re.search(pattern, datetime)
        if res:
            _date=res.group(0)
            _time=re.sub(pattern, "", datetime)
            index = dateformatre.index(pattern)
            _date=_date.split(repat[index//2])
            if index%2 == 0:
                _date=_date[::-1]
            _date="-".join(_date)
            return _date+_time

def datatype_decider(data: str) -> any:
    data_lower: str = data.lower()
    datatype_pred: str = ""
    date_candidate = None
    converted_data = data
    try:
        int(data_lower)
        datatype_pred+=("I")
    except:
        pass

    try:
        float(data_lower)
        datatype_pred+=("F")
        if 1_000_000_000 < float(data_lower) < datetime.datetime.utcnow().timestamp():
            datatype_pred+=("u")
    except:
        pass
    
    if not datatype_pred:
        try:
            date_candidate = datetime_reformatter(data)
            datetime.datetime.fromisoformat(date_candidate)
            datatype_pred+=("DT")
        except:
            pass

    if not datatype_pred:
        datatype_pred = "STR"

    else:
        if datatype_pred == "IFu":
            converted_data =  int(data)
            datatype_pred = "DATE"

        elif datatype_pred == "IF":
            converted_data = float(data)
            datatype_pred = "NUMBER"

        elif datatype_pred == "Fu":
            converted_data = float(data)
            datatype_pred = "DATE"

        elif datatype_pred == "F":
            converted_data = float(data)
            datatype_pred = "NUMBER"

        elif datatype_pred == "DT":
            converted_data = datetime.datetime.fromisoformat(date_candidate).timestamp()
            datatype_pred = "DATE"

        elif datatype_pred == "DTDT":
            print(data_lower)

        else:
            print("Awkward: ", data)

    return converted_data, datatype_pred



def fetch_meta(dataset: dict) -> dict:
    dataset_meta = {}
    for column in dataset.keys():
        column_meta = copy.deepcopy(common_types)
        for data in dataset[column]:
            cdata, pred = datatype_decider(data)
            column_meta[pred]["occurrence"]+=1
            if pred in ("INT", "NUMBER", "DATE"):
                column_meta[pred]["min"] = min(column_meta[pred]["min"], cdata)
                column_meta[pred]["max"] = max(column_meta[pred]["max"], cdata)
            
            elif pred in ("STR"):
                if column_meta[pred]["keywords"].get(cdata, None):
                    column_meta[pred]["keywords"][cdata]+=1
                else:
                    column_meta[pred]["keywords"][cdata]=1

        for key in column_meta.keys():
            if not column_meta[key]["occurrence"]:
                column_meta[key] = None
        
        if column_meta['STR']:
            for key in column_meta['STR']['keywords']:
                column_meta['STR']['keywords'][key]=float("{:.3f}".format(column_meta['STR']['keywords'][key]/column_meta['STR']['occurrence']))
        
        if column_meta['DATE']:
            column_meta['DATE']['min_str'] = (datetime.datetime.fromtimestamp(column_meta['DATE']['min'])).isoformat()
            column_meta['DATE']['max_str'] = (datetime.datetime.fromtimestamp(column_meta['DATE']['max'])).isoformat()

        column_meta["name"] = column
        column_meta["number_of_rows"] = len(dataset[column])
        dataset_meta[column] = column_meta

    return dataset_meta

def name_similarity(column_name: str, column_set: list) -> float:
    ratio = 0
    for column_in_set in column_set:

        ratio = max(ratio, SequenceMatcher(None, column_name, column_in_set["col"]["name"]).ratio())
    return ratio

# def number_similarity(column_name: str, column_set: list) -> float:
#     ratio = 0
#     for column_in_set in column_set:
#         ratio = max(ratio, SequenceMatcher(None, column_name, column_in_set["col"]["name"]).ratio())
#     return ratio
# jaccard similarity will be implemented
# data_type_matching will be implemented

def match_meta(universal_set, dataset):
    if not universal_set:
        for column in dataset["meta_columns"]:
            match_set = [[1]]
            u_set = {"match_set": match_set, "columns": [{ "src": dataset["dataset_name"], "col": dataset["meta_columns"][column]}]}
            universal_set.append(u_set)
    else:
        for column in dataset["meta_columns"]:
            name_similarity_ratio = 0
            number_similarity_ratio = 0
            date_similarity_ratio = 0
            str_similarity_ratio = 0

            column_similarity_ratio = {
                "name_sr": [0, -1],
                "number_sr": [0, -1],
                "date_sr": [0, -1],
                "str_sr": [0, -1]
            }

            for u_set in universal_set:
                if dataset["dataset_name"] in list(map(lambda x: x["src"], u_set["columns"])):
                    # print("Same source")
                    continue
                if dataset["meta_columns"][column]["DATE"] and u_set["columns"][0]["col"]["DATE"]:
                    column_similarity_ratio["date_sr"][0] = 1
                    column_similarity_ratio["date_sr"][1] = universal_set.index(u_set)

                else:
                    tmp_name_sim = name_similarity(dataset["meta_columns"][column]["name"], u_set["columns"])
                    # print(dataset["meta_columns"][column]["name"], list(map(lambda x: x["col"]["name"], u_set["columns"])), tmp_name_sim)
                    if column_similarity_ratio["name_sr"][0] < tmp_name_sim:
                        column_similarity_ratio["name_sr"][0] = tmp_name_sim
                        column_similarity_ratio["name_sr"][1] = universal_set.index(u_set)

            if column_similarity_ratio["date_sr"][0] and u_set["columns"][0]["col"]["DATE"]:
                match_index = column_similarity_ratio["date_sr"][1]
            else:

                match_index = column_similarity_ratio["name_sr"][1]

            if match_index > -1:
                universal_set[match_index]["columns"].append({ "src": dataset["dataset_name"], "col": dataset["meta_columns"][column]})
            else:
                match_set = [[1]]
                universal_set.append({"match_set": match_set, "columns": [{ "src": dataset["dataset_name"], "col": dataset["meta_columns"][column]}]})
                
    return universal_set