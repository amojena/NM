# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
MAX_FLOAT = float("Inf")

def was_visited(G, s, t, paths, capacities): 
    # initialize as all unvisited except source 
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
    # This array is filled by BFS and to store path 
    paths = len(G) * [-1]
    max_flow = 0 

    pairs = []

    # Augment the flow while there is path from source to sink 
    while was_visited(G, s, t, paths, c) : 

        # Find minimum residual capacity of the edges along the 
        # path filled by BFS. Or we can say find the maximum flow 
        # through the path found. 
        path_flow = MAX_FLOAT
        sink = t
        while(sink !=  s): 
            path_flow = min(path_flow, c[(paths[sink],sink)]) 
            sink = paths[sink] 

        # Add path flow to overall flow 
        max_flow +=  path_flow 

        # update residual capacities of the edges and reverse edges 
        # along the path 
        v = t 
     
        while(v !=  s): 
            u = paths[v] 
            c[(u, v)] -= path_flow 
            c[(v, u)] += path_flow 
            if (v != t) and (u != s): 
                pairs.append((u,v))
            v = paths[v] 

    if pairs:
        print("maximum bipartite matching: {}".format(pairs))
    return max_flow 

# 9 (c)
# implement an algorithm that computes a maximum matching in a bipartite graph G
# Note: you may represent the bipartite graph however you want
def max_matching(G):
    # return M # a matching
    pass


c = {(0, 1): 1, (1,0): 0, (0,2): 3, (2,0): 0, (1, 2): 2, (2,1): 0, (2,3): 1, (3,2): 0, (1,3): 1, (3,1): 0}
G = {0: [1,2], 1:[2,3], 2:[3], 3:[]}

print("max flow for graph 6.1: {}".format(max_flow(G, 0, 3, c)))

G = {0: [1,2,3,4,5], 1:[7], 2: [6,7], 3:[6], 4:[8,10], 5:[8,9], 6:[11], 7:[11], 8:[11], 9:[11], 10:[11], 11:[]}
c = {(0,1): 1, (1,0): 0, (0,2): 1, (2,0): 0, (0,3): 1, (3,0): 0, (0,4): 1, (4, 0): 0, (0, 5): 1, (5,0): 0,
    (1, 7): 1,  (7,1): 0, (2, 6): 1, (6, 2): 0, (2, 7): 1, (7,2): 0, (3,6): 1, (6,3): 0, (4,8): 1, (8,4): 0, (4,10): 1, (10,4): 0, (5,8): 1, (8,5): 0, (5, 9): 1, (9,5): 0,
    (6,11): 1, (11,6): 0, (7,11): 1, (11,7): 0, (8,11): 1, (11, 8): 0, (9, 11): 1, (11,9): 0, (10, 11): 1, (11,10): 0}

print("max flow for graph 6.3: {}".format(max_flow(G, 0, 11, c)))


G = {0: [1,2,3,4,5], 1:[7], 2: [6,7,9], 3:[6,7,8], 4:[8,10], 5:[8,9], 6:[11], 7:[11], 8:[11], 9:[11], 10:[11], 11:[]}
c = {(0,1): 1, (1,0): 0, (0,2): 1, (2,0): 0, (0,3): 1, (3,0): 0, (0,4): 1, (4, 0): 0, (0, 5): 1, (5,0): 0,
    (1, 7): 1,  (7,1): 0, (2, 6): 1, (6, 2): 0, (2, 7): 1, (7,2): 0, (3,6): 1, (6,3): 0, (4,8): 1, (8,4): 0, (4,10): 1, (10,4): 0, (5,8): 1, (8,5): 0, (5, 9): 1, (9,5): 0,
    (6,11): 1, (11,6): 0, (7,11): 1, (11,7): 0, (8,11): 1, (11, 8): 0, (9, 11): 1, (11,9): 0, (10, 11): 1, (11,10): 0, (2,9):1, (9,2): 0, (3,7): 1, (7,3): 0, (3,8): 1, (8,3): 0}

print("max flow for example 2: {}".format(max_flow(G, 0, 11, c)))
