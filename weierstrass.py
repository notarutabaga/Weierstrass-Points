import igraph as ig
import dhars as dh
from itertools import combinations_with_replacement, permutations

def get_combinations(num_chips, array_size):
    numbers = range(num_chips + 1)
    combinations = list(combinations_with_replacement(numbers, array_size))
    result = []
    
    for combo in combinations:
        if sum(combo) == num_chips:
            result.append(combo)

    return result

def get_permutations(combinations):
    combo_perms = []

    for combo in combinations:
        combo_perms.extend(list(set(permutations(combo))))

    return combo_perms

def permute(num_chips, array_size):
    combinations = get_combinations(num_chips, array_size)
    permutations = get_permutations(combinations)
    
    return permutations

def genus(G):
    return G.ecount() - G.vcount() + 1

def weight(gap_seq, g):
    return sum(gap_seq) - ((g * (g + 1)) / 2)

# returns the degree of the divisor (ie sum of chips distrtibuted)
def degree(divisor):
    return sum(divisor)

# an effective divisor has all chips >= 0 (ie all are not in debt)
def is_effective(divisor):
    for div in divisor:
        if div < 0: 
            return False 
    
    return True

def canonical(G):
    canon_divisor = []
    
    for v in G.vs:
        canon_divisor.append(G.degree(v) - 2)
        
    return canon_divisor

def rank(G, index):
    deg = degree(G.vs["divisor"])
    g = genus(G)
    
    # case 1
    if deg < 0:
        print("case 1")
        return -1
    
    # case 2
    if deg >= (2 * g) - 1:
        print("case 2")
        return deg - g 
    
    r = 0
    
    # case 3
    if g <= deg and deg <= (2 * g) - 2:
        print("case 3")
        KG = G.copy()
        KG.vs["divisor"] = canonical(G)        
        
        G_diff = G.copy()
        
        div_diff = []
        for d1, d2 in zip(KG.vs["divisor"], G.vs["divisor"]):
            div_diff.append(d1 - d2)
        
        G_diff.vs["divisor"] = div_diff
        
        # get the rank of the difference
        r = rank(G_diff, index)
        
        return r + deg - g + 1
    
    # case 4 (please refactor, this is so ugly)
    
    # k = 0
    # computing = True
    
    # while computing:
    #     # list of all possible configurations of k chips
    #     perms = permute(k, G.vcount())
        
    #     # check if all configurations still give an effective divisor
    #     for perm in perms:
    #         perm = list(perm)
            
    #         G_copy = G.copy()
    #         diff = [] 
            
    #         # subtract current configuration from divisor
    #         for v1, v2 in zip(G.vs["divisor"], perm):
    #             diff.append(v1 - v2)
            
    #         G_copy.vs["divisor"] = diff 
            
    #         # determine effectiveness via dhar's
    #         effective = dh.dhars_burning(G_copy)
            
    #         # if even one config of k is not effective, the rank is k-1
    #         if not effective:
    #             return k - 1
        
    #     # increment k if all configs are effective
    #     k += 1
    
    k = -1
    effective = True
    
    # determine if removing k chips preserves effectiveness
    while effective:
        k += 1
        perms = permute(k, G.vcount())
        
        for perm in perms:
            perm = list(perm)
            
            G_copy = G.copy()
            diff = []
            
            # subtract current configuration from divisor
            for v1, v2 in zip(G.vs["divisor"], perm):
                diff.append[v1 - v2]
            
            G_copy.vs["divisor"] = diff 
            
            # stop testing permutations once one breaks effectiveness
            effective = dh.dhars_burning(G_copy)
            if not effective:
                break
    
    # once a configuration of k fails, its rank is k-1
    return k - 1
 
# REMOVE FOR PAPER    
# weierstrass point p is normal iff its gap sequence is {1, 2, ..., g-1, g+1}
def is_normal(gap_seq, g):
    # make the normal gap sequence for the given g
    normal = set()
    for i in range(1, g - 1):
        normal.append(i)
    normal.append(g + 1)
    
    # check to see if they are equal (gap_seq may be a list and order of items doesn't matter)
    return set(gap_seq) == normal

# v is weierstrass iff K_G - gv is effective
def is_weierstrass(G, index):
    # g = genus(G)
    
    # G_copy = G.copy()
    # G_copy.vs["divisor"] = 0
    # G_copy.vs[index]["divisor"] = g 
    
    # if rank(G_copy, index, g) >= 1:
    #     return True 
    
    # return False
    KG = G.copy()
    KG.vs["divisor"] = canonical(G)        
    
    # G_diff = G.copy()
    
    # div_diff = []
    # for d1, d2 in zip(KG.vs["divisor"], G.vs["divisor"]):
    #     div_diff.append(d1 - d2)
    
    # G_diff.vs["divisor"] = div_diff
    KG.vs[index]["divisor"] = KG.vs[index]["divisor"] - genus(G)
    
    return dh.dhars_burning(KG)

# REMOVE FOR PAPER 
def compute_gap_seq(ranks):
    gap_seq = []
    
    for i in range(1, len(ranks)):
        if ranks[i] == ranks[i - 1]:
            gap_seq.append(i)
    
    return gap_seq        