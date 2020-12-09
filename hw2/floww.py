# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 9 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.

def bfs(G, s, t, parents):
    queue = [s]
    visited = [s]

    while queue != []:
        cur = queue[0]
        queue = queue[1:]

        for node, cap in enumerate(G[cur]):
            if node not in visited and cap > 0:
                queue.append(node)
                visited.append(node)
                parents[node] = cur

    if t in visited:
        return parents

    return None


#G is represented as a list of lists. 
#If an edge exists between two nodes (a,b), then G[a][b] will be the capacity of the edge, and 0 if no edge
def max_flow(G, s, t):
    parents = [-1]*len(G)
    maxFlow = 0

    parents = bfs(G, s, t, parents)

    while parents != None:
        curFlow = float("Inf")
        cur = t

        while(cur != s):
            curFlow = min(curFlow, G[parents[cur]][cur])
            cur = parents[cur]

        maxFlow += curFlow

        cur = t
        while(cur != s):
            prev = parents[cur]
            G[prev][cur] -= curFlow
            G[cur][prev] += curFlow
            cur = prev

        parents = bfs(G, s, t, parents)

    return maxFlow

# 9 (c)
# implement an algorithm that computes a maximum matching in a bipartite graph G
# Note: you may represent the bipartite graph however you want

#Assuming the graph already has s and t appending to either end
#m and n are the number of nodes in each partition of the bipartite graph
def max_matching(G, m, n):
    parents = [-1]*len(G)
    maxFlow = 0
    s = 0
    t = len(G) - 1

    parents = bfs(G, s, t, parents)

    while parents != None:
        curFlow = float("Inf")
        cur = t

        while(cur != s):
            curFlow = min(curFlow, G[parents[cur]][cur])
            cur = parents[cur]

        maxFlow += curFlow

        cur = t
        while(cur != s):
            prev = parents[cur]
            G[prev][cur] -= curFlow
            G[cur][prev] += curFlow
            cur = prev

        parents = bfs(G, s, t, parents)

    #Reverse edges formed between the n nodes and the m nodes in the matching. 
    #These can be found in the adjacency lists of the n nodes within the m positions

    M = []
    for node in range(m + 1, m + n + 1):
        node_adj = G[node][1: m + 1]

        if sum(node_adj) == 1:
            M.append((node_adj.index(1) + 1, node))

    return M # a matching

#graph 6.1
g1 = [
    [0, 1, 3, 0],
    [0, 0, 2, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]

#graph 6.3
g3 = [
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 100, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 100, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# x = max_flow(g1, 0, 3)
# print(x)

# x = max_flow(g3, 0, 11)
# print(x)

M = max_matching(g3, 5, 5)
print(M)