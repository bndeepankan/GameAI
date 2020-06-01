from GameAI.problems01.tic_tac_toe import *
import numpy as np


def buildTree(S, p, node):
    succ = []

    if not move_was_winning_move(S, p):
        p *= -1
        rs, cs = np.where(S==0)
        for j in range(rs.size):
            Ssucc = np.copy(S)
            Ssucc[rs[j], cs[j]] = p

            newnode = max(nodeDict.keys()) + 1
            nodeDict[newnode] = Ssucc

            succ.append(newnode)

    succDict[node] = succ

    for s in succ:
        buildTree(nodeDict[s], p, s)


nodeDict = {}
succDict = {}


if __name__ == '__main__':
    S = np.array([[1,1,-1],[0,1,0],[0,-1,-1]])
    p = 1

    node = 0
    nodeDict[node] = S
    buildTree(S, p, node)
    print(nodeDict)
