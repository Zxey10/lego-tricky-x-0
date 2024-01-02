class Player:
    X = "x"
    O = 'o'


# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return True
    return False

def evaluate(b):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
            if (b[row][0] == Player.X):
                return 10
            elif (b[row][0] == Player.O):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):

        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):

            if (b[0][col] == Player.X):
                return 10
            elif (b[0][col] == Player.O):
                return -10

    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):

        if (b[0][0] == Player.X):
            return 10
        elif (b[0][0] == Player.O):
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):

        if (b[0][2] == Player.X):
            return 10
        elif (b[0][2] == Player.O):
            return -10

    return 0

def minimax(board, depth, isMax):
    score = evaluate(board)

    if score == 10:
        return score

    if score == -10:
        return score

    if not isMovesLeft(board):
        return 0

    if isMax:
        best = -1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if board[i][j] == "":
                    # Make the move
                    board[i][j] = Player.X

                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(board,
                                             depth + 1,
                                             not isMax))

                    # Undo the move
                    board[i][j] = ""
        return best

    else:
        best = 1000

        for i in range(3):
            for j in range(3):

                if board[i][j] == "":
                    # Make the move
                    board[i][j] = Player.O

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not isMax))

                    # Undo the move
                    board[i][j] = ""
        return best

def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3):
        for j in range(3):

            # Check if cell is empty
            if board[i][j] == "":

                board[i][j] = Player.X

                moveVal = minimax(board, 0, False)

                board[i][j] = ""

                if moveVal > bestVal:
                    bestMove = (i, j)
                    bestVal = moveVal

    print("The value of the best Move is :", bestVal)
    print()
    return bestMove


# Driver code
boardMatrix = [
    ["x", "x", "o"],
    ["o", "o", "x"],
    ["x", "o", "x"]
]

bestMove = findBestMove(boardMatrix)

print("The Optimal Move is :")
print("ROW:", bestMove[0], " COL:", bestMove[1])
print(bestMove)