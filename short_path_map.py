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
        start = np.random.randint(0,33)
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

def get_shortest_path(origin_iot, q):
    map_names = {0:'R-A1',1:'R-B1',2:'R-C1',3:'R-D1', 4:'R-E1',5:'R-F1',6:'R-G1', 7:'R-H1', 8:'R-I1', 9:'R-M1', 10:'R-M2',
                11:'R-M3', 12:'R-N1', 13:'W-1',14:'W-2', 15:'W-3',16:'W-4',17:'W-5', 18:'W-6', 19:'W-7', 20: 'W-8',
                21:'W-9', 22:'W-10', 23:'W-11', 24:'W-12', 25:'W-13', 26:'W-14', 27:'W-15', 28:'W-16', 29:'W-17', 30:'W-18',
                31:'W-19', 32:'W-20'}
    res = []
    origin = 0
    print(origin_iot)
    for key, value in map_names.items():
        if origin_iot == value:
            origin = key
    print(origin)
    for n in shortest_path(origin,26,q):
         res.append(map_names[n])
    return res

def lambda_handler(event, context):
    start_node =str(event['start_node'])
    #end_node =10
    edges = [(6,13),(13,6),(7,14),(14,7),(8,15),(15,8),(15,16),(16,15),(13,14),(14,13),(14,15),(15,14),(16,17),(17,16),
            (17,0),(0,17),(0,19),(19,0),(19,20),(20,19),(17,18),(18,17),(18,20),(20,18),(20,9),(9,20),(20,21),(21,20),
            (21,10),(10,21),(21,23),(23,21),(23,22),(22,23),(22,11),(11,22),(23,25),(25,23),(25,26),(26,25),(25,24),(24,25),
            (24,2),(2,24),(2,27),(27,2),(27,25),(25,27),(25,29),(29,25),(27,29),(29,27),(29,28),(28,29),(29,32),(32,29),
            (32,12),(12,32),(32,31),(31,32),(3,31),(31,3),(31,4),(4,31),(30,31),(31,30),(30,5),(5,30),(1,19),(19,1)]
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    # nx.draw_networkx_nodes(g,pos)
    # nx.draw_networkx_edges(g,pos)
    # nx.draw_networkx_labels(g,pos)

    r = np.matrix(np.zeros(shape = (33,33)))
    for x in g[26]:
        r[x,26] = 100
    
    q = np.matrix(np.zeros(shape = (33,33)))
    q-=100
    for node in g.nodes:
        for x in g[node]:
            q[node,x]=0
            q[x,node]=0
    learn(0.5,0.8,0.8,g,q,r)
    s_path =get_shortest_path(start_node, q)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Shortest Path ": str(s_path)
        })
    }



