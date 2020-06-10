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


def move_any_choice(S, node):
    tmp = succDict[node]
    val = node
    if tmp:
        val = np.random.choice(tmp)
        for k,v in nodeDict.items():
            if k == val:
                S = v
                break
    return S, val


def maxNodeUtil(node, alpha, beta):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = nodeUtilDict[node]
        return nodeMinMaxDict[node]
    for s in succDict[node]:
        alpha = max(alpha, minNodeUtil(s, alpha, beta))
        if alpha >= beta:
            nodeMinMaxDict[node] = alpha
            return nodeMinMaxDict[node]
    nodeMinMaxDict[node] = alpha
    return nodeMinMaxDict[node]


def minNodeUtil(node, alpha, beta):
    if node in nodeUtilDict:
        nodeMinMaxDict[node] = nodeUtilDict[node]
        return nodeMinMaxDict[node]
    for s in succDict[node]:
        beta = min(beta, maxNodeUtil(s, alpha, beta))
        if beta <= alpha:
            nodeMinMaxDict[node] = beta
            return nodeMinMaxDict[node]
        nodeMinMaxDict[node] = beta
        return nodeMinMaxDict[node]


nodeDict = {}
succDict = {}
nodeMinMaxDict = {}
nodeUtilDict = {}
# python dictionary to map integers (1, -1, 0) to characters ('x', 'o', ' ')
symbols = { 1:'x',
           -1:'o',
            0:' '}


if __name__ == '__main__':

    for i in range(1):

        gameState = np.array(([0,1,0],[0,1,0],[0,-1,0]))

        player = 1
        mvcntr = 1

        noWinnerYet = True

        node = 0
        nodeDict[node] = gameState
        buildTree(gameState, player, node)
        player *= -1

        f = open('test.csv', 'a')

        while move_still_possible(gameState) and noWinnerYet:

            alpha = float('-inf')
            beta = float('inf')

            name = symbols[player]
            print('%s moves' %  name)

            if player == -1:
                gameState, node = move_any_choice(gameState, node)
            elif player == 1:
                optVal = maxNodeUtil(node, alpha, beta)
                k = node
                for k in succDict[node]:
                    if nodeMinMaxDict[k] == optVal:
                        gameState = nodeDict[k]
                        break
                node = k

            print_game_state(gameState)

            # evaluate current game state
            if move_was_winning_move(gameState, player):
                gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
                gameState1 = gameState1 + ',' + name
                print('player %s wins after %d moves' % (name, mvcntr))
                noWinnerYet = False

            # switch current player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
            gameState1 = gameState1 + ',' + "draw"
            print('game ended in a draw')

        f.write(gameState1)
        f.write("\n")
    f.close()
