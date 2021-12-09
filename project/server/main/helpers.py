# project/server/main/forms.py

from io import StringIO
from csv import reader

def ConvertCSVtoDict(filestorage):
    """
    Convert CSV to Dictionary by using column name as key
    """
    stream = StringIO(filestorage.stream.read().decode("utf-8"), newline=None)
    csv_reader = reader(stream, delimiter=',')
    header = next(csv_reader)
    result = {}
    total_data = 0
    duplicate_data = 0
    for row in csv_reader:
        key = "_".join(row)
        if key in result.keys():
            result[key]["total_exist"] += 1
            if result[key]["total_exist"] > 1:
                duplicate_data += 1
        else:
            row_dict = dict(zip(header, row))
            row_dict["total_exist"] = 1
            result[key] = row_dict
        total_data += 1
    result["total_data"] = total_data
    result["duplicate_data"] = duplicate_data
    result["header"] = header
    return result

def CompareTwoDict(dict1, dict2):
    """
    Compare two dict of 2 csvs
    and return the result of comparison
    """
    dict_report = {"matching_records": 0, "matches": [],"unmatched_records": 0, "unmatched_data": {}, "total_records": 0}
    for key in dict1:
        if key in dict2.keys():
            if key not in ["total_data", "duplicate_data", "header"]:
                dict_report["matching_records"] += 1
        else:
            dict1[key]["points"] = 0
            if "TransactionID" not in dict1[key]:
                dict_report["errors"] = "TransactionID is missing"
                break
            dict_report["unmatched_data"][dict1[key]["TransactionID"]] = dict1[key]
            dict_report["unmatched_records"] += 1
    dict_report["total_records"] = len(dict1)
    return dict_report

def SuggestPossibilities(dict1, dict2, headers):
    """
    Compare two dict of 2 csvs
    and return the result the suggestion of possible matches
    """
    for key in dict1["unmatched_data"]:
        if key in dict2["unmatched_data"].keys():
            points = 0
            for header in headers:
                if dict1["unmatched_data"][key][header] == dict2["unmatched_data"][key][header] and header != "TransactionID":
                    points += 1
            dict2["unmatched_data"][key]["points"] = points
            dict1["unmatched_data"][key]["points"] = points
    return dict1, dict2
    

def wrapper(func, arg, queue):
    """
    wrapper function is to put function to a queue
    to handle threading
    """
    queue.put(func(arg))
