import json 
import os

#Adds comma as a delimiter
#Currently, I am manually adding "{"messages":[" to the beginning, "]}" to the end, and manually removing 
#the last comma that is added by this function so it converts to a JSON object correctly
#I have tried a few approaches but have settled on this for the time being since it is more efficient
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

#checks for duplicates in the "body" of each message
def remove_duplicate_messages(data_fp):
    unique_data_objects = json.loads('{"messages": []}')
    unique_messages = []
    f = open(data_fp)
    data = json.load(f)
    f.close()
    for i in data['messages']:
        if i['body'] not in unique_messages:
            unique_messages.append((i['body']))
            unique_data_objects['messages'].append(i)
    return unique_data_objects

#creates json file to store our cleaned data in 

#file_formatting("original_conti_data.txt")
#result = open("unique_messages.json", "w")
#result_str = json.dumps(remove_duplicate_messages("formatted_conti.txt"))
#result.write(result_str)
#result.close()