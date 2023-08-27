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

def complete(n):
    G = Graph.Full(n)
    
    G.vs["divisor"] = 0
    
    G.vs["burned"] = False
    G.es["burned"] = False  
    
    return G 

def compl_bipart(n, m):
    G = new_graph([], 0)
    G.add_vertices(n + m)

    for i in range(n):
        for j in range(m):
            G.add_edge(i, n + j)
            
    return G

# G1 = housex()
# G1.vs["divisor"] = [5, 2, -3, -1, 3]

# G2 = housex()
# G2.vs["divisor"] = canonical(G2)

# fig, ax = plt.subplots(figsize=(5,5))
    
# formatted_labels = [f'$v_{{{str(v.index + 1)}}}$' for v in G1.vs]

# # Assign the labels to the vertices
# G1.vs['label'] = formatted_labels
    
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