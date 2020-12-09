# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 7 (a)
# implement an algorithm that given a bipartite graph G, outputs
# either a perfect matching or a constricted set
# Note: this will be used in 7 (b) so you can implement it however you
# like
import random
from matplotlib import pyplot as plt

MAX_FLOAT = float("Inf")
MAX_INT = MAX_FLOAT
def was_visited(G, s, t, paths, capacities): 
    vis = len(G) * [False]
    q =[] 
    q.append(s) 
    vis[s] = True
    # print(G)
    while q: 
        curr = q.pop(0)
        for i in G[curr]: 
            if vis[i] == False and capacities[(curr, i)] > 0 : 
                q.append(i) 
                vis[i] = True
                paths[i] = curr

    return True if vis[t] else False

def matching_or_cset(c, prices, values, n,m, G):
    s = 0
    t = n + m + 1
    op_size = n + 1
    max_flow = 0 
    pairs = []
    # new_vals = {}
    pref_pairings = {}
    for key,vals in values.items():
        new_vals = [a_i - b_i for a_i, b_i in zip(vals, prices)]
        max_val = max(new_vals)
        indices = [i + op_size for i, j in enumerate(new_vals) if j == max_val]
        #record their preferences for figuring out the inset later 
        pref_pairings[key] = indices
        G[key] = []
        for ind in indices:
            end = ind
            c[(key, end)] = max_val
            c[(s, key)] = max_val
            G[s].append(key)
            G[key].append(end)
            G[end].append(t)
            if (end,t) in c:
                c[(end,t)] = max(max_val, c[(end,t)])
            c[(end, t)] = max_val    

    paths = len(G) * [-1]
    while was_visited(G, s, t, paths, c) : 

        path_flow = MAX_FLOAT
        sink = t
        while(sink !=  s): 
            path_flow = min(path_flow, c[(paths[sink],sink)]) 
            sink = paths[sink] 
        max_flow +=  path_flow 


        v = t 
     
        while(v !=  s): 
            # print("CURR PAIR IS: {}".format((u,v)))
            u = paths[v] 
            c[(u, v)] = 0 
            c[(v, u)] += path_flow 
            if (v != t) and (u != s): 
                pairs.append((u,v))
            # if (u == t):
            #     path_flow = 0
            v = paths[v] 

    return pairs, pref_pairings

# 7 (b)
# implement an algorithm that given n (the number of players and items,
# which you can assume to just be labeled 0,1,...,n-1 in each case),
# and values where values[i][j] represents the ith players value for item j,
# output a market equilibrium consisting of prices and matching
# (p,M) where player i pays p[i] for item M[i]. 

def create_graph(size):
    c = {}
    G = {}
    for i in range(size):
        G[i] = []
        for j in range(i, size):
            c[(i,j)] = 0
            c[(j,i)] = 0
    return G, c

def market_eq(n, m, values, g_size=None):

    vals = {}
    for i in range(len(values)):
        vals[i + 1] = values[i]
    
    
    prices = [0]*n
    if g_size is None:
        G, c = create_graph(n + m + 2)
    else:
        G, c = create_graph(g_size + 2)

    pairs = []
    count = 0
    last_len = 0
    while len(pairs) < min(n, m):
        pairs, prefs = matching_or_cset(c, prices,vals, n, m, G)
        inset = []
        got_paired = []
        visited = set()
        new_pairs = []
        #remove any potential duplicates
        for a, b in pairs: 
            if not b in visited: 
                visited.add(b) 
                new_pairs.append((a, b))   
        pairs = new_pairs
        if len(pairs) < last_len:
            for i in range(len(prices)):
                if (n + 1 + i) in inset:
                    prices[i] -= 1    
            break
        last_len = len(pairs)
        for pair in pairs:
            got_paired.append(pair[0])
        #figure out which items weren't paired and where they could've been to build the inset
        for key, val in prefs.items():
            if key not in got_paired:
                inset = inset + val
        #dedupe inset       
        inset = list(dict.fromkeys(inset))

        #increment prices in inset
        for i in range(len(prices)):
            if (n + 1 + i) in inset:
                prices[i] += 1

        count += 1
    p = [0]*n
    M = [-1]*n
    for pair in pairs: 
        i = pair[0] - 1

        p[i] = prices[pair[1] - n - 1]
        M[i] = pair[1]

    while 0 not in p:
        for i in range(n):
            p[i] -= 1

    return (p,M)

# 8 (b)
# Given n players 0,...,n-1 and m items 0,...,m-1 and valuations
# values such that values[i][j] is player i's valuation for item j,
# implement the VCG mechanism with Clarke pivot rule that outputs
# a set of prices and assignments (p,M) such that player i pays p[i]
# (which should be positive) for item M[i].
def vcg(n, m, values, g_size=None):
    # print("VALUES: {}".format(values))
    (p_star,M_star) = market_eq(n, m, values)
    # print("BACK INTO VCG")
    # print("MSTAR: {} AND P STAR: {}".format(M_star, p_star))
    # print(len(values))
    p = [0]*n
    M = [-1]*n
    new_vals = values.copy()
    for i in range (n):
        del new_vals[i]
        (p, M) = market_eq(n-1, m, new_vals, g_size)
        p.insert(i, 0)
        M.insert(i, 0)
        
        item_ind = max(M_star[i] - n -1, -1)

        ext_with = 0
        ext_without = 0
        for j in range(n):
            if j != i:
                temp_val =0
                actual_val = 0
                actual_item_ind = max(M_star[j] - n -1, -1)

                if item_ind == -1:
                    temp_val = 0
                else:
                    temp_val = values[j][item_ind]

                if actual_item_ind == -1:
                    actual_val = 0
                else:
                    actual_val = values[j][actual_item_ind]
                
                ext_with += actual_val
                ext_without += max(actual_val, temp_val) 
    
        p[i] = ext_without - ext_with

        new_vals = values.copy()


    M = M_star
    return (p,M)
    

#7a,b
prices = [0,3,2]
values = {1: [4,12,5], 2:[7,10,9], 3:[7,7,10]}
c = {(0, 1): 12, (1,0): 0, (0,2): 10, (2,0): 0, (0,3):0, (3,0):0, (1, 4): 0, (4,1):0, (1,5):0, (5,1):0, (1,6):0, (6,1):0,(2,4): 0,(4,2):0, (2,5):0, (5,2):0, (2,6):0, (6,2):0, (3,4):0, (4,3):0, (3,5):0, (4,7):0, (7,4):0, (5,3):0, (3,6):0, (6,3): 0, (5,7): 0, (7,5): 0, (6,7): 0, (7,6):0}
G = {0: [1,2,3], 1:[4,5,6], 2:[4,5,6], 3:[4,5,6], 4:[7], 5:[7], 6:[7], 7:[]}

##7a
res, _ = matching_or_cset(c, prices, values, 3,3, G)
print("RESULTS: {}".format(res))




##7b
# values = [[4,12,5], [7,10,9], [7,7,10]]
# res = market_eq(3, 3,values)
# res_vcg = vcg(3,3,values)
# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))


# values = [[4,12,5, 6,8], [7,10,9,7,4], [7,7,10, 12, 10], [5,6,9,6,6], [7,12,4,4,7]]
# res = market_eq(5, 5,values)
# res_vcg = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))

# values = [[18,19,16,19,18], [8,7,4,7,6],[10,9,6,9,6],[8,9,6,9,8],[8,9,12,9,12]]
# res = market_eq(5, 5,values)
# res_vcg = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))

# values = [[5,8,10,6,11], [10,7,9,9,6],[7,4,6,6,3],[7,4,6,6,3],[4,1,3,3,2]]
# res = market_eq(5, 5,values)
# res_vcg = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))

# values= [[2,4,2,4,2,4,2,4,2,4], [1,3,5,7,9,8,7,6,4,2], [12,21,3,14,5,4,7,7,8,0],[1,20,3,14,5,16,7,18,9,0], [1,1,3,9,9,6,6,3,8,2], [1,1,3,9,9,6,6,3,8,2],[1,1,2,12,7,6,6,3,4,2], [1,3,5,7,9,8,7,6,4,2], [1,2,3,4,5,6,7,9,8,0,4], [8,2,11,12,4,4,4,8,12,5]]
# res = market_eq(10, 10,values)
# res_vcg = vcg(10,10,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))


##8b

# values = [[4,12,5], [7,10,9], [7,7,10]]
# res = vcg(3,3,values)
# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))


# values = [[4,12,5, 6,8], [7,10,9,7,4], [7,7,10, 12, 10], [5,6,9,6,6], [7,12,4,4,7]]
# res = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))

# values = [[18,19,16,19,18], [8,7,4,7,6],[10,9,6,9,6],[8,9,6,9,8],[8,9,12,9,12]]
# res = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))

# values = [[5,8,10,6,11], [10,7,9,9,6],[7,4,6,6,3],[7,4,6,6,3],[4,1,3,3,2]]
# res = vcg(5,5,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))


# values= [[2,4,2,4,2,4,2,4,2,4], [1,3,5,7,9,8,7,6,4,2], [12,21,3,14,5,4,7,7,8,0],[1,20,3,14,5,16,7,18,9,0], [1,1,3,9,9,6,6,3,8,2], [1,1,3,9,9,6,6,3,8,2],[1,1,2,12,7,6,6,3,4,2], [1,3,5,7,9,8,7,6,4,2], [1,2,3,4,5,6,7,9,8,0,4], [8,2,11,12,4,4,4,8,12,5]]
# res = vcg(10,10,values)

# print("VALUES: {}".format(values))
# print("RESULT: {}".format(res))



# ####
# ##P9
# ######

# amounts = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
# values = []
# for i in range(20):
#     rand_val = random.randint(1,50)
#     values.append([element * rand_val for element in amounts])


# res_vcg = vcg(20,20,values)

# print("VALUES: {}".format(values[0]))
# print("RESULT: {}".format(res_vcg))
