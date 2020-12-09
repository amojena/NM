# Some helper functions for Part 5
# you may use these or define your own. Make sure it is clear where your solutions are
from matching_market import create_graph, matching_or_cset, market_eq, vcg
from random import randint
from matplotlib import pyplot as plt

# compute the manhattan distance between two points a and b (represented as pairs)
def dist(a,b):
    x0, y0 = a[0], a[1]
    x1, y1 = b[0], b[1]
    dist = abs(x0 - x1) + abs(y0 - y1)
    return dist

def stable_outcome(ndrivers, nriders, value=None, g_size=None):
    # riders / drivers: [loc, dest, value]
    riders  = [ ]
    for _ in range(nriders):
        temp_coord, dest_coord = getRandomXY(nriders), getRandomXY(nriders)

        # no two riders in the same coordinate
        while temp_coord in riders:
            temp_coord = getRandomXY(nriders)

        while dest_coord == temp_coord:
            dest_coord = getRandomXY(nriders)

        trip_dist = dist(dest_coord, temp_coord)

        if value is None:
            rider_val = randint(2*trip_dist, 4*trip_dist)
        else:
            rider_val = value

        riders += [(temp_coord, dest_coord, rider_val)]


    drivers = [ ]
    for _ in range(ndrivers):
        temp_coord = getRandomXY(ndrivers)

        # no two drivers in the same coordinate
        while temp_coord in riders:
            temp_coord = getRandomXY(ndrivers)

        drivers += [temp_coord]


    driver_vals = []
    for driverPos in drivers:
        temp_dists = []
        for riderPos, riderDest, _ in riders:
            d_val = dist(riderPos, driverPos) + dist(riderDest, riderPos)
            temp_dists.append(d_val)
        driver_vals.append(temp_dists)



    print(f"VCG: {ndrivers} drivers, {nriders} riders")
    res = vcg (ndrivers, nriders, driver_vals, g_size)
    print("Prices: ", res[0], ", Matches: ", res[1])


    M = [(driver, res[1][driver]) for driver in range(ndrivers)]
    a = {}

    for driver, rider in M:
        rider_index = rider - ndrivers - 1
        if rider_index >= 0:
            a[(driver, rider)] = riders[rider_index][2] - driver_vals[driver][rider_index]

    return (M,a)


def getRandomXY(n):
    return (randint(0, n), randint(0, n))

def print_stable_outcome(M, a):
    for driver, rider in M:
        if rider != -1:
            print(f"Matched {(driver, rider)} - allocation: {a[(driver, rider)]}")


## 11.a
# print("Test 1:")
# M, a = stable_outcome(5, 5)
# print_stable_outcome(M,a)

# print("-" * 10)
# print()

# print("Test 2:")
# M, a = stable_outcome(randint(5, 10), randint(5, 10))
# print_stable_outcome(M,a)


## 11.b (make scatter plot for this?)

# r = d
x, y = [], []
for _ in range(10):
    rd = 10
    M, a = stable_outcome(rd, rd, 100, 100)
    print_stable_outcome(M,a)
    vals = [b[1] for b in a.items()]
    x.extend([10] * len(vals))
    y.extend(vals)
    print()
    print()

plt.scatter(x, y, c="tab:blue", label="10 drivers, 10 riders")

# r << d
x, y = [], []
for _ in range(10):
    r = 5
    d = 20
    M, a = stable_outcome(d, r, 100, 100)
    print_stable_outcome(M,a)
    vals = [b[1] for b in a.items()]
    x.extend([20] * len(vals))
    y.extend(vals)
    print()
    print()

plt.scatter(x, y, c="tab:green", label="20 drivers, 5 riders")

# r >> d
x, y = [], []
for _ in range(10):
    r = 20
    d = 5
    M, a = stable_outcome(d, r, 100, 100)
    print_stable_outcome(M,a)
    vals = [b[1] for b in a.items()]
    x.extend([5] * len(vals))
    y.extend(vals)
    print()
    print()

    
plt.scatter(x, y, c="tab:orange", label="5 drivers, 20 riders")

plt.grid()
plt.title('Allocation after running VCG with different number of rider and drivers')
plt.legend()
plt.xlabel("# of drivers")
plt.ylabel("Allocation")
plt.savefig("11b.png")
