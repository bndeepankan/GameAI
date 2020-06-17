from GameAI.problems07.make_graph import *
import numpy as np
import networkx as nx


def test_a_star(G, src, t):
    path = nx.astar_path(G, src, t, heuristic=findDist, weight='distance')
    return path


def findDist(u, v):
    xi = u
    xj = v
    return np.sqrt(np.sum((xi - xj) ** 2))


def a_star(G, src, t):
    closed = []
    fringe = [src]
    g = {}
    f = {}
    h = {}
    g[src] = 0
    h[src] = findDist(np.array(G.nodes[src]['location']), np.array(G.nodes[t]['location']))
    f[src] = g[src] + h[src]
    path = {}

    while fringe:
        curr = fringe[0]
        for i in fringe:
            if f[curr] > f[i]:
                curr = i
        u = curr
        if u == t:
            break

        closed.append(u)
        fringe.remove(u)

        for v in [x for x in G.neighbors(u)]:
            if v not in closed:
                _g = g[u] + G[u][v]['distance']
                if v not in fringe or (v in g and g[v] > _g):
                    g[v] = _g
                    h[v] = findDist(np.array(G.nodes[v]['location']), np.array(G.nodes[t]['location']))
                    f[v] = g[v] + h[v]
                    path[v] = u
                    if v not in fringe:
                        fringe.append(v)

    return g, path


def shortestPath(path, src, t):
    p = []
    while t != src:
        p.append(t)
        t = path[t]
    p.append(t)
    return p


if __name__ == '__main__':

    f = open('simple-map-1.txt', 'r')
    graph = []

    for i in f:
        graph.append(i.rstrip().split(' '))

    graph = np.array(graph)
    graph = np.rot90(np.rot90(np.rot90(graph)))

    obj = makeGraph()
    obj.create_graph(graph)

    graph = obj.build_nx_graph(obj.succDict, obj.nodeDict)
    src = obj.mapVal[(1, 8)]
    t = obj.mapVal[(14, 8)]
    dist, path = a_star(graph, src, t)

    spath = shortestPath(path, src, t)

    print('Shortest path from source to destination')
    print(spath[::-1])

    print('\nShortest path from source to destination using networkx function')
    print(test_a_star(graph, src, t))
