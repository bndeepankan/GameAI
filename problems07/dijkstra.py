from GameAI.problems07.make_graph import *
import numpy as np
import networkx as nx


def test_dijkstra(G, src, t):
    path = nx.dijkstra_path(G, src, t, weight='distance')
    return path


def dijkstra(G, src, t):
    closed = []
    fringe = [src]
    dist = {}
    path = {}
    for i in G.nodes():
        path[i] = -1
        if i == src:
            dist[i] = 0
        else:
            dist[i] = float('inf')
    while fringe:
        curr = fringe[0]
        for d in fringe:
            if d not in closed and dist[curr] > dist[d]:
                curr = d
        u = curr
        closed.append(u)
        fringe.remove(u)
        for v in [x for x in G.neighbors(u)]:
            if v not in closed:
                if v not in fringe:
                    fringe.append(v)
                if dist[v] > dist[u] + G[u][v]['distance']:
                    dist[v] = dist[u] + G[u][v]['distance']
                    path[v] = u

        if u == t:
            break

    return dist, path


def dijkstraShortestPath(path, src, t):
    p = []
    while path[t] != -1 and t != src:
        p.append(t)
        t = path[t]
    p.append(t)
    return p


if __name__ == '__main__':

    f = open('simple-map-2.txt', 'r')
    graph = []

    for i in f:
        graph.append(i.rstrip().split(' '))

    graph = np.array(graph)
    graph = np.rot90(np.rot90(np.rot90(graph)))

    obj = makeGraph()
    obj.create_graph(graph)  # Create labels and the location of the graph

    graph = obj.build_nx_graph(obj.succDict, obj.nodeDict)     # Create the graph from the labels and location
    src = obj.mapVal[(0, 4)]
    t = obj.mapVal[(14, 19)]
    dist, path = dijkstra(graph, src, t)

    spath = dijkstraShortestPath(path, src, t)

    for i in dist:
        if dist[i] < float('inf'):
            print("Distance of Node %s from source is: " % i, dist[i])

    print('\nShortest distance from source to destination')
    print(spath[::-1])
    print('\nShortest distance from source to distance using networkx function')
    print(test_dijkstra(graph, src, t))
