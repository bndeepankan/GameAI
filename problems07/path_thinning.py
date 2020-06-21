from GameAI.problems07.make_graph import *
from GameAI.problems07.a_star import a_star, shortestPath
from GameAI.problems07.dijkstra import dijkstra, dijkstraShortestPath


def checkPredVisible(G, pred, node, obj):
    """
    Implementation of Bresenham's line drawing algorithm
    """
    px, py = G.nodes[pred]['location']
    nx, ny = G.nodes[node]['location']
    dx = abs(nx - px)
    dy = abs(ny - py)
    m = 1
    try:
        if (ny-py)/(nx-px) < 0:
            m = -1
    except ZeroDivisionError:
        pass
    P = 2 * dy - dx
    flag = 1
    while px < nx:
        try:
            if obj.mapVal[(px, py)]:
                px += 1
                if P < 0:
                    P = P + 2 * dy
                else:
                    P = P + 2 * dy - 2 * dx
                    py += m
        except KeyError:
            flag = 0
            break
    return flag


def thinOutPath(G, path, obj):
    newPath = []
    newPath.append(path.pop())
    newPath.append(path.pop())
    while path:
        pred = newPath[-2]
        node = path.pop()
        if checkPredVisible(G, pred, node, obj):
            newPath.pop()
        newPath.append(node)
    return newPath


if __name__ == '__main__':

    f = open('simple-map-1.txt', 'r')
    graph = []

    for i in f:
        graph.append(i.rstrip().split(' '))

    graph = np.array(graph)
    graph = np.rot90(np.rot90(np.rot90(graph)))
    tmp = graph

    obj = makeGraph()
    obj.create_graph(graph)

    graph = obj.build_nx_graph(obj.succDict, obj.nodeDict)
    src = obj.mapVal[(1, 8)]
    t = obj.mapVal[(14, 8)]

    dist, path = a_star(graph, src, t)
    apath = shortestPath(path, src, t)

    dist, path = dijkstra(graph, src, t)
    dpath = dijkstraShortestPath(path, src,t)

    athinPath = thinOutPath(graph, apath, obj)
    dthinPath = thinOutPath(graph, dpath, obj)

    print("The shortest path of A* algorithm after path thinning\n", athinPath)
    print("\nThe shortest path of Dijkstra after path thinning\n", dthinPath)
