from GameAI.problems07.make_graph import *
import numpy as np
from colorama import Fore


def k_means(G, k, W, tmax=100):

    m = np.random.choice(G.nodes, k, replace=False)
    means = []
    for i in m:
        means.append(list(W[i]))

    cluster = {}

    for i in range(tmax):
        for j in range(k):
            cluster[j] = []

        for j in G.nodes:
            cluster[np.argmin([np.sqrt(np.sum((W[j] - m) ** 2)) for m in means])].append(j)

        for j in range(k):
            if len(cluster[j]):
                means[j] = np.sum(np.array([list(W[p]) for p in cluster[j]]), axis=0)/len(cluster[j])
            else:
                means[j] = np.zeros(k)

    return cluster


def computeDegree(M):
    D = np.diag(np.sum(M, axis=1))

    return D


def adjMatrix(G):

    nodes = max(G.nodes) + 1
    adjM = np.zeros(nodes*nodes, dtype=int).reshape(nodes, nodes)

    for k in G.edges:
        x, y = k
        adjM[x][y] = 1
        adjM[y][x] = 1

    return adjM


if __name__ == '__main__':

    graph = np.loadtxt('simple-map-dungeon.txt', dtype=str)
    num_cluster = 4

    graph = np.rot90(np.rot90(np.rot90(graph)))
    tmp = graph

    obj = makeGraph()
    obj.create_graph(graph)

    graph = obj.build_nx_graph(obj.succDict, obj.nodeDict)

    adjM = adjMatrix(graph)
    D = computeDegree(adjM)

    L = D - adjM
    eigenVal, eigenVec = np.linalg.eigh(L)

    W = eigenVec[:, [i for i in range(1, num_cluster+1)]]
    cluster = k_means(graph, num_cluster, W, 1000)

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
