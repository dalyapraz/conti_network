import datetime
import dateutil.parser 
import json
import argparse

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

