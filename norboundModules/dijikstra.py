from collections import defaultdict

topo3 = {
    1: {1: 0, 2: 133, 3: float('inf'), 4: 64, 5: float('inf')},
    2: {1: 133, 2: 0, 3: float('inf'), 4: float('inf'), 5: 64},
    3: {1: float('inf'), 2: float('inf'), 3: 0, 4: 64, 5: 133},
    4: {1: 64, 2: float('inf'), 3: 64, 4: 0, 5: float('inf')},
    5: {1: float('inf'), 2: 64, 3: 133, 4: float('inf'), 5: 0}
}

adjacency = defaultdict(lambda: defaultdict(lambda: None))
switch = set(topo3)


def minimum_distance(Q, distance):
    min_value = float('inf')
    node = 0
    for v in Q:
        if distance[v] < min_value:
            min_value = distance[v]
            node = v
    return node


def dijkstra(graf, src, dst):
    Q = set(graf)
    distance = {}
    previous = {}

    for i in Q:
        distance[i] = float('Inf')
        previous[i] = None

    distance[src] = 0

    while len(Q) > 0:
        u = minimum_distance(Q, distance)
        Q.remove(u)

        for p in Q:
            if graf[u][p] != float('inf'):  # it means they're directly connected
                if distance[p] > distance[u] + graf[u][p]:
                    distance[p] = distance[u] + graf[u][p]
                    previous[p] = u

    r = []
    p = dst
    r.append(p)
    q = previous[p]
    while q is not None:
        if q == src:
            r.append(q)
            break
        p = q
        r.append(p)
        q = previous[p]
    r.reverse()
    if src == dst:
        path = [src]
        distance[src] = graf[src][dst]
    else:
        path = r

    print("Shortest path from", src, "to", dst, ":", path, "Cost =", distance[dst])


def main():
    for src in switch:
        for dst in switch:
            dijkstra(topo3, src, dst)


if __name__ == "__main__":
    main()
