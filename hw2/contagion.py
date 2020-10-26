# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
from graphs import create_fb_graph

# 8 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.
def get_node_status(G, status, neighbors, q):
    different = 0
    new_status = status

    for neighbor in neighbors:
        if (G.get(neighbor)[0] != status):
            different += 1
            new_status = G.get(neighbor)[0]
    
    density = different / len(neighbors)
    return new_status if (density > q) else status
    
def contagion_brd(G, S, q):
    changes = 0

    while (True):

        change = False
        for node, vals in G.items():

            # Early adopter, cannot change during BRD
            if (node in S):
                continue

            prev_status, neighbors = vals[0], vals[1]

            #update node behavior based on neighbors
            G[node][0] = get_node_status(G, prev_status, neighbors, q)

            if (prev_status != G[node][0]):
                changes += 1

                # do brd again
                change = True
                    
        
        # if no change, done with BRD
        if (change is False):
            break

    #return graph after brd and number of changes
    return G, changes

def print_graph(G):
    for node, vals in G.items():
        print(f"{node}: {vals[0]}", end=" ")
    
    print()

if __name__ == "__main__":
    S = [0, 3]
    q = 1/3

    print()
    print(f"q: {q}")

    filename = "test_graph.txt"
    g = create_fb_graph(S, filename)
    print_graph(g)

    g2, changes = contagion_brd(g, S, q)
    print_graph(g2)