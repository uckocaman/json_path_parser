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
    global exmp_values

    for k, val in json_data.items():
        if isinstance(val, dict):
            fields_list += [k + "." + x for x in json_field_path(val)]
        elif isinstance(val, list):
            if len(val) == 0:
                fields_list.append(k)
                data_types.append("Empty Array")
                exmp_values.append("Empty Array, nothing in here :(")
            elif isinstance(val[0], dict):
                fields_list += [k + "." + x for x in json_field_path(val[0])]
            else:
                fields_list.append(k)
                data_types.append(type(val[0]).__name__)
                exmp_values.append(val if len(val) <= 3 else val[:3])
        else:
            fields_list.append(k)
            data_types.append(type(val).__name__)
            exmp_values.append(val)
    return fields_list


def write_to_excel(fields, data_types, example_value):
    df = pd.DataFrame(
        list(zip(fields, data_types, example_value)),
        columns=["Field", "Data Type", "Example Value"],
    )
    df.loc[df["Data Type"] == "str", "Data Type"] = "string"
    df.loc[df["Data Type"] == "int", "Data Type"] = "integer"
    df.loc[df["Data Type"] == "bool", "Data Type"] = "boolean"

    dates = ["Date", "date", "Time", "time" "created_at", 'last_modified_at','updatedAt','createdAt'] # add lower  
    df.loc[
        df["Field"].str.contains("|".join(dates)), "Data Type"
    ] = "timestamp (please check from document)"
    df["Description"] = ""

    print(df)
    # df.to_excel("output.xlsx", index=False)


if __name__ == "__main__":
    data_types, exmp_values = [], []
    json_data = json_file(sys.argv[1])
    fields = json_field_path(json_data)
    write_to_excel(fields, data_types, exmp_values)
