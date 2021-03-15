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
        start = np.random.randint(0,40)
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
    map_names = {0:'R-A1',1:'R-A2',2:'R-B1',3:'R-C1', 4:'R-C2',5:'R-D1',6:'R-D2', 7:'R-E1', 8:'R-F1', 9:'R-G1', 10:'R-H1',
               11:'R-I1', 12:'R-M1', 13:'R-M2',14:'R-M3', 15:'R-N1',16:'W-1',17:'W-2', 18:'W-3', 19:'W-4', 20: 'W-5',
               21:'W-6', 22:'W-7', 23:'W-8', 24:'W-9', 25:'W-10', 26:'W-11', 27:'W-12', 28:'W-13', 29:'W-14', 30:'W-15',
               31:'W-16', 32:'W-17', 33:'W-18', 34:'W-19', 35:'W-20', 36:'W-21', 37:'W-22', 38:'R-B2',39:'W-23'}
    res = []
    origin = 0
    print(origin_iot)
    for key, value in map_names.items():
        if origin_iot == value:
            origin = key
    print(origin)
    for n in shortest_path(origin,31,q):
         res.append(map_names[n])
    return res

def lambda_handler(event, context):
    start_node =str(event['start_node'])
    #end_node =10
    ################# Read the List from DB #########################
    edges = [(9,16),(16,9),(10,17),(17,10),(11,18),(18,11),(16,17),(17,16),(17,18),(18,17),
         (18,19),(19,18),(19,21),(21,19),(20,21),(21,20),(20,0),(0,20),(21,24),(24,21),
         (22,24),(24,22),(22,1),(1,22),(24,12),(12,24),(23,24),(24,23),(23,2),(2,23),
         (24,25),(25,24),(25,13),(13,25),(25,27),(27,25),(27,28),(28,27),(28,3),(3,28),
         (28,30),(30,28),(30,31),(31,30),(30,29),(29,30),(30,32),(32,30),(29,4),(4,29),
         (32,33),(33,32),(29,32),(32,29),(33,34),(34,33),(33,5),(5,33),(34,6),(6,34),
         (32,37),(37,32),(37,36),(36,37),(37,15),(15,37),(36,7),(7,36),(35,8),(8,35),
         (36,35),(35,36),(27,30),(30,27),(26,27),(27,26),(14,26),(26,14),(0,1),(1,0),
         (2,38),(38,2),(39,38),(38,39),(12,13),(13,12),(13,14),(14,13),(14,12),(12,14),
         (3,4),(4,3),(5,6),(6,5),(39,27),(27,39)]
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    # nx.draw_networkx_nodes(g,pos)
    # nx.draw_networkx_edges(g,pos)
    # nx.draw_networkx_labels(g,pos)

    # Intitialize Reward Matrix
    r = np.matrix(np.zeros(shape = (40,40)))
    for x in g[31]:
        r[x,31] = 100
    
    q = np.matrix(np.zeros(shape = (40,40)))
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



