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

#Merge all jabber into one json file
jabber_dir = "Conti Jabber Chat Logs 2021 - 2022"
jabber_out = "jabber_logs.json"
#merge_chats(jabber_dir,jabber_out )
jabber_users, jab_json_with_usernames = user_parser(jabber_out)
clean_users(jab_json_with_usernames, jabber_out)

#Merge all chats into one json file
chat_dir = "Conti Chat Logs 2020"
chat_out = "chat_logs.json"
#merge_chats(chat_dir,chat_out)
chat_users, chat_json_with_usernames = user_parser(chat_out)
clean_users(chat_json_with_usernames, chat_out)

#Evaluates user lists
both = [i for i in jabber_users if i in chat_users]
unique_chat = [i for i in chat_users if i not in jabber_users]
unique_jabber = [i for i in jabber_users if i not in chat_users]
all_users = numpy.union1d(jabber_users, chat_users)
with open('users.txt', 'w') as file:
    numpy.savetxt(file, all_users, fmt='%s')

#Various result printers
def print_users(jabber_users,chat_users):
    print("Jabber Users")
    print(jabber_users)
    print("Chat Users")
    print(chat_users)
    
def print_unique_lists(both, unique_jabber, unique_chat):
    print("---Comparison---")
    print("Both")
    print(numpy.array(both))
    print("Only Jabber")
    print(numpy.array(unique_jabber))
    print("Only Chat")
    print(numpy.array(unique_chat))

def print_analysis(jabber_users,chat_users,both,unique_jabber,unique_chat):
    print("---ANALYSIS---")
    print("Jabber+Chat:", len(jabber_users)+len(chat_users))
    print("Intersection:", len(both))
    print("Jabber & ~Chat:", len(unique_jabber))
    print("Chat & ~Jabber:", len(unique_chat))

print_analysis(jabber_users,chat_users,both,unique_jabber,unique_chat)
