import random
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import math
from queue import Queue

# returns the degree of the divisor (ie sum of chips distrtibuted)
def degree(divisor):
    return sum(divisor)

# an effective divisor has all chips >= 0 (ie all are not in debt)
def is_effective(divisor):
    for div in divisor:
        if div < 0: 
            return False 
    
    return True

# checks to see if the divisor is effective excluding one specified vertex
def is_effective_away(G, away_from):
    for v in G.vs:
        if v.index != away_from:
            if G.vs[v.index]["divisor"] < 0: 
                return False
        
    return True

# checks if all vertices in the vertex set are burned
def is_burned(burned):
    for burn in burned:
        if burn == False: 
            return False
    
    return True 

    
# performs dhar's burning algoriothm on G
def dhars_burning(G):
    # if D is already effective, done
    if is_effective(G.vs["divisor"]): 
        return True
    
    if sum(G.vs["divisor"]) < 0:
        return False
    
    # find subset of D that is not effective
    in_debt = [v for v in G.vs if G.vs[v.index]["divisor"] < 0]
    
    # choose one of the chips in debt at random
    q = random.choice(in_debt)
        
    while not is_effective_away(G, q.index):
        print(G.vs["divisor"])
        print(q.index)
        queue = []
        queue.append(q)
        
        G.vs["visited"] = False
        
        while len(queue) > 0:
            curr = queue.pop(0)
            curr_neighbors = curr.neighbors()
            
            for neighbor in curr_neighbors:
                if not G.vs[neighbor.index]["visited"] and G.vs[neighbor.index]["divisor"] < 0:
                    G.vs[curr.index]["divisor"] += G.vs[neighbor.index]["divisor"]
                    G.vs[neighbor.index]["divisor"] = 0
            
            for neighbor in curr_neighbors:
                if not G.vs[neighbor.index]["visited"]:
                    queue.append(neighbor)
            
            G.vs[curr.index]["visited"] = True   
        
        print(G.vs["divisor"])
        print()
    
    print("============================")
        
    G.vs["burned"] = False
    G.es["burned"] = False
           
    # continue the burning and firing process until D is effective or the entire graph is burned
    while not is_effective(G.vs["divisor"]) and not is_burned(G.vs["burned"]):
        G.vs["burned"] = False # reset all vertices
        G.es["burned"] = False # reset all edges
        
        G.vs[q.index]["burned"] = True
        
        # set all incident edges of q on fire
        incidents = G.incident(q)
        for edge in incidents: 
            G.es[edge]["burned"] = True 
        
        # add all burned nodes to one list
        burned_nodes = []
        burned_nodes.append(q)
        
        # keep track of unburned neighbors of the burned nodes
        unburned_nodes = []
        
        # controls how far the fire spreads before firing
        spread = True
        
        # loop
        while spread:
            # add all unburned neighbors of burned to another
            for node in burned_nodes:
                curr_neighbors = node.neighbors()
                
                for neighbor in curr_neighbors:
                    if not G.vs[neighbor.index]["burned"]:
                        if neighbor not in unburned_nodes:
                            unburned_nodes.append(neighbor)
             
            # assume we cannot continue spreading      
            spread = False
    
            # loop through each unburned neighbor to see if the fire can spread
            for node in unburned_nodes:
                curr_incidents = G.incident(node)
                
                # number of incident edges burned
                count = 0
                for edge in curr_incidents:
                    if G.es[edge]["burned"]: 
                        count += 1
                
                # if D(v) < burned incident edges
                if G.vs[node.index]["divisor"] < count:
                    # burn the current node
                    G.vs[node.index]["burned"] = True
                    
                    if node not in burned_nodes:
                        burned_nodes.append(node)
                    
                    unburned_nodes.remove(node)

                    for edge in curr_incidents:
                        G.es[edge]["burned"] = True
                    
                    # since we were able to burn another node, we may be able to spread farther
                    spread = True
        
        # fire from unburned nodes along burned edges only
        for node in unburned_nodes:
            curr_neighbors = node.neighbors()
            
            # check each neighbor of the current node
            for target in curr_neighbors:
                if G.vs[target.index]["burned"]:
                    edge = G.get_eid(node, target)
                    
                    # only fire from an unburned node along a burned edge
                    if G.es[edge]["burned"]:
                        G.vs[node.index]["divisor"] -= 1
                        G.vs[target.index]["divisor"] += 1
    
    # reset
    G.vs["burned"] = False
    G.es["burned"] = False
    
    if is_effective(G.vs["divisor"]):
        return True 
    
    return False