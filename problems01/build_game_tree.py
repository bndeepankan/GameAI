from GameAI.problems01.tic_tac_toe import *
import numpy as np


def buildTree(S, p, node):
    succ = []

    check = move_was_winning_move(S, p)
    pos = move_still_possible(S)
    if not check and pos:
        p *= -1
        rs, cs = np.where(S==0)
        for j in range(rs.size):
            Ssucc = np.copy(S)
            Ssucc[rs[j], cs[j]] = p

            newnode = max(nodeDict.keys()) + 1
            nodeDict[newnode] = Ssucc

            succ.append(newnode)
    else:
        if check:
            nodeUtilDict[node] = p
        elif not pos:
            nodeUtilDict[node] = 0

    succDict[node] = succ

    for s in succ:
        buildTree(nodeDict[s], p, s)


nodeDict = {}
succDict = {}
nodeUtilDict = {}

if __name__ == '__main__':
    S = np.array(([0,1,0],[0,1,0],[0,-1,0]))
    p = 1

    node = 0
    nodeDict[node] = S
    buildTree(S, p, node)
    print(nodeDict)