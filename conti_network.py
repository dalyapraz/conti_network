import networkx as nx
import igraph as ig
from numpy import loadtxt
import json 
import matplotlib.pyplot as plt
import dateutil.parser
G = nx.MultiDiGraph()

#Accepts a text file of usernames and returns as a list
def find_users(user_fp):
    users = []
    with open(user_fp) as f:
        users = f.read().splitlines()
    return users

#Adds users as nodes to G
def generate_nodes(users):
    G.add_nodes_from(users)

#Generates directed edges in G based off interactions
def generate_edges(data_json, src):
    for interaction in data_json:
        sender = interaction['from']
        receiver = interaction['to']
        if (sender, receiver) in G.edges():
            data = G.get_edge_data(sender, receiver, key='edge')
            if data['channel'] == src:
                # lst = data['time']
                # lst.append(dateutil.parser.isoparse(interaction['ts']))
                #G.add_edge(sender, receiver, key='edge', weight = data['weight'] + 1, time = lst)
                G.add_edge(sender, receiver, key='edge', weight = data['weight'] + 1)
            else:
                #G.add_edge(sender, receiver, key='edge', weight = 1, channel = src, time = [dateutil.parser.isoparse(interaction['ts'])])
                G.add_edge(sender, receiver, key='edge', weight = 1, channel = src)
        else:
            #G.add_edge(sender, receiver, key='edge', weight = 1, channel = src, time = [dateutil.parser.isoparse(interaction['ts'])])
            G.add_edge(sender, receiver, key='edge', weight = 1, channel = src)
    #print(G)
    return

#Pulls needed data from files
users = find_users('user_lists/users.txt')
with open('logs/jabber_logs.json') as f:
    jabber_json = json.load(f)
with open('logs/chat_logs.json') as f:
    chat_json = json.load(f)

#Builds network
generate_nodes(users)
generate_edges(jabber_json, "jabber")
generate_edges(chat_json, "chat")

nx.write_gexf(G, 'conti.gexf')

with open('sorted_edges.txt','w') as f:
   f.write(str(sorted(G.edges(data=True),key= lambda x: x[2]['weight'],reverse=True)))

# fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
# ig.layout_with_lgl(G, node_size=50)
# plt.show()
# h = ig.Graph.from_networkx(G)
# fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
# ax1.set_title("Plot with igraph plot")
# layout = h.layout_kamada_kawai()
# ig.plot(h, layout=layout, target=ax1)
# plt.axis("off")
# plt.show()
# print(max(dict(G.edges).items(), key=lambda x: x[1]['weight']))

# print(max(dict(G.degree()).items(), lambda x: x[2]['weight']))
# print(min(dict(G.degree()).items(), lambda x: x[2]['weight']))
#print(nx.get_edge_attributes(G, 'channel'))
# nx.draw(G)
# plt.show()
#https://igraph.org/python/versions/latest/
#https://towardsdatascience.com/visualising-graph-data-with-python-igraph-b3cc81a495cf?gi=737fbb3e668