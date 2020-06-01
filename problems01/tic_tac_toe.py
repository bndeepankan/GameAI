
import numpy as np


def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S


def move_by_probability(S, p, winx_prob, wino_prob):
    xs, yx = np.where(S==0)
    s_zero = np.where(S.flatten()==0)[0].tolist()
    j = 0
    if p == 1:
        j = binarySort(s_zero, winx_prob)
    elif p == -1:
        j = binarySort(s_zero, wino_prob)
    winx_prob.remove(j)
    wino_prob.remove(j)
    i = s_zero.index(j)
    S[xs[i], yx[i]] = p

    return S


def binarySort(arr, priority):
    arr = sorted(arr)

    val = findNum(arr, priority[0], 0, len(arr)-1)
    if val:
        return priority[i]


def findNum(arr, key, l, r):
    
    if l <= r:

        mid = int(l + (r-l)/2)

        if arr[mid] == key:
            return True
        elif arr[mid] > key:
            return findNum(arr, key, l, mid-1)
        else:
            return findNum(arr, key, mid+1, r)

    return False


def move_by_evaluation(S, p):
    xs, ys = np.where(S == 0)
    max_val = float('-inf')
    index = 0
    if len(xs) == 9:
        index = 4
    else:
        for i in range(len(xs)):
            S[xs[i], ys[i]] = p
            if not move_was_winning_move(S, p):
                curr_x = evaluate(S, -1)
                curr_o = evaluate(S, 1)
                curr = curr_x - curr_o
                if curr > max_val:
                    index = i
                    max_val = curr
                S[xs[i], ys[i]] = 0
            else:
                return S

    S[xs[index], ys[index]] = p
    return S


def evaluate(S, p):
    count = 0
    if -p not in S[0,:]:
        count = count + 1
    if -p not in S[1,:]:
        count = count + 1
    if -p not in S[2,:]:
        count = count + 1
    if -p not in S[:,0]:
        count = count + 1
    if -p not in S[:,1]:
        count = count + 1
    if -p not in S[:,2]:
        count = count + 1
    if -p not in np.diag(S):
        count = count + 1
    if -p not in np.diag(np.rot90(S)):
        count = count + 1
    return count


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False



# python dictionary to map integers (1, -1, 0) to characters ('x', 'o', ' ')
symbols = { 1:'x',
           -1:'o',
            0:' '}


# print game state matrix using characters
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)





if __name__ == '__main__':

    for i in range(1):
        # initialize an empty tic tac toe board
        gameState = np.zeros((3,3), dtype=int)

        # initialize the player who moves first (either +1 or -1)
        player = 1

        # initialize a move counter
        mvcntr = 1

        # initialize a flag that indicates whetehr or not game has ended
        noWinnerYet = True

        # probability of selecting winning fields in increasing order
        winx_prob = [4, 2, 6, 8, 0, 3, 5, 7, 1]
        wino_prob = [4, 2, 8, 0, 6, 5, 7, 1, 3]
        
        f = open('test.csv', 'a')
        
        while move_still_possible(gameState) and noWinnerYet:
            # turn current player number into player symbol
            name = symbols[player]
            print ('%s moves' % name)

            # let player "O" move at random
            if player == -1:
                gameState = move_at_random(gameState, player)
            elif player == 1:
                # let player "X" move by evaluation
                gameState = move_by_evaluation(gameState, player)

            # let current player move at some probability
            # gameState = move_by_probability(gameState, player, winx_prob, wino_prob)

            # print current game state
            print_game_state(gameState)
            
            # evaluate current game state
            if move_was_winning_move(gameState, player):
                gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
                gameState1 = gameState1 + ',' + name
                print ('player %s wins after %d moves' % (name, mvcntr))
                noWinnerYet = False

            # switch current player and increase move counter
            player *= -1
            mvcntr +=  1



        if noWinnerYet:
            gameState1 = ','.join([str(x) for x in gameState.flatten().tolist()])
            gameState1 = gameState1 + ',' + "draw"
            print ('game ended in a draw' )

        f.write(gameState1)
        f.write("\n")
    f.close()