import json 
import os
import argparse
import dateutil.parser

#Adds comma as a delimiter
#Currently, I am manually adding "{"messages":[" to the beginning, "]}" to the end, and manually removing 
#the last comma that is added by this function so it converts to a JSON object correctly
def file_formatting(fp):
    open_bracket = -1
    with open(fp) as original, open("formatted_conti.txt","a") as new:
        for line in original:
            for char in line:
                new.write(char)
                if(char=="{"):
                    open_bracket+=1
                elif(char=="}"):
                    open_bracket-=1
                    if(open_bracket==0):
                        new.write(",")

def json_converter(data_fp):
    data_objects = json.loads('{"messages": []}')
    f = open(data_fp)
    data = json.load(f)
    f.close()
    for i in data['messages']:
        data_objects['messages'].append(i)
    return data_objects

#creates json file to store our cleaned data in 

#file_formatting("original_conti_data.txt")
# result = open("conti_chats.json", "w")
# result_str = json.dumps(json_converter("formatted_conti.txt"))
# result.write(result_str)
# result.close()

def time_parser(data_json):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store')
    filename = data_json
    with open(filename) as f:
        json_data = json.load(f)
    for i in (json_data["messages"]):
        i['ts'] = dateutil.parser.isoparse(i['ts']) # ISO 8601 extended format
    return json_data
print(time_parser("conti_chats.json"))

# date_string = '2021-07-05T19:21:07.978947'
# new = dateutil.parser.isoparse(date_string) # ISO 8601 extended format
# print(type(new))
# print(new)




#checks for duplicates in the "body" of each message
#don't do this for body of the message- need to update it to compare every part of each object
# def remove_duplicate_messages(data_fp):
#     unique_data_objects = json.loads('{"messages": []}')
#     unique_messages = []
#     f = open(data_fp)
#     data = json.load(f)
#     f.close()
#     for i in data['messages']:
#         if i['body'] not in unique_messages:
#             unique_messages.append((i['body']))
#             unique_data_objects['messages'].append(i)
#     return unique_data_objects
