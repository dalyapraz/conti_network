import networkx as nx
import json
import dateutil.parser
import datetime
from clean import time_parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics

G = nx.read_gexf('conti.gexf')

def sort_in_degrees():
    indegrees = G.in_degree()
    sorted_nodes = sorted(indegrees, key=lambda x: x[1], reverse=True)
    return sorted_nodes

def sort_out_degrees():
    outdegrees = G.out_degree()
    sorted_nodes = sorted(outdegrees, key=lambda x: x[1], reverse=True)
    return sorted_nodes

def message_cluster(message_lst):
    start = message_lst[0] + datetime.timedelta(hours=12)
    result = 1
    for i in range(len(message_lst)):
        if message_lst[i] > start:
            result+=1
            start = message_lst[i] + datetime.timedelta(hours=12)
    return result

def create_buckets(message_lst, delta):
    start = message_lst[0] + datetime.timedelta(hours=delta)
    buckets = {}
    buckets[start] = 1
    for i in range(len(message_lst)):
        if message_lst[i] > start:
            start = message_lst[i] + datetime.timedelta(hours=delta)
            buckets[start] = 1
        else:
            buckets[start] += 1
    return buckets

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

def node_communication_frequency():
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
    # interactions = {}
    # for u in users:
    #     interactions[u] = {}
    # for i in messages.keys():
    #     for j in messages[i].keys():
    #         if len(messages[i][j]) > 0: 
    #             interactions[i][j] = message_cluster(messages[i][j])
    # return interactions
    return messages

def sorted_node_lifespan():
    user_frequency = {}
    with open('user_lists/users.txt') as f:
        users = f.read().splitlines()
    jabber_json = time_parser('logs/jabber_logs.json')
    chat_json = time_parser('logs/chat_logs.json')
    for u in users:
        user_frequency[u] = []
    for i in jabber_json:
        sender = i['from']
        receiver = i['to']
        user_frequency[sender].append(i['ts'])
        user_frequency[receiver].append(i['ts'])
    for i in chat_json:
        sender = i['from']
        receiver = i['to']
        user_frequency[sender].append(i['ts'])
        user_frequency[receiver].append(i['ts'])
    result = {}
    for u in users: 
        user_frequency[u] = sorted(user_frequency[u])
        result[u] = user_frequency[u][-1]-user_frequency[u][0]
    result = dict(sorted(result.items(), key=lambda item: item[1]))
    return result

def extract_conversation(interaction_dict):
    interactions = []
    users = []
    for i in interaction_dict.keys():
        interactions += interaction_dict[i]
        users.append(i)
    if len(users) == 1:
        user1 = users[0]
        user2 = users[0]
    else:
        user1 = users[0]
        user2 = users[1]
    interactions.sort()
    conversations = []
    init_interaction = interactions[0]
    if init_interaction in interaction_dict[user1]:
        sender2 = user2
    else:
        sender2 = user1
    check_users = False
    if user1 == user2: check_users = True
    for i in range(len(interactions)-1):
        delta_new = interactions[i+1]-interactions[i]
        if interactions[i+1] in interaction_dict[sender2]:
            check_users = True
        if delta_new > datetime.timedelta(hours=8) and check_users:
            end_interaction = interactions[i+1]
            conversations.append([init_interaction, end_interaction])
            if i == len(interactions)-2:
                break
            init_interaction = interactions[i+2]
    return conversations

