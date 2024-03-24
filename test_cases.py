import igraph as ig
from igraph import Graph
import matplotlib.pyplot as plt
import dhars
from weierstrass import canonical

def new_graph(edges, divisor):
    G = ig.Graph(edges)
    
    G.vs["divisor"] = divisor
    G.vs["weier"] = False
    
    G.vs["burned"] = False
    G.es["burned"] = False  
    
    return G 

def cubic():
    edges = [(0, 1), (0, 3), (0, 5),
        (1, 2), (1, 6),
        (2, 3), (2, 7),
        (3, 4),
        (4, 5), (4, 7),
        (5, 6),
        (6, 7),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)]

    return new_graph(edges, 0)

def housex():
    edges = [(0, 1), (0, 2),
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)]
    divisor = 0

    G = new_graph(edges, divisor)
    return G

def sun():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
    return new_graph(edges, 0)

def tulip():
    edges = [(0, 1), (0, 2), (0, 3),
             (1, 4),
             (2, 4),
             (3, 4),
             (4, 5), (4, 6), (4, 7), (4, 8),
             (5, 9),
             (6, 9),
             (7, 10),
             (8, 10)]
    
    return new_graph(edges, 0)

def cycle(n):
    edges = []
    for i in range(n):
        edges.append((i, (i+1) % n))
        
    G = new_graph(edges, 0)
    
    return G
    

def complete(n):
    G = Graph.Full(n)
    
    G.vs["divisor"] = 0
    
    G.vs["burned"] = False
    G.es["burned"] = False  
    
    return G 

def compl_bipart(n, m):
    G = ig.Graph.Full_Bipartite(n, m)
    
    G.vs["divisor"] = 0
    
    G.vs["burned"] = False
    G.es["burned"] = False
    
    G.vs["weier"] = False
            
    return G

# TO DOOOOO
def gen_peter(n, k):
    G = cycle(n)
    G.add_vertices(n)
    
    for i in range(n):
        G.add_edge(i, i + n)
    
    return G
        
def wheel(n):
    G = cycle(n-1)
    G.add_vertices(1)
    
    for i in range(n-1):
        G.add_edge(i, n-1)
    
    G.vs["divisor"] = 0
    G.vs["weier"] = False
    
    G.vs["burned"] = False
    G.es["burned"] = False  
    
    return G

# G1 = housex()
# G1.vs["divisor"] = [5, 2, -3, -1, 3]

# G2 = housex()
# G2.vs["divisor"] = canonical(G2)

# fig, ax = plt.subplots(figsize=(5,5))
# G = cycle(5)
# G.add_edge(0,2)
    
# formatted_labels = [f'$v_{{{str(v.index + 1)}}}$' for v in G.vs]

# # Assign the labels to the vertices
# G.vs['label'] = formatted_labels

# ig.plot(
#     G,
#     target="pptex.png",
#     layout="circle",
#     vertex_color="lightsteelblue",
#     vertex_label=G.vs['label'],
# )
    
# ig.plot(
#     G1,
#     target="housex.png",
#     layout="auto",
#     vertex_color="lightsteelblue",
#     vertex_label=G1.vs['label']
# )

# ig.plot(
#     G1,
#     target="housex_div.png",
#     layout="auto",
#     vertex_color="lightsteelblue",
#     vertex_label=G1.vs["divisor"]
# )

# ig.plot(
#     G2,
#     target="housex_canon.png",
#     layout="auto",
#     vertex_color="lightsteelblue",
#     vertex_label=G2.vs["divisor"]
# )

# G2.vs[0]["burned"] = True
# incidents = G2.incident(0)
# for edge in incidents: 
#     G2.es[edge]["burned"] = True 

# ig.plot(
#     G2,
#     target="housex_canon_selected.png",
#     layout="auto",
#     vertex_color=["darkseagreen" if burned else "lightsteelblue" for burned in G2.vs["burned"]],
#     edge_color=["darkseagreen" if burned else "black" for burned in G2.es["burned"]],
#     vertex_label=G2.vs["divisor"]
# )

# G2.vs["divisor"] = [2,1,1,1,1]
# G2.vs["color"] = [1,2,2,0,0]

# ig.plot(
#     G2,
#     target="housex_canon_postfire.png",
#     layout="auto",
#     vertex_color=["indianred" if color == 2 else "darkseagreen" if color == 1 else "lightsteelblue" for color in G2.vs["color"]],
#     edge_color=["darkseagreen" if burned else "black" for burned in G2.es["burned"]],
#     vertex_label=G2.vs["divisor"]
# )

