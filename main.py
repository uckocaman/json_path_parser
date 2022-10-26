import pandas as pd
import numpy as np
from dateutil.parser import parse
import json
import sys

def json_file(file_path):
    f = open(file_path)
    json_data = json.load(f)
    
    return json_data

def json_field_path(json_data):
    if not isinstance(json_data, dict):
        return json_data
    
    fields_list = []
    global data_types

    for k, val in json_data.items():
        if isinstance(val, dict):
            fields_list += [k + "." + x for x in json_field_path(val)]
        elif isinstance(val, list):
            fields_list.append(k)
            if type(val[0]).__name__ == 'str':
                try: 
                    parse(val[0])
                    data_types.append('timestamp')
                except ValueError:
                    data_types.append(type(val[0]).__name__)
            else:
                data_types.append(type(val[0]).__name__)
        else:
            fields_list.append(k)
            if type(val).__name__ == 'str':
                try: 
                    parse(val[0])
                    data_types.append('timestamp')
                except ValueError:
                    data_types.append(type(val[0]).__name__)
            else:
                data_types.append(type(val).__name__)
    return fields_list

def write_to_excel(fields,data_types):
    df = pd.DataFrame(list(zip(fields, data_types)),columns =['Field', 'Data Type'])
    #df.loc[df["Data Type"] == "str", "Data Type"] = "string"

    df['Data Type'] = np.where(df['Data Type'] == "str", "string",
                       np.where(df['Data Type'] == "int", "integer",
                       np.where(df['Data Type'] == "bool", "boolean", df['Data Type'])))
    df['Description'] = ''

    df.to_excel('output.xlsx', index=False)

if __name__ == '__main__':
    data_types = []
    json_data = json_file(sys.argv[1])
    fields = json_field_path(json_data)
    
    write_to_excel(fields,data_types)