from GameAI.problems01.connect_four import *
import numpy as np


def build_tree(S, p, node, depth):
    """
    S : Game State.
    p : Current player.
    node : Number of the GameState in the Game Tree.
    depth : Total depth till which the tree is to be constructed.
    """

    succ = []

    check = move_was_winning_move(S, p)
    pos = move_still_possible(S)

    if node not in succDict:
        if not check and pos and depth > -1:
            p *= -1
            rs = []
            cs = []
            for i in range(7):
                if len(np.where(S[:, i] == 0)[0]) > 0:
                    cs.append(i)
                    rs.append(np.where(S[:, i] == 0)[0][-1])
            for j in range(len(rs)):
                Ssucc = np.copy(S)
                Ssucc[rs[j], cs[j]] = p

                newnode = max(nodeDict.keys()) + 1
                nodeDict[newnode] = Ssucc

                succ.append(newnode)
        elif depth == -1:
            nodeUtilDict[node] = evaluation(S, p)
        else:
            if not pos:
                nodeUtilDict[node] = 0
            if check:
                nodeUtilDict[node] = p

        if succ:
            succDict[node] = succ

    for s in succ:
        build_tree(nodeDict[s], p, s, depth - 1)


def evaluation(S, p):
    """
    Heuristic method to calculate the chances of winning in this state
    """
    T1 = np.copy(S)
    T1[T1==0] = p
    n1 = num_winning_lines(T1, p)

    T2 = np.copy(S)
    T2[T2==0] = -p
    n2 = num_winning_lines(T2, -p)

    return n1-n2


def num_winning_lines(S, p):
    """
    Calculates the number of winning ways
    """
    m, n = S.shape
    count = 0
    for i in range(m - 1, -1, -1):
        if len(np.where(S[i, :] == p)[0]) >= 4:
            count = count + count_four(S[i, :], p)

    for i in range(n - 1, -1, -1):
        if len(np.where(S[:, i] == p)[0]) >= 4:
            count = count + count_four(S[:, i], p)

    for i in range(int(m / 2) + 1):
        if len(np.where(np.diag(S, i) == p)[0]) >= 4:
            count = count + count_four(np.diag(S, i), p)

        if len(np.where(np.diag(np.rot90(S), i) == p)[0]) >= 4:
            count = count + count_four(np.diag(np.rot90(S), i), p)

        if len(np.where(np.diag(S, -i) == p)[0]) >= 4 and i != 0:
            count = count + count_four(np.diag(S, -i), p)

        if len(np.where(np.diag(np.rot90(S), -i) == p)[0]) >= 4 and i != 0:
            count = count + count_four(np.diag(np.rot90(S), -i), p)

    return count


def count_four(S, p):
    """
    Checks if four values are consecutive
    """
    stack = []
    arr = tuple(S)
    n = len(S)
    if (arr, p) in mapEvalVal:
        return mapEvalVal[(arr,p)]
    for i in range(n):
        if arr[i] == p:
            stack.append(p)
        else:
            while stack:
                stack.pop()
        if sum(stack) * p == 4:
            mapEvalVal[(arr,p)] = 1
            return mapEvalVal[(arr,p)]
    mapEvalVal[(arr,p)] = 0
    return mapEvalVal[(arr,p)]


def move_any_choice(S, node):
    """
    S : GameState
    node : Current node in the Game tree
    return : Next GameState and node
    """
    tmp = succDict[node]
    val = node
    if tmp:
        val = np.random.choice(tmp)
        S = nodeDict[val]
    return S, val


def maxNodeUtil(node):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = nodeUtilDict[node]
        return nodeMinMaxDict[node]
    mmv = float('-inf')
    for s in succDict[node]:
        mmv = max(mmv, minNodeUtil(s))
    nodeMinMaxDict[node] = mmv
    return nodeMinMaxDict[node]


def minNodeUtil(node):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = nodeUtilDict[node]
        return nodeMinMaxDict[node]
    mmv = float('inf')
    for s in succDict[node]:
        mmv = min(mmv, maxNodeUtil(s))
    nodeMinMaxDict[node] = mmv
    return nodeMinMaxDict[node]


def scanTree(node):
    for k in succDict[node]:
        if k in nodeMinMaxDict:
            return True
    return False


def computeMissingValue(node):
    mmv = float('-inf')
    for k in succDict[node]:
        mmv = max(mmv, maxNodeUtil(k))
    return mmv


nodeDict = {}
succDict = {}
nodeMinMaxDict = {}
nodeUtilDict = {}
mapEvalVal = {}


if __name__ == '__main__':

    for i in range(1):

        gameState = np.zeros((6,7), dtype=int)

        player = -1
        mvcntr = 1

        noWinnerYet = True

        node = 0
        depth = 2
        nodeDict[node] = gameState

        f = open('test.csv', 'a')

        while move_still_possible(gameState) and noWinnerYet:

            build_tree(gameState, player, node, depth)
            player *= -1

            name = symbols[player]
            print('%s moves' % name)

            if player == -1:
                gameState, node = move_any_choice(gameState, node)
            elif player == 1:
                optVal = maxNodeUtil(node)
                k = node
                if not scanTree(node):
                    optVal = computeMissingValue(node)
                for k in succDict[node]:
                    if nodeMinMaxDict[k] == optVal:
                        gameState = nodeDict[k]
                        break

                node = k

            print_game_state(gameState)

            if move_was_winning_move(gameState, player):
                gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
                gameState1 = gameState1 + ',' + name
                print('player %s wins after %d moves' % (name, mvcntr))
                noWinnerYet = False

            mvcntr += 1

        if noWinnerYet:
            gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
            gameState1 = gameState1 + ',' + "draw"
            print('game ended in a draw')

        f.write(gameState1)
        f.write("\n")
    f.close()
