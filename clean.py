import json 
import os
import argparse
import dateutil.parser
import numpy

#Formats file into JSON file
def file_formatting(fp):
    parser = json.JSONDecoder()
    parsed = []  # a list to hold individually parsed JSON structures
    with open(fp) as f:
        data = f.read()
    head = 0  # hold the current position as we parse
    while True:
        head = (data.find('{', head) + 1 or data.find('[', head) + 1) - 1
        try:
            struct, head = parser.raw_decode(data, head)
            parsed.append(struct)
        except (ValueError, json.JSONDecodeError):  # no more valid JSON structures
            break
    json_obj = json.dumps(parsed, indent=2)
    return json_obj

#Merges a directory of JSON files into one
def merge_chats(dir, output):
    result = []
    with open(output, "w") as out:
        for file in os.listdir(dir):
            #print(file)
            #input()
            f = os.path.join(dir, file)
            if os.path.isfile(f):
                out.write(file_formatting(f))
    result = file_formatting(output)
    with open(output, "w") as out:
        out.write(result)

#Updates master files with only username
def clean_users(data_json, output):
    with open(output, 'w') as out:
        out.write(json.dumps(data_json))

#Returns JSON object with datetime value 
def time_parser(data_json):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store')
    filename = data_json
    with open(filename) as f:
        json_data = json.load(f)
    for i in (json_data):
        i['ts'] = dateutil.parser.isoparse(i['ts']) # ISO 8601 extended format
    return json_data

#Returns a unique np array of users from a JSON file
def user_parser(data_json):
    users = []
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store')
    filename = data_json
    with open(filename) as f:
        json_data = json.load(f)
    for i in (json_data):
        user_str = i['from'].lower()
        lst = user_str.split('@')
        users.append(lst[0]) 
        i['from'] = lst[0]
        user_str = i['to'].lower()
        lst = user_str.split('@')
        users.append(lst[0]) 
        i['to'] = lst[0]
    users_np = numpy.array(users)
    return numpy.unique(users_np), json_data
