import datetime
import dateutil.parser 
import json
import argparse
import os
import pickle

def time_parser(data_json):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store')
    filename = data_json
    with open(filename) as f:
        json_data = json.load(f)
    for i in (json_data):
        i['ts'] = dateutil.parser.isoparse(i['ts']) # ISO 8601 extended format
    return json_data


def find_interaction(to, fro):
    chat_logs = time_parser('logs/chat_logs.json')
    jabber_logs = time_parser('logs/jabber_logs.json')
    messages = {}
    with open('user_lists/users.txt') as f:
        users = f.read().splitlines()
    for i in users:
        messages[i] = {}
    for i in users:
        for j in users:
            messages[i][j] = []
    for i in chat_logs:
        sender = i['from']
        receiver = i['to']
        messages[sender][receiver].append(i['ts'])
    for i in jabber_logs:
        sender = i['from']
        receiver = i['to']
        messages[sender][receiver].append(i['ts'])
    for i in messages.keys():
        for j in messages[i].keys():
            messages[i][j] = sorted(messages[i][j])
    return messages[to][fro]


def find_users(user_fp):
    users = []
    with open(user_fp) as f:
        users = f.read().splitlines()
    return users

def all_conversations_sorted():
    # Step 1: Count messages in JSON logs
    chat_logs = time_parser('logs/chat_logs.json')
    jabber_logs = time_parser('logs/jabber_logs.json')
    structured_messages = {} # dict

    initial_count = len(chat_logs) + len(jabber_logs)
    print(f"Initial total message count: {initial_count}")

    def extract_conversations(logs):
        for i in logs:
            sender = i['from']
            receiver = i['to']
            key1, key2 = sorted([sender, receiver])
            if key1 not in structured_messages:
                structured_messages[key1] = {}
            if key2 not in structured_messages[key1]:
                structured_messages[key1][key2] = []
            structured_messages[key1][key2].append((i['ts'], sender, receiver, i['body']))

    extract_conversations(chat_logs)
    extract_conversations(jabber_logs)

    # Step 2: Count messages in structured_messages
    processed_count = sum(len(convo) for user in structured_messages.values() for convo in user.values())
    print(f"Total processed message count: {processed_count}")

    # Sorting each conversation by time
    for i in structured_messages.keys():
        for j in structured_messages[i].keys():
            structured_messages[i][j].sort(key=lambda x: x[0])  # Sort by timestamp

    if initial_count != processed_count:
        print(f"Mismatch detected! Initial count: {initial_count}, Processed count: {processed_count}")
    else:
        print("Message counts match.")
    return structured_messages

def count_files_in_folder(folder_path):
    try:
        # List all items in the directory and filter for files
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return len(files)
    except FileNotFoundError:
        print("Folder not found.")
        return 0
    
def split_to_txt_files(conversations_dict, save_to_path):
    # Ensure the directory structure exists
    if not os.path.exists(save_to_path):
        os.makedirs(save_to_path)

    for user_i in conversations_dict.keys():
        for user_j in conversations_dict[user_i].keys():
            # Create file for each 1-1 conversation 
            output_file_path = f'{save_to_path}{user_i}<>{user_j}.txt'
            
            # Write each message to the text file
            with open(output_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write("Timestamp\tFrom\tTo\tMessage\n")  # Header row
                for message in conversations_dict[user_i][user_j]:
                    ts, from_user, to_user, body = message
                    txt_file.write(f"{ts}\t{from_user}\t{to_user}\t{body}\n")


def count_unique_users_in_conversations(conversations_dict):
    users = set()
    for user_i, user_j_convos in conversations_dict.items():
        # Add user_i only once
        users.add(user_i)
        # Add each user_j from the nested dictionary of user_i
        users.update(user_j_convos.keys())
    return len(users)

def save_graph(graph, filename):
    with open(filename, "wb") as f:
        pickle.dump(graph, f)
    print(f"Graph saved as {filename}")

def load_graph(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    print(f"Graph loaded from {filename}")
    return graph