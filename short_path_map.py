import json
import boto3
import networkx as nx
import numpy as np
import random
from boto3.dynamodb.conditions import Key
import requests
import json
from flatten_json import flatten
   

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
        try:
            start = np.random.randint(0,40)
            next_node = next_number(start,er, g, q, r)
            updateQ(start,next_node,lr,discount, q, r)
        except:
            break

def shortest_path(begin, end, q):

    path = []
    msg = False
    path = [begin]
    if not np.argmax(q[begin,]):
        print(path)
        print(msg)
        return path, msg
    else:
        next_node = np.argmax(q[begin,])
        path.append(next_node)
        temp = next_node
        while next_node != end:
            next_node = np.argmax(q[next_node,])
            if next_node == temp:
                msg = False
                print(path)
                print(msg)
                break
            path.append(next_node)
            msg = True
            print(path)
            print(msg)
        return path, msg


def get_shortest_path(origin_iot, q, edges):
    map_names = {0:'R-A1',1:'R-A2',2:'R-B1',3:'R-C1', 4:'R-C2',5:'R-D1',6:'R-D2', 7:'R-E1', 8:'R-F1', 9:'R-G1', 10:'R-H1',
               11:'R-I1', 12:'R-M1', 13:'R-M2',14:'R-M3', 15:'R-N1',16:'W-1',17:'W-2', 18:'W-3', 19:'W-4', 20: 'W-5',
               21:'W-6', 22:'W-7', 23:'W-8', 24:'W-9', 25:'W-10', 26:'W-11', 27:'W-12', 28:'W-13', 29:'W-14', 30:'W-15',
               31:'W-16', 32:'W-17', 33:'W-18', 34:'W-19', 35:'W-20', 36:'W-21', 37:'W-22', 38:'R-B2',39:'W-23'}
    res = []
    spath = []
    pathFlag = False
    origin = 0
    keyExist = False
    #print(origin_iot)
    for key, value in map_names.items():
        if origin_iot == value:
            origin = key
    #print(origin)
    for key, value in edges:
        if key == origin:
            keyExist = True
    if (keyExist == True):
        spath, pathFlag = shortest_path(origin,31,q)
        if(pathFlag == True):
            for n in spath:
                res.append(map_names[n])
    return res, pathFlag

def get_map():
    url = "https://knaiab6xvbgbngi526537bslgu.appsync-api.us-east-1.amazonaws.com/graphql"
    query = \
        """
        query MyQuery {
            getBuilding(id: "id001") {
                edges {
                    items {
                        sourceIoT {
                            number
                        }
                        destinationIoT {
                            number
                        }
                        isActive
                        canBeDeactivated
                    }
                }
            }
        }
        """

    payload=json.dumps({"query": query})
    headers = {
    'x-api-key': 'da2-bevlp556a5hpzciuumghepwnqy',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    edgesDb = json.loads(response.text)['data']['getBuilding']['edges']['items']
    print(edgesDb)
    dict_edges = {}
    for d in edgesDb:
        if(d['isActive'] == False):
            dict_edges[d['sourceIoT']['number']] = d['destinationIoT']['number']
    print(dict_edges)
    mapList = [(k, v) for k, v in dict_edges.items()]
    revMapList = [(v, k) for k, v in dict_edges.items()]
    edges = mapList + revMapList
    print(edges)
    return edges

def parse_node_list(lst_start_node, q, edges):
    s_path = []
    pFlag = False
    sPathList = {}
    print(lst_start_node)
    for sn in lst_start_node:
        sPathList[sn] = {}
        print(sn)
        s_path, pFlag = get_shortest_path(sn, q, edges)
        print(s_path)
        print(pFlag)
        sPathList[sn]["shortestPath"] = s_path
        sPathList[sn]["actionCode"] = pFlag
    print(sPathList) 
    return sPathList


def lambda_handler(event, context):
    lst_snode = []
    lst_snode =event['start_node_lst']
    sPathLst = {}

    ################### Read from Edge Table ####################
    edges = get_map()

    #############################################################

    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)

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
    
    sPathLst = parse_node_list(lst_snode, q, edges)
    return sPathLst
    