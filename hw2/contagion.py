# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
from graphs import create_fb_graph, create_graph
from random import randint

# 8 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.
def BRD(G, status, neighbors, q):
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
    node_change = {node : False for node in G.keys()}

    while (True):
        change = False
        for node, vals in G.items():
            # Early adopter, cannot change more than once during BRD
            if (node in S or node_change[node]):
                continue

            prev_status, neighbors = vals[0], vals[1]
            #update node behavior based on neighbors

            new_status = BRD(G, prev_status, neighbors, q)
            if (prev_status != new_status):
                G[node][0] = new_status
                changes += 1
                change = True
                node_change[node] = True

        # if no change, done with BRD
        if (change is False):
            break

    #return graph after brd and number of changes
    return G, changes


def print_graph(G):
    for node, vals in G.items():
        print(f"{node}: {vals[0]}", end=" ")
    
    print()


def verification_4_1():
    # Figure 4.1, first graph
    S = ['0', '1']
    filename = "graph_4_1_1.txt"

    # incomplete cascade
    print()
    q = 2/3
    g = create_fb_graph(S, filename)
    print(f"Original graph 4.1.1 (incomplete cascade), S={S}, q={q}")
    print_graph(g)
    g2, changes = contagion_brd(g, S, q)
    print(f"\n{changes} node switches {changes} after BRD")
    print_graph(g2)


    print("-" * 40)

    #complete cascade
    print()
    print(f"Original graph 4.1.1 (complete cascade), S={S}, q={q}")
    q = 1/3
    g = create_fb_graph(S, filename)
    print_graph(g)
    g2, changes = contagion_brd(g, S, q)
    print(f"\n{changes} node switches {changes} after BRD")
    print_graph(g2)

    # -------------------------------------------
    print()
    print("-" * 40)
    print("-" * 40)


    # FIGURE 4.1, second graph
    S = ['0', '3']
    q = 1/3
    filename = "graph_4_1_2.txt"

    # incomplete cascade
    print()
    print(f"\n Original graph 4.1.2 (incomplete cascade), S={S}, q={q}:")
    g = create_fb_graph(S, filename)
    print_graph(g)
    g2, changes = contagion_brd(g, S, q)
    print(f"\n{changes} node switches {changes} after BRD")
    print_graph(g2)

    print("-" * 40)
    #complete cascade
    print()
    q = 1/4
    print(f"\n Original graph 4.1.2 (complete cascade), S={S}, q={q}")
    g = create_fb_graph(S, filename)
    print_graph(g)
    g2, changes = contagion_brd(g, S, q)
    print(f"\n{changes} node switches {changes} after BRD")
    print_graph(g2)


def gen_random_S(amount_adopters):
    return [str(randint(0,4038)) for _ in range(amount_adopters)]

def graph_cascaded(graph):
    first = graph['0'][0]

    for _, vals in graph.items():
        if vals[0] != first:
            return False
    
    return True

def q8b():
    total_changes = 0
    q = 0.1

    change_record = []
    for i in range(100):
        if (i % 10 == 0):
            print(i)
        
        S = gen_random_S(10)
        g = create_fb_graph(S)
        g2, changes = contagion_brd(g, S, q)
        total_changes += changes
        cascaded = graph_cascaded(g2)
        change_record += [(changes, cascaded)]
    
    print(f"\nAverage amount of node switches: {total_changes/100}")
    print("\nChanges in each iteration:")
    print(change_record)

def q8c():
    qs = [0.05 * i for i in range(11)]
    amts_adopters = [10 * i for i in range(26)]

    change_record = []
    total_full_cascades = 0
    for q in qs:
        total_changes = 0
        print(f"Avg infection rate for q={q}: ", end="")
        for amt_adopters in amts_adopters:
            S = gen_random_S(amt_adopters)
            g = create_fb_graph(S)
            g2, changes = contagion_brd(g, S, q)
            total_changes += changes
            cascaded = graph_cascaded(g2)
            if cascaded:
                total_full_cascades += 1
            change_record += [(changes, cascaded)]
        print(total_changes/25)
    
    print(f"Full cascades: {total_full_cascades}")





if __name__ == "__main__":
    # q8b()
    q8c()
