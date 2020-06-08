nodeDict = {}
nodeSuccDict = {}
nodeUtilDict = {}
nodeMinMaxDict = {}


def maxNodeUtil(node):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = [nodeUtilDict[node], nodeUtilDict[node]]
        return nodeMinMaxDict[node]
    mmv = []
    for s in nodeSuccDict[node]:
        mmv.append(minNodeutil(s))
    tmp = list(map(lambda x: x[0], mmv))
    if tmp.count(max(tmp)) > 1:
        nodeMinMaxDict[node] = [max(tmp), max(list(map(lambda x: x[1] if x[0] == max(tmp) else float('-inf'), mmv)))]
    else:
        nodeMinMaxDict[node] = max(mmv)
    return nodeMinMaxDict[node]


def minNodeutil(node):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = [nodeUtilDict[node], nodeUtilDict[node]]
        return nodeMinMaxDict[node]
    mmv = []
    for s in nodeSuccDict[node]:
        mmv.append(maxNodeUtil(s))
    tmp = list(map(lambda x: x[0], mmv))
    nodeMinMaxDict[node] = [min(tmp), max(tmp)]
    return nodeMinMaxDict[node]


if __name__ == '__main__':

    nodeSuccDict = {'n0':['n1','n2','n3','n4'], 'n1':['n5','n6','n7','n8','n9'], 'n2':['n10','n11'], 'n3': ['n12','n13','n14'], 'n4': ['n15','n16']}
    nodeUtilDict = {'n5': 18, 'n6': 6, 'n7': 16, 'n8': 6, 'n9': 5, 'n10': 7, 'n11': 1, 'n12': 16, 'n13': 16, 'n14': 5, 'n15': 10, 'n16': 2}
    node = 'n0'
    mmv, check = maxNodeUtil(node)
    print(mmv, check)
