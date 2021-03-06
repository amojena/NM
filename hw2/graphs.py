import random

def add_node(graph, node, S):
    if graph.get(node) is None:
        graph[node] = [node in S, []]

def add_edge(graph, n1, n2):
    graph[n1][1] += [n2]
    graph[n2][1] += [n1]

# Question 9.a
def create_fb_graph(S, filename="facebook_combined.txt"):

    with open(filename) as f:
        lines = f.readlines()

    # {node : [
    #   bool, 
    #   [ neighbors(int) ] 
    #   ] }    
    graph = dict()

    for line in lines:
        nodes = line.split()
        n1, n2 = nodes[0], nodes[1]

        add_node(graph, n1, S)
        add_node(graph, n2, S)

        add_edge(graph, n1, n2)
    
    # print(graph)
    return graph


def create_graph(network, S):
    graph = dict()
    for node, neighbors in network.items():
        add_node(graph, node, S)

        for neighbor in neighbors:
            add_node(graph, neighbor, S)
            add_edge(graph, node, neighbor)

    return graph