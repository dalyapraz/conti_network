import networkx as nx
import json
import dateutil.parser
import datetime
from clean import time_parser

G = nx.read_gexf('conti.gexf')

def sort_node_degrees():
    node_degrees = G.degree()
    sorted_nodes = sorted(node_degrees, key=lambda x: x[1], reverse=True)
    return sorted_nodes

def node_communication_frequency():
    return

#Going to start by doing this for users and then transferring the logic over to nodes in the graph?
def sorted_node_lifespan():
    user_frequency = {}
    with open('users.txt') as f:
        users = f.read().splitlines()
    jabber_json = time_parser('jabber_logs.json')
    chat_json = time_parser('chat_logs.json')
    for u in users:
        user_frequency[u] = {'start': None, 'end': None}
    for i in jabber_json:
        current_user = i['from']
        if user_frequency[current_user]['start'] == None and user_frequency[current_user]['end']==None:
            user_frequency[current_user]['start'] = i['ts']
            user_frequency[current_user]['end'] = i['ts']
        if user_frequency[current_user]['start'] > i['ts']:
            user_frequency[current_user]['start'] = i['ts']
        elif user_frequency[current_user]['end'] < i['ts']:
            user_frequency[current_user]['start'] = i['ts']
    for i in chat_json:
        current_user = i['from']
        if user_frequency[current_user]['start'] == None and user_frequency[current_user]['end']==None:
            user_frequency[current_user]['start'] = i['ts']
            user_frequency[current_user]['end'] = i['ts']
        elif user_frequency[current_user]['start'] > i['ts']:
            user_frequency[current_user]['start'] = i['ts']
        elif user_frequency[current_user]['end'] < i['ts']:
            user_frequency[current_user]['start'] = i['ts']
    result = {}
    print(user_frequency['gold'])
    for obj in user_frequency.keys(): 
        if user_frequency[obj]['end'] != None:
            result[obj] = user_frequency[obj]['end'] - user_frequency[obj]['start']
    result = dict(sorted(result.items(), key=lambda item: item[1]))
    return result

top_lifespan_users = sorted_node_lifespan()
for i in top_lifespan_users:
    print(i, ": ", top_lifespan_users[i])