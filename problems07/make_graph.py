import numpy as np


class makeGraph:

    def __init__(self):
        self.succDict = {}
        self.nodeDict = {}
        self.mapVal = {}

    def findSucc(self, a, pos):
        succ = []
        m = len(a)
        n = len(a[0])
        x, y = pos
        if -1 < x+1 < m and -1 < y < n and a[x+1][y] == '0':
            succ.append(self.mapVal[(x+1, y)])
        if -1 < x < m and -1 < y+1 < n and a[x][y+1] == '0':
            succ.append(self.mapVal[(x, y+1)])
        if -1 < x < m and -1 < y-1 < n and a[x][y-1] == '0':
            succ.append(self.mapVal[(x, y-1)])
        if -1 < x-1 < m and -1 < y < n and a[x-1][y] == '0':
            succ.append(self.mapVal[(x-1, y)])

        return succ

    def create_graph(self, arr):
        row = len(arr)
        col = len(arr[0])
        node = 0

        for i in range(row):
            for j in range(col):
                if arr[i][j] == '0':
                    self.nodeDict[node] = (i, j)
                    self.mapVal[(i, j)] = node
                node = node + 1

        for k,v in self.nodeDict.items():
            self.succDict[k] = self.findSucc(arr, v)


if __name__ == '__main__':
    f = open('simple-map-1.txt', 'r')
    graph = []

    for i in f:
        graph.append(i.rstrip().split(' '))

    graph = np.array(graph)
    graph = np.rot90(np.rot90(np.rot90(graph)))

    obj = makeGraph()

    obj.create_graph(graph)
    print(obj.nodeDict)
    print(obj.succDict)
