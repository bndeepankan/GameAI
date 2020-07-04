from GameAI.problems07.make_graph import *
from GameAI.problems07.dijkstra import dijkstra
import numpy as np
from colorama import Fore


def k_medoids(G, k, distMap, tmax = 100):

    medoid = np.random.choice(G.nodes, k, replace=False)
    cluster = {}

    for i in range(tmax):
        for i in range(k):
            cluster[i] = []

        for j in G.nodes:
            cluster[np.argmin([distMap[m][j] for m in medoid])].append(j)

        for key, values in cluster.items():
            m = []
            for i in values:
                m.append(sum([distMap[i][v] for v in values]))
            medoid[key] = values[m.index(min(m))]

    return cluster


if __name__ == '__main__':

    f = open('simple-map-dungeon.txt', 'r')
    num_cluster = 4

    graph = []

    for i in f:
        graph.append(i.rstrip().split(' '))

    graph = np.array(graph)
    graph = np.rot90(np.rot90(np.rot90(graph)))
    tmp = graph

    obj = makeGraph()
    obj.create_graph(graph)  # Create labels and the location of the graph

    graph = obj.build_nx_graph(obj.succDict, obj.nodeDict)  # Create the graph from the labels and location

    nodes = max(graph.nodes)
    distMat = [['x' for x in range(nodes + 1)] for x in range(nodes + 1)]

    for i in graph.nodes:
        for j in graph.nodes:
            if i != j and distMat[i][j] == 'x':
                dist, path = dijkstra(graph, i, j)
                for k in dist.keys():
                    if dist[k] < float('inf'):
                        distMat[i][k] = dist[k]
                        distMat[k][i] = dist[k]
            elif i == j:
                distMat[i][j] = 0

    cluster = k_medoids(graph, num_cluster, distMat, 1000)

    pattern = ['x', 'y', 'z', 'w']
    for key, values in cluster.items():
        c = pattern[key]
        for k in values:
            x, y = graph.nodes[k]['location']
            tmp[x][y] = c

    tmp = np.rot90(tmp)
    m, n = tmp.shape
    for i in range(m):
        for j in range(n):
            if tmp[i][j] == 'x':
                print(Fore.BLUE + 'o', end=' ')
            elif tmp[i][j] == 'y':
                print(Fore.YELLOW + 'o', end=' ')
            elif tmp[i][j] == 'z':
                print(Fore.GREEN + 'o', end=' ')
            elif tmp[i][j] == 'w':
                print(Fore.RED + 'o', end=' ')
            else:
                print(Fore.BLACK + tmp[i][j], end=' ')
        print()
