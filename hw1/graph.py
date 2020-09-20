# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import random

def add_node(graph, node):
    if graph.get(node) is None:
        graph[node] = []

def add_edge(graph, n1, n2):
    graph[n1] += [n2]
    graph[n2] += [n1]

# given number of nodes n and probability p, output a random graph 
# as specified in homework
def create_graph(n,p):
    graph = dict()

    for i in range(n):
        add_node(graph, i)
        for j in range(i + 1, n):
            add_node(graph, j)

            if (random.uniform(0,1) <= p):
                add_edge(graph, i, j)
    
    return graph

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G,i,j):
    queue = [[i]]
    seen = []

    if i == j:
        return 0

    #bfs
    while len(queue) > 0:
        path = queue.pop(0) #FIFO
        node = path[-1] #get last node from current path

        # move on if we've seen this node already
        if node in seen:
            continue

        for edge in G[node]:
            # add unseen node to current path
            newPath = path + [edge]
            # add updated path to queue
            queue += [newPath]
            # if the node we just added is the target node, return the length of the new path
            if edge == j:
                return len(newPath)
        
        seen += [node]
    
    # disconnected graph
    return "infinity"

# Question 8.c
def c8(graph=create_graph(1000, .1), filePath="avg_shortest_path.txt", maxNode = 999):
    n, p = 1000, .1
    outputFile = open(filePath, "w")
    
    total = 0
    print("Finding shortest paths...")
    for r in range(1000):
        print("Round {}...".format(r))
        i, j = random.randint(0, maxNode), random.randint(0, maxNode)
        while i == j:
            j = random.randint(0, maxNode)
    
        pathLength = shortest_path(graph, i, j)
        outputFile.write("({}, {}, {})\n".format(i, j, pathLength))
        total += pathLength
    
    print("Closing output file...")
    outputFile.close()
    print("Graph with {} nodes connected with p = {} has average path length of {}".format(n, p, total/1000))

# Question 8.d
def plot():
    import matplotlib.pyplot as plt

    with open("varying_p.txt", "r") as f:
        lines = f.readlines()
    
    x, y = [], []
    for line in lines:
        l = line.split(",")
        x += [ float(l[0]) ]
        y += [ float(l[1]) ]
    

    plt.title("Average path length of 1000-node graph with varying p")
    plt.xlabel("p")
    plt.ylabel("Average path length")
    plt.plot(x, y, '-o')
    plt.show()

def varyingPs():
    
    ps = [.01 * i for i in range(1,10)] + [.05 * i for i in range(2, 10)]
    
    n = 1000
    filePath = "varying_p.txt"
    outputFile = open(filePath, "w")
    
    
    for p in ps:
        print(f"Finding shortest path for p = {p}...")
        graph = create_graph(n, p)
        total = 0
        for _ in range(1000):
            i, j = random.randint(0, 999), random.randint(0, 999)
            while i == j:
                j = random.randint(0, 999)

            total += shortest_path(graph, i, j)

        outputFile.write("{}, {}\n".format(p, total/1000))
    
    print("Closing output file...")
    outputFile.close()
    plot()


# Question 9.a
def createFBGraph():
    with open("facebook_combined.txt") as f:
        lines = f.readlines()
    
    graph = dict()

    for line in lines:
        nodes = line.split()
        n1, n2 = int(nodes[0]), int(nodes[1])

        add_node(graph, n1)
        add_node(graph, n2)

        add_edge(graph, n1, n2)
    
    return graph
    
if __name__ == "__main__":
    g = createFBGraph()
    c8(g, "fb_shortest_path.txt", 4038)
