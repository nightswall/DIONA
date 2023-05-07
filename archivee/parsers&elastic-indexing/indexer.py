from elasticsearch import Elasticsearch
import os
import json



if __name__ == "__main__":
    elasticsearch = Elasticsearch('http://localhost:9200')
    doc_type = '_doc'
    os.chdir("./outputs")
    for file in os.listdir():
        if file.endswith(".json"):
            file_name = f"{file}"
            index_name = file_name.split(".")[0]
            index_name = index_name.lower() #elasticsearch accepts lowercase index names only
            json_file = open(file_name)
            json_data = json.load(json_file)
            for temp_data in (json_data):
                indexes= [{} for x in range(len(json_data[temp_data]))] #creates n (numbers of row) dictionary object for m json outputs. 
                break
            for temp_data in (json_data):
                i=0
                for i in range((len(json_data[temp_data]))):
                    indexes[i][temp_data]= json_data[temp_data][i]
                    i+=1
                
            for i in range((len(indexes))):
                ret = elasticsearch.index(index=index_name,document=indexes[i])
            print(ret)
                   

    ##query = {"query": {"match": {'Occupancy':1}}} example query syntax for future use
