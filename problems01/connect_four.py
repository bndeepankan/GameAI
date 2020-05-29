import numpy as np


def move_still_possible(S):
    return not (S[S == 0].size == 0)


def move_at_random(S, p):
    yx = []
    for i in range(7):
        if len(np.where(S[:,i] == 0)[0]) > 0:
            yx.append(i)
    k = np.random.choice(yx)
    xs = np.where(S[:, k] == 0)[0][-1]

    S[xs, k] = p

    return S


def move_was_winning_move(S, p):
    m, n = S.shape
    for i in range(m-1, -1, -1):
        if len(np.where(S[i,:] == p)[0]) >= 4:   # To Do: Need to write a map to stored the result of computed segment
            flag = count_four(S[i,:], p)
            if flag:
                return flag

    for i in range(n-1, -1, -1):
        if len(np.where(S[:,i] == p)[0]) >= 4:
            flag = count_four(S[:,i], p)
            if flag:
                return flag

    for i in range(int(m/2)+1):
        if len(np.where(np.diag(S, i) == p)[0]) >= 4:
            flag = count_four(np.diag(S, i), p)
            if flag:
                return flag
        if len(np.where(np.diag(np.rot90(S), i) == p)[0]) >= 4:
            flag = count_four(np.diag(np.rot90(S), i), p)
            if flag:
                return flag
        if len(np.where(np.diag(S, -i) == p)[0]) >= 4 and i != 0:
            flag = count_four(np.diag(S, -i), p)
            if flag:
                return flag
        if len(np.where(np.diag(np.rot90(S), -i) == p)[0]) >= 4 and i != 0:
            flag = count_four(np.diag(np.rot90(S), -i), p)
            if flag:
                return flag

    return False


def count_four(S, p):
    stack = []
    arr = list(S)
    n = len(S)
    for i in range(n):
        if arr[i] == p:
            stack.append(p)
        else:
            while stack:
                stack.pop()
        if sum(stack) * p == 4:
            return True
    return False


symbols = {1: 'x', -1: 'o', 0: ' '}


# print game state matrix using characters
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)


if __name__ == '__main__':

    for i in range(1):          # Increasing the number of iterations

        gameState = np.zeros((6,7), dtype=int)
        player = 1
        mvcntr = 1
        noWinnerYet = True

        f = open('test.csv', 'a')

        while move_still_possible(gameState) and noWinnerYet:

            name = symbols[player]
            print('%s moves' % name)
            gameState = move_at_random(gameState, player)

            print_game_state(gameState)

            if move_was_winning_move(gameState, player):
                gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
                gameState1 = gameState1 + ',' + name
                print('player %s wins after %d moves' % (name, mvcntr))
                noWinnerYet = False

            player *= -1
            mvcntr += 1

        if noWinnerYet:
            gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
            gameState1 = gameState1 + ',' + "draw"
            print('game ended in a draw')

        f.write(gameState1)
        f.write("\n")
    f.close()