import networkx as nx
import json
import dateutil.parser
import datetime
from clean import time_parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics

G = nx.read_gexf('conti.gexf')

#future: length of messages
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
    #create a formula to determine number of interactions, not just messages
    #determine 12 hour differences between conversation 
    chat_logs = time_parser('chat_logs.json')
    jabber_logs = time_parser('jabber_logs.json')
    messages = {}
    with open('users.txt') as f:
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
    #create a formula to determine number of interactions, not just messages
    #determine 12 hour differences between conversation 
    chat_logs = time_parser('chat_logs.json')
    jabber_logs = time_parser('jabber_logs.json')
    messages = {}
    with open('users.txt') as f:
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
    print(messages['carter']['stern'])
    interactions = {}
    for u in users:
        interactions[u] = {}
    for i in messages.keys():
        for j in messages[i].keys():
            if len(messages[i][j]) > 0: 
                interactions[i][j] = message_cluster(messages[i][j])
    return interactions

#Going to start by doing this for users and then transferring the logic over to nodes in the graph?
#Make list of each users timestamps and sort, then find difference
#look at both sending and receiving as separate lists
#to think about lifespan, we can combine two lists
def sorted_node_lifespan():
    user_frequency = {}
    with open('users.txt') as f:
        users = f.read().splitlines()
    jabber_json = time_parser('jabber_logs.json')
    chat_json = time_parser('chat_logs.json')
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
    for i in range(len(interactions)-1):
        delta_new = interactions[i+1]-interactions[i]
        if interactions[i+1] in interaction_dict[sender2]:
            check_users = True
        if delta_new > datetime.timedelta(hours=8) and check_users:
            end_interaction = interactions[i+1]
            conversations.append([init_interaction, end_interaction])
            init_interaction = interactions[i+2]
    return conversations

user1 = 'professor'
user2 = 'target'
inter1 = find_interaction(user1, user2)
inter2 = find_interaction(user2, user1)
both = {user1:inter1, user2:inter2}
print((extract_conversation(both)))
# buckets = create_buckets(both, 8)
# plt.bar(buckets.keys(), buckets.values(), color='g')
# plt.show()

#all_user_interactions = node_communication_frequency()
#print(all_user_interactions)
# number_of_interactions = {}
# for i in all_user_interactions.keys():
#     number_of_interactions[i] = sum(all_user_interactions[i].values())
# number_of_interactions = dict(sorted(number_of_interactions.items(), key=lambda item: item[1]))
#print(number_of_interactions)
# mango to bentley 50
# carter to stern 60
# top_lifespan_users = sorted_node_lifespan()
# for i in top_lifespan_users:
#     print(i, ": ", top_lifespan_users[i])

# top_senders = sort_out_degrees()
# top_receivers = sort_in_degrees()
# print(top_receivers)
# carter_stern = find_interaction('carter', 'stern')
# stern_carter = find_interaction('stern', 'carter')
# both = carter_stern + stern_carter 
# interaction_dict = {}
# for i in carter_stern.keys():
#     interaction_dict[i] = carter_stern[i]
# for i in stern_carter.keys():
#     if i in 
# carter_stern_test_buckets = create_buckets(both, 2)
# plt.bar(carter_stern_test_buckets.keys(), carter_stern_test_buckets.values(), color='g')
# plt.show()
