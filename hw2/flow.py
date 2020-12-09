# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
MAX_FLOAT = float("Inf")
from random import randint
from matplotlib import pyplot as plt

def was_visited(G, s, t, paths, capacities): 
    vis = len(G) * [False]
    q =[] 
    q.append(s) 
    vis[s] = True
    while q: 
        curr = q.pop(0)
        for i in G[curr]: 
            if vis[i] == False and capacities[(curr, i)] > 0 : 
                q.append(i) 
                vis[i] = True
                paths[i] = curr

    return True if vis[t] else False

# 9 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.
def max_flow(G, s, t, c):
    paths = len(G) * [-1]
    max_flow = 0 

    pairs = []

    while was_visited(G, s, t, paths, c) : 

        path_flow = MAX_FLOAT
        sink = t
        while(sink !=  s): 
            path_flow = min(path_flow, c[(paths[sink],sink)]) 
            sink = paths[sink] 
        max_flow +=  path_flow 


        v = t 
     
        while(v !=  s): 
            u = paths[v] 
            c[(u, v)] -= path_flow 
            c[(v, u)] += path_flow 
            if (v != t) and (u != s): 
                pairs.append((u,v))
            v = paths[v] 

    return max_flow, pairs

# 9 (c)
# implement an algorithm that computes a maximum matching in a bipartite graph G
# Note: you may represent the bipartite graph however you want
def max_matching(G):
    graph = G[0]
    cap = G[1]
    res = max_flow(graph, 0, len(graph) - 1, cap)

    M = res[1]
    return M # a matching

# 9 (d)
# Now consider the case where there are n drivers and n riders, and the drivers each driver is connected to each rider with probability p.  
# Fix n=1000 (or maybe 100 if that’s too much), and estimate the probability that allnriders will get matched for varying values of p.  Plot your results.

def create_graph_np(p, n):
    print(p)
    n2 = n * 2 + 1
    G = {i : [] for i in range(1,n2)}
    G[0] = [i for i in range(1, n+1)]
    G[n2] = [i for i in range(n+1, n2)]

    c = dict()

    for i in range(1, n+1):
        c[0, i], c[i, 0] = 1, 0
        for j in range(n+1, n2):
            c[n2, j], c[j, n2] = 0, 1
            G[j] += [n2]
            if randint(0,100) / 100 < p:
                G[i] += [j]
                c[(i,j)], c[(j, i)] = 1, 0

    matches = max_matching((G,c))
    print(f"Matches:  {len(matches)}")
    return len(matches)





# c = {(0, 1): 1, (1,0): 0, (0,2): 3, (2,0): 0, (1, 2): 2, (2,1): 0, (2,3): 1, (3,2): 0, (1,3): 1, (3,1): 0}
# G = {0: [1,2], 1:[2,3], 2:[3], 3:[]}

# print("max flow for graph 6.1: {}".format(max_flow(G, 0, 3, c)[0]))

# G = {0: [1,2,3,4,5], 1:[7], 2: [6,7], 3:[6], 4:[8,10], 5:[8,9], 6:[11], 7:[11], 8:[11], 9:[11], 10:[11], 11:[]}
# c = {(0,1): 1, (1,0): 0, (0,2): 1, (2,0): 0, (0,3): 1, (3,0): 0, (0,4): 1, (4, 0): 0, (0, 5): 1, (5,0): 0,
#     (1, 7): 1,  (7,1): 0, (2, 6): 1, (6, 2): 0, (2, 7): 1, (7,2): 0, (3,6): 1, (6,3): 0, (4,8): 1, (8,4): 0, (4,10): 1, (10,4): 0, (5,8): 1, (8,5): 0, (5, 9): 1, (9,5): 0,
#     (6,11): 1, (11,6): 0, (7,11): 1, (11,7): 0, (8,11): 1, (11, 8): 0, (9, 11): 1, (11,9): 0, (10, 11): 1, (11,10): 0}

# print("max flow for graph 6.3: {}".format(max_flow(G, 0, 11, c)[0]))

# G = {0: [1,2,3,4,5], 1:[7], 2: [6,7], 3:[6], 4:[8,10], 5:[8,9], 6:[11], 7:[11], 8:[11], 9:[11], 10:[11], 11:[]}
# c = {(0,1): 1, (1,0): 0, (0,2): 1, (2,0): 0, (0,3): 1, (3,0): 0, (0,4): 1, (4, 0): 0, (0, 5): 1, (5,0): 0,
#     (1, 7): 1,  (7,1): 0, 
#     (2, 6): 1, (6, 2): 0, (2, 7): 1, (7,2): 0, 
#     (3,6): 1, (6,3): 0, 
#     (4,8): 1, (8,4): 0, (4,10): 1, (10,4): 0, 
#     (5,8): 1, (8,5): 0, (5, 9): 1, (9,5): 0,
#     (6,11): 1, (11,6): 0, 
#     (7,11): 1, (11,7): 0, 
#     (8,11): 1, (11, 8): 0, 
#     (9, 11): 1, (11,9): 0, 
#     (10, 11): 1, (11,10): 0}

# print("max bipartite for graph 6.3: {}".format(max_matching((G,c))))

# G = {0: [1,2,3,4,5], 1:[7], 2: [6,7,9], 3:[6,7,8], 4:[8,10], 5:[8,9], 6:[11], 7:[11], 8:[11], 9:[11], 10:[11], 11:[]}
# c = {(0,1): 1, (1,0): 0, (0,2): 1, (2,0): 0, (0,3): 1, (3,0): 0, (0,4): 1, (4, 0): 0, (0, 5): 1, (5,0): 0,
#     (1, 7): 1,  (7,1): 0, 
#     (2, 6): 1, (6, 2): 0, (2, 7): 1, (7,2): 0, (2,9): 1, (9,2): 0, 
#     (3,6): 1, (6,3): 0, (3,7): 1, (7,3): 0, (3,8): 1, (8,3): 0,
#     (4,8): 1, (8,4): 0, (4,10): 1, (10,4): 0, 
#     (5,8): 1, (8,5): 0, (5, 9): 1, (9,5): 0,
#     (6,11): 1, (11,6): 0, 
#     (7,11): 1, (11,7): 0, 
#     (8,11): 1, (11, 8): 0, 
#     (9, 11): 1, (11,9): 0, 
#     (10, 11): 1, (11,10): 0}

# print("max bipartite for example 2: {}".format(max_matching((G,c))))





ps = [0.1 * i for i in range(10)]
n = 500
matchings = [create_graph_np(p, n) for p in ps]

plt.figure(0)
plt.plot(ps, matchings)
plt.xlabel('Probability p')
plt.ylabel('Number of matches')
plt.grid(True)
plt.xlim(0, .9)
plt.title(f'Number of matches for {n} drivers/riders across varying probabilites')
plt.savefig('9d.png')

