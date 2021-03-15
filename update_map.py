import json
import boto3
import networkx as nx
import numpy as np
import random

def get_node_key(node_name):
    map_names = {0:'R-A1',1:'R-A2',2:'R-B1',3:'R-C1', 4:'R-C2',5:'R-D1',6:'R-D2', 7:'R-E1', 8:'R-F1', 9:'R-G1', 10:'R-H1',
               11:'R-I1', 12:'R-M1', 13:'R-M2',14:'R-M3', 15:'R-N1',16:'W-1',17:'W-2', 18:'W-3', 19:'W-4', 20: 'W-5',
               21:'W-6', 22:'W-7', 23:'W-8', 24:'W-9', 25:'W-10', 26:'W-11', 27:'W-12', 28:'W-13', 29:'W-14', 30:'W-15',
               31:'W-16', 32:'W-17', 33:'W-18', 34:'W-19', 35:'W-20', 36:'W-21', 37:'W-22', 38:'R-B2',39:'W-23'}
    res = []
    node_key = ''
    for key, value in map_names.items():
        if node_name == value:
            node_key = key
    return node_key

def lambda_handler(event, context):
    first_node =str(event['first_node'])
    second_node =str(event['second_node'])
    first_node_key = get_node_key(first_node)
    second_node_key = get_node_key(second_node)
    # Replace the following edge list with list from DB, retrieve list from DB
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
    
    # Update the connection between the given nodes
    edges.remove((first_node_key,second_node_key))
    edges.remove((second_node_key,first_node_key))

    #Save updated edge list in DB
    #Implement Here

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Updated Map ": str(edges) 
        })
    }