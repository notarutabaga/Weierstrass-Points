import test_cases as test
from weierstrass import *
import igraph as ig
import matplotlib.pyplot as plt

ig.config["plotting.backend"] = "matplotlib"
ig.config["plotting.layout"] = "auto"
ig.config.save()

graphs = []

G = test.housex()

# iterate through the list of graphs
for g_index, G in enumerate(graphs):
    g = genus(G)

    # check each vertex of the current graph
    for v in G.vs:
        print("vertex " + str(v.index) + ":")
            
        # reset the divisor
        G.vs["divisor"] = 0
            
        # color the weierstrass vertices
        if is_weierstrass(G, v.index):
            G.vs[v.index]["weier"] = True
                
        # ranks = []
                
        # # want to test divisors n(v) for 0 <= n <= 2g-2 (and then a couple more)
        # for n in range((2 * g) + 2):
        #     # D(v) = n
        #     G.vs[v.index]["divisor"] = n 
                    
        #     # compute r(nv) and add it to the list
        #     r = rank(G, v.index, g)
        #     ranks.append(r)
                
        # # output all of the information
            
        # print("n: ", end="")
        # for n in range(len(ranks)):
        #     print(n, end="\t")
                
        # print()
        # print("r: ", end="")
        # for r in ranks:
        #     print(r, end="\t")
                
        # print()
                
        # # compute gap sequence and weight if it is weierstrass
        # if G.vs[v.index]["weier"]:
        #     gap_seq = compute_gap_seq(ranks)
        #     w = weight(gap_seq, g)
                
        #     print("gap seq = " + str(gap_seq))
        #     print("weight = " + str(w))
                    
        # print()
        
    # save graph
    
    # fig, ax = plt.subplots(figsize=(5,5))
    
    # formatted_labels = [f'$v_{{{str(v.index + 1)}}}$' for v in G.vs]

    # # assign the labels to the vertices
    # G.vs['label'] = formatted_labels
    
    ig.plot(
        G,
        target=str(g_index)+".png",
        layout="auto",
        vertex_color=["limegreen" if weierstrass else "lightsteelblue" for weierstrass in G.vs["weier"]],
        vertex_label=[v.index for v in G.vs]
    )
    
    # print()
        