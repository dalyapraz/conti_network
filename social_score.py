from functions import find_users, time_parser
import networkx as nx

G = nx.Graph() 
Users = find_users('user_lists/users.txt')
G.add_nodes_from(Users)

def all_chat_timestamps():
    chat_logs = time_parser('logs/chat_logs.json')
    jabber_logs = time_parser('logs/jabber_logs.json')
    messages = {}
    with open('user_lists/users.txt') as f:
        users = f.read().splitlines()
    for i in users:
        messages[i] = {}
    for i in chat_logs:
        sender = i['from']
        receiver = i['to']
        if receiver in messages[sender].keys():
            messages[sender][receiver].append(i['ts'])
        else: 
            messages[sender][receiver] = [i['ts']]
    for i in jabber_logs:
        sender = i['from']
        receiver = i['to']
        if receiver in messages[sender].keys():
            messages[sender][receiver].append(i['ts'])
        else: 
            messages[sender][receiver] = [i['ts']]
    for i in messages.keys():
        for j in messages[i].keys():
            messages[i][j] = sorted(messages[i][j])
    return messages
interactions = all_chat_timestamps()

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

def generate_edges(interactions):
    for user1 in interactions.keys():
        for user2 in interactions[user1].keys():
            inter1 = interactions[user1][user2]
            if user2 in interactions.keys():
                if user1 in interactions[user2].keys():
                    inter2 = interactions[user2][user1]
                else:
                    inter2 = []
            else: inter2 = []
            both = {user1:inter1, user2:inter2}
            wgt = len(extract_conversation(both))
            if wgt > 0:
                G.add_edge(user1, user2, key='edge', weight = wgt)
generate_edges(interactions)

def normalize(dictionary):
    n = min(dictionary.values())
    m = max(dictionary.values())
    for i in dictionary.keys():
        dictionary[i] = (dictionary[i]-n) / (m-n)
    return dictionary

user_cliques = {}
degrees = G.degree()
#degrees_dict = {degrees[i][0]: degrees[i][1] for i in range(0, len(degrees))}
degrees_dict = {}
for i in degrees:
    degrees_dict[i[0]] = i[1]
degrees_dict = normalize(degrees_dict)
betweeness_centrality_dict = normalize(nx.betweenness_centrality(G))
degree_centrality_dict = normalize(nx.degree_centrality(G))
hubs_authorities = normalize(nx.hits(G)[0])
user_clustering_coefficient = {}
user_shortest_path = {}
for node in Users:
    user_cliques[node] = len(nx.cliques_containing_node(G, node))
    cur_clustering_coefficient = nx.clustering(G, nodes = node)
    user_clustering_coefficient[node] = cur_clustering_coefficient
    shortest_path = nx.shortest_path_length(G, source=node).values()
    shortest_path_val = sum(shortest_path) / (len(shortest_path))
    user_shortest_path[node] = shortest_path_val
user_clustering_coefficient = normalize(user_clustering_coefficient)
user_shortest_path = normalize(user_shortest_path)
user_cliques = normalize(user_cliques)

social_score = {}
for u in Users:
    social_score[u] = ((degrees_dict[u] + betweeness_centrality_dict[u] + degree_centrality_dict[u] + hubs_authorities[u] + user_clustering_coefficient[u] + user_shortest_path[u] + user_cliques[u])/7)*100
social_score = dict(sorted(social_score.items(), key=lambda item: item[1]))

import pandas as pd
df = pd.DataFrame.from_dict(social_score, orient='index', columns = ['Social Score'])
df["Degree"] = pd.Series(degrees_dict)
df["Betweeness Centrality"] = pd.Series(betweeness_centrality_dict)
df["Degree Centrality"] = pd.Series(degree_centrality_dict)
df["Hubs/Authorities Score"] = pd.Series(hubs_authorities)
df["Clustering Coefficient"] = pd.Series( user_clustering_coefficient)
df["Average Shortest Path"] = pd.Series(user_shortest_path)
df["Number of Cliques"] = pd.Series(user_cliques)
#display(df[399:])
pd.DataFrame.to_csv(df, path_or_buf="score.csv")

nx.write_gexf(G, 'conti_meaningful.gexf')