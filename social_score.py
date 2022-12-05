from network_analysis import sorted_node_lifespan, find_interaction, extract_conversation, node_communication_frequency
from conti_network import find_users
import datetime 
import networkx as nx
G = nx.Graph() 

# remove admins, test accounts, users with lifespan <30days
# def clean_users():
#     users = sorted_node_lifespan()
#     return_users = []
#     for u in users.keys():
#         if users[u] >= datetime.timedelta(days = 30):
#             if 'admin' not in u and 'alarm' not in u:
#                 return_users.append(u)
#     return return_users
Users = find_users('user_lists/users.txt')
G.add_nodes_from(Users)

def generate_edges(interactions):
    for user1 in interactions.keys():
        for user2 in interactions[user1].keys():
            inter1 = find_interaction(user1, user2)
            inter2 = find_interaction(user2, user1)
            both = {user1:inter1, user2:inter2}
            wgt = len(extract_conversation(both))
            #ADD SOMETHING FOR IF FROM ONE USER TO SAME USER
            if wgt > 0:
                G.add_edge(user1, user2, key='edge', weight = wgt)
interactions = node_communication_frequency()
generate_edges(interactions)
print(G)
# reverse the graph (network): 
#  1.	Nodes = users; 
#  2.	Edges = undirected; meaningful conversations (threshold >5 convs)
