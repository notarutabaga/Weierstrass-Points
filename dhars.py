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

def make_effective_away_from(G, q):
    # construct laplacian: adjacency matrix - degree matrix
    jacobian = np.array(list(G.get_adjacency()))
    for v in G.vs:
        jacobian[v.index][v.index] = -G.degree(v)
    
    # jacobian is the laplacian without row k and column k
    jacobian = np.delete(jacobian, G.vcount()-1, 0)
    jacobian = np.delete(jacobian, G.vcount()-1, 1)
    
    # determinant of jacobian
    m = np.linalg.det(jacobian)
    
    # for each inneffective vertex (not q), fire m chips from q to v until effective
    for v in G.vs:
        if v != q: 
            while G.vs[v.index]["divisor"] < 0:
                G.vs[v.index]["divisor"] += m
                G.vs[q.index]["divisor"] -= m
                
    return G.vs["divisor"]

def print_graph(G,i):
    # fig, ax = plt.subplots(figsize=(5,5))
    
    ig.plot(
        G,
        target="step"+str(i)+".png",
        layout="circle",
        vertex_color=["indianred" if burned else "lightsteelblue" for burned in G.vs["burned"]],
        edge_color=["indianred" if burned else "black" for burned in G.es["burned"]],
        vertex_label=[div for div in G.vs["divisor"]]
    )
    
    # plt.show()
    
# performs dhar's burning algoriothm on G
def dhars_burning(G):
    i=0
    
    # print("original graph")
    # print_graph(G,i)
    # i+=1
    
    # if D is already effective, done
    if is_effective(G.vs["divisor"]): 
        return True
    
    if degree(G.vs["divisor"]) < 0:
        return False
    
    # find subset of D that is not effective
    in_debt = [v for v in G.vs if G.vs[v.index]["divisor"] < 0]
    
    # choose one of the chips in debt at random
    q = random.choice(in_debt)
    
    # make the divisor effective away from q
    if not is_effective_away(G, q.index): 
        # G.vs["divisor"] = make_effective_away_from(G, q)
        # construct laplacian: adjacency matrix - degree matrix
        jacobian = np.array(list(G.get_adjacency()))
        for v in G.vs:
            jacobian[v.index][v.index] = -G.degree(v)
        
        # jacobian is the laplacian without row k and column k
        jacobian = np.delete(jacobian, G.vcount()-1, 0)
        jacobian = np.delete(jacobian, G.vcount()-1, 1)
        print(jacobian)
        
        # determinant of jacobian
        m = round(abs(np.linalg.det(jacobian)))
        print("m = " + str(m))
        
        # for each inneffective vertex (not q), fire m chips from q to v until effective
        for v in G.vs:
            if v != q: 
                while G.vs[v.index]["divisor"] < 0:
                    G.vs[v.index]["divisor"] += m
                    G.vs[q.index]["divisor"] -= m
    
    # print("after making effective away from q")                
    # print_graph(G,i)
    # i+=1
                
    # set all burning to false    
    G.vs["burned"] = False
    G.es["burned"] = False
           
    # continue the burning and firing process until D is effective or the entire graph is burned
    while not is_effective(G.vs["divisor"]) and not is_burned(G.vs["burned"]):
        # print("start of next dhar's iteration")
        # print_graph(G,i)
        # i+=1
        
        G.vs["burned"] = False # reset all vertices
        G.es["burned"] = False # reset all edges
        
        # print("reset burn")
        # print_graph(G,i)
        # i+=1
        
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
        
        # print("before spreading fire")
        # print_graph(G,i)
        # i+=1
        
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
        
        # print("after spreading fire")
        # print_graph(G,i)
        # i+=1
        
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
        
        # print("after firing along burned edges")
        # print_graph(G,i)
        # i+=1
    
    # print("final graph (before reset)")                    
    # print_graph(G,i)
    # i+=1
    
    # reset
    G.vs["burned"] = False
    G.es["burned"] = False
    
    # print("final graph (after reset)")
    # print_graph(G,i)
    # i+=1
    
    if is_effective(G.vs["divisor"]):
        return True 
    
    return False