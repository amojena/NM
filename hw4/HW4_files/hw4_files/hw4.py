# Please enter here the netids of all memebers of your group (yourself included.)
authors = ['am3238']

# Which version of python are you using? python 2 or python 3? 
python_version = "3"

# Important: You are NOT allowed to modify the method signatures (i.e. the arguments and return types each function takes).
from matplotlib import pyplot as plt
import networkx as nx
from collections import defaultdict

# Implement the methods in this class as appropriate. Feel free to add other methods
# and attributes as needed. 
# Assume that nodes are represented by indices between 0 and number_of_nodes - 1
class DirectedGraph:
    def __init__(self,number_of_nodes):
        self.num_of_nodes = number_of_nodes
        self.graph = dict()
        self.outedges = [0 for _ in range(self.num_of_nodes)]
        self.in_links = defaultdict(list)
    
    def add_edge(self, origin_node, destination_node):
        if self.check_edge(origin_node, destination_node):
            return
        if self.graph.get(origin_node) is None:
            self.graph[origin_node] = [destination_node]
        else:
            self.graph[origin_node].append(destination_node)

        self.outedges[origin_node] += 1
        self.in_links[destination_node].append(origin_node)
    
    def edges_from(self, origin_node):
        ''' This method shold return a list of all the nodes u such that the edge (origin_node,u) is 
        part of the graph.'''
        return self.graph[origin_node] if self.graph.get(origin_node) is not None else []

    def check_edge(self, origin_node, destination_node):
        ''' This method should return true is there is an edge between origin_node and destination_node
        and destination_node, and false otherwise'''
        return False if self.graph.get(origin_node) is None else destination_node in self.graph[origin_node]
    
    def number_of_nodes(self):
        ''' This method should return the number of nodes in the graph'''
        return self.num_of_nodes
    
    def in_link(self, destination_node):
        return self.in_links[destination_node]
    
def scaled_page_rank(graph, num_iter, eps = 1/7.0):
    ''' This method, given a directed graph, should run the epsilon-scaled page-rank
    algorithm for num-iter iterations and return a mapping (dictionary) between a node and its weight. 
    In the case of 0 iterations, all nodes should have weight 1/number_of_nodes'''  

    num_nodes = graph.number_of_nodes()
    nodeWeights = {node : 1 / num_nodes for node in range(num_nodes)}
    for _ in range(num_iter):
        prevWeights = nodeWeights.copy()
        for node in range(num_nodes):
            new_score = 0
            for edge in graph.in_link(node):
                #𝜖/n + (1 − 𝜖)∑ (v′,v)∈E Score(v′)/out-deg(v′), v' is node pointing to v
                new_score +=  prevWeights[edge] / graph.outedges[edge]
            nodeWeights[node] = (eps / num_nodes) + (1-eps) * new_score
            
    print(sum(nodeWeights.values()))
    return nodeWeights


def graph_15_1_left():
    ''' This method, should construct and return a DirectedGraph encoding the left example in fig 15.1
    Use the following indexes: A:0, B:1, C:2, Z:3 '''    
    g_15_1 = DirectedGraph(4)
    g_15_1.add_edge(3, 3) #z, z
    g_15_1.add_edge(0, 3) #a, z
    g_15_1.add_edge(0, 1) #a, b
    g_15_1.add_edge(1, 2) #b, c
    g_15_1.add_edge(2, 0) #c, a
    return g_15_1

def graph_15_1_right():
    ''' This method, should construct and return a DirectedGraph encoding the right example in fig 15.1
    Use the following indexes: A:0, B:1, C:2, Z1:3, Z2:4'''    
    g_15_1 = DirectedGraph(5)
    g_15_1.add_edge(3, 4) #z1, z2
    g_15_1.add_edge(4, 3) #z2, z1
    g_15_1.add_edge(0, 3) #a, z1
    g_15_1.add_edge(0, 4) #a, z2
    g_15_1.add_edge(0, 1) #a, b
    g_15_1.add_edge(1, 2) #b, c
    g_15_1.add_edge(2, 0) #c, a
    return g_15_1

def graph_15_2():
    ''' This method, should construct and return a DirectedGraph encoding example 15.2
        Use the following indexes: A:0, B:1, C:2, A':3, B':4, C':5'''
      
    g_15_2 = DirectedGraph(6)
    g_15_2.add_edge(0, 1) #a, b
    g_15_2.add_edge(1, 2) #b, c
    g_15_2.add_edge(2, 0) #c, a
    g_15_2.add_edge(3, 4) #a', b'
    g_15_2.add_edge(4, 5) #b', c'
    g_15_2.add_edge(5, 0) #c', a'
    return g_15_2

def extra_graph_1():
    ''' This method, should construct and return a DirectedGraph of your choice with at least 10 nodes'''    
    ex_g_1 = DirectedGraph(10)

    for i in range(4):
        ex_g_1.add_edge(i, 4)
        ex_g_1.add_edge(4, i)
    
    for i in range(6,10):
        ex_g_1.add_edge(i, 5)
        ex_g_1.add_edge(5, i)
        
    ex_g_1.add_edge(4, 5)
    ex_g_1.add_edge(5, 4)

    return ex_g_1
    

# This dictionary should contain the expected nodeWeights for each node when running the scaled page rank on the extra_graph_1 output
# with epsilon = 0.07 and num_iter = 20.
extra_graph_1_nodeWeights = {0: 0.05850659257528375, 1: 0.05834894986571982, 2: 0.05834894986571982, 3: 0.05834894986571982, 4: 0.2760696229339776, 5: 0.27569031648630987, 6: 0.05842509855392206, 7: 0.05827839886645363, 8: 0.05827839886645363, 9: 0.05827839886645363}

def extra_graph_2():
    ''' This method, should construct and return a DirectedGraph of your choice with at least 10 nodes'''    
    ex_g_2 = DirectedGraph(11)

    for i in range(4):
        ex_g_2.add_edge(i, 4)
        ex_g_2.add_edge(4, i)
    
    for i in range(6,10):
        ex_g_2.add_edge(i, 5)
        ex_g_2.add_edge(5, i)
        
    ex_g_2.add_edge(4, 5)
    ex_g_2.add_edge(5, 4)
    ex_g_2.add_edge(10, 4)
    ex_g_2.add_edge(10, 5)
    ex_g_2.add_edge(4, 10)
    ex_g_2.add_edge(5, 10)

    return ex_g_2

# This dictionary should contain the expected nodeWeights for each node when running the scaled page rank on the extra_graph_2 output
# with epsilon = 0.07 and num_iter = 20.
extra_graph_2_nodeWeights = {0: 0.048589372724965024, 1: 0.048445719917914604, 2: 0.048445719917914604, 3: 0.048445719917914604, 4: 0.27149731325340803, 5: 0.2712171002311596, 6: 0.04853916676349514, 7: 0.048402286899466095, 8: 0.048402286899466095, 9: 0.048402286899466095, 10: 0.09048437045374433}


def facebook_graph(filename = "facebook_combined.txt"):
    ''' This method should return a DIRECTED version of the facebook graph as an instance of the DirectedGraph class.
    In particular, if u and v are friends, there should be an edge between u and v and an edge between v and u.'''    
    with open(filename, 'r') as f:
        friendships = f.readlines()
    
    fb_graph = DirectedGraph(4039)
    for friendship in friendships:
        f1, f2 = friendship.split()
        fb_graph.add_edge(int(f1), int(f2))
        fb_graph.add_edge(int(f2), int(f1))
    return fb_graph



# The code necessary for your measurements for question 7b should go in this function.
# Please COMMENT THE LAST LINE OUT WHEN YOU SUBMIT (as it will be graded by hand and we do not want it to interfere
# with the automatic grader).
def question8b():
    
    fb_graph = facebook_graph()
    for n in range(10, 21):
        nw = scaled_page_rank(fb_graph, n)
        weights = [(node, fb_graph.outedges[node], weight) for node, weight in nw.items()]
        weights = sorted(weights, key=lambda x: x[2])
        

        outputToFile(weights, f"fb_{n}.txt")
    # weightScatterPlot(weights)
    makeNXGraph(fb_graph, weights)
    return nw

def outputToFile(weights, filename):
        ws = [f"{w[0]}, {w[1]}, {w[2]}\n" for w in weights]
        with open(filename, 'w') as fi:
            fi.writelines(ws)


def weightScatterPlot(weights):
    x, y = [], []
    for i, w in enumerate(weights):
        x.append(i)
        y.append(w[1])
    
    plt.figure(1)
    plt.scatter(x[: -100], y[: -100])
    plt.scatter(x[-100:], y[-100:], c="tab:red")
    plt.grid()
    plt.ylabel('Out-degree')
    plt.xlabel('Rank')
    plt.title('Relationship between rank and out-deg(v)')
    plt.savefig('out_weight.png')

def makeNXGraph(graph, weights):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(graph.number_of_nodes())])
    colors = ["b"] * 4039

    for i, w in enumerate(weights):
        if i > 3938:
            colors[w[0]] = "c"
        elif i < 300:
            colors[w[0]] = "r"

    for node, edges in graph.graph.items():
        for edge in edges:
            G.add_edge(node, edge)

    # plt.style.use('dark_background')
    plt.figure(2)
    nx.draw(G, width=.05, node_size=5, node_color = colors, with_labels=False)
    plt.savefig("graph.png")


#6a
# g15 = graph_15_1_left()
# print(g15.graph)
# nw = scaled_page_rank(g15, 10)
# print(nw)

# # print()

# g15 = graph_15_1_right()
# print(g15.graph)
# nw = scaled_page_rank(g15, 10)
# print(nw)

# 7b
question8b()
