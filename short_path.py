import json
import boto3
import networkx as nx
import numpy as np
import random
   

def next_number(start,er, g, q, r):
    random_value = random.uniform(0,1)
    if random_value < er:
        sample= g[start]
    else:
        sample = np.where(q[start,] == np.max(q[start]))[1]
    next_node = int(np.random.choice(sample,1))
    return next_node

def updateQ(node1,node2,lr,discount, q, r):
    max_index = np.where(q[node2,]==np.max(q[node2,]))[1]
    if max_index.shape[0]>1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    max_value = q[node2,max_index]
    q[node1,node2] = int((1-lr)*q[node1,node2]+lr*(r[node1,node2]+discount*max_value))

def learn(er,lr,discount, g, q, r):
    for i in range(50000):
        start = np.random.randint(0,11)
        next_node = next_number(start,er, g, q, r)
        updateQ(start,next_node,lr,discount, q, r)

def shortest_path(begin, end, q):
    path = [begin]
    next_node = np.argmax(q[begin,])
    path.append(next_node)
    while next_node != end:
        next_node = np.argmax(q[next_node,])
        path.append(next_node)
    return path


def lambda_handler(event, context):
    start_node =int(event['start_node'])
    end_node =10
    e = [(0,4),(4,0),(0,3),(3,0),(1,2),(2,1),(1,4),(4,1),(1,8),(8,1),(1,9),(9,1),(2,3),(3,2),(2,6),(6,2),(1,5),(5,1),(2,5), (5,2),(5,6),(6,5),(7,8),(8,7),(7,5),(5,7),(8,9),(9,8),(8,10),(10,8),(9,10),(10,9)]
    edges = e
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    # nx.draw_networkx_nodes(g,pos)
    # nx.draw_networkx_edges(g,pos)
    # nx.draw_networkx_labels(g,pos)

    r = np.matrix(np.zeros(shape = (11,11)))
    for x in g[10]:
        r[x,10] = 100
    
    q = np.matrix(np.zeros(shape = (11,11)))
    q-=100
    for node in g.nodes:
        for x in g[node]:
            q[node,x]=0
            q[x,node]=0
    learn(0.5,0.8,0.8,g,q,r)
    s_path =shortest_path(start_node, end_node, q)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Shortest Path ": str(s_path)
        })
    }



