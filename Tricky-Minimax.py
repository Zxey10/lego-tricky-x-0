from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, \
    not_equal_to
import math
import random

cellSize = 4
gridSize = 12
gridWidth = 4
gridHeight = 4
pairMotorSpeed = 10
rotateRobotSize = 2.5
robotError = 9.25

motor_pair = MotorPair('B', 'A')
pen_motor = Motor('C')

hub = MSHub()

color_sensor = ColorSensor('E')
motor_pair.set_default_speed(pairMotorSpeed)
pen_motor.run_to_position(165, 'shortest path')

offset = 1

boardMatrix = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]


class Player:
    X = "+"
    O = '-'


movements_map = {
    'RR': {'distance': 10, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 0},
    'GR': {'distance': 10, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 0},
    'BR': {'distance': 10, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 0},
    'BG': {'distance': 6, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 1},
    'RG': {'distance': 6, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 1},
    'GG': {'distance': 6, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 1},
    'GB': {'distance': 2, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 2},
    'RB': {'distance': 2, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 2},
    'BB': {'distance': 2, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 2}
}


class RotationTurn:
    rotatePlayerTurn = Player.X

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


def chooseRandomMovementKey(movementsKeys):
    if len(movementsKeys) == 0:
        return None
    movement_key = random.choice(movementsKeys)
    return movement_key


def getMovementFilteredKeys():
    filtered_keys = [key for key, value in movements_map.items() if value['isEmpty']]
    return filtered_keys


def printToHub(message: str):
    hub.light_matrix.write(message)


def getBestMoveKey(best_move):
    for key, values in movements_map.items():
        if (values['row'], values['col']) == best_move:
            return key
    else:
        return None




class Game:
    robotPlayer = Player.X
    humanPlayer = Player.O
    playerTurn = Player.X
    isGameOver = False
    isRobotFirst = True
    loops = 0

    def startGame(self):
        hub.speaker.play_sound('Play')
        while not self.isGameOver:

            self.loops += 1

            print("Player Turn", self.playerTurn)

            if self.playerTurn == Player.X:
                self.drawRobotPlayer()
            else:
                self.drawHumanPlayer()

            print(boardMatrix)

            if self.loops >= 9:
                self.gameOver()

    def changeTurn(self):
        if self.playerTurn == Player.X:
            self.playerTurn = Player.O
        else:
            self.playerTurn = Player.X
        printToHub(self.playerTurn)

    def drawRobotPlayer(self) -> bool:

        bestMove = findBestMove(board=boardMatrix)
        row = bestMove[0]
        col = bestMove[1]
        
        bestMoveKey = getBestMoveKey((row, col))

        if bestMoveKey is None:
            print("No Places Left")
            return False

        print("Robot Drawing X at", bestMoveKey)
        moveAndRotate(movements_map[bestMoveKey]['distance'], movements_map[bestMoveKey]['rotation'],
                      movements_map[bestMoveKey]['upDir'], movements_map[bestMoveKey]['row'],
                      movements_map[bestMoveKey]['col'])
        movements_map[bestMoveKey]['isEmpty'] = False
        movements_map[bestMoveKey]['player'] = Player.X

        self.changeTurn()

        [winnerText, status] = self.checkForWinner()
        if status:
            print(winnerText)
            printToHub(winnerText)
            hub.speaker.play_sound('Celebrate')
            wait_for_seconds(3)
            hub.light_matrix.show_image('HAPPY')
            self.gameOver()
            return

        return True

    def drawHumanPlayer(self) -> bool:
        humanPosition = scanForColors()

        if humanPosition is None:
            print("No Places Left")
            return False

        print("Human Drawing O at", humanPosition)
        moveAndRotate(movements_map[humanPosition]['distance'], movements_map[humanPosition]['rotation'],
                      movements_map[humanPosition]['upDir'], movements_map[humanPosition]['row'],
                      movements_map[humanPosition]['col'])
        movements_map[humanPosition]['isEmpty'] = False
        movements_map[humanPosition]['player'] = Player.O

        self.changeTurn()

        [winnerText, status] = self.checkForWinner()
        if status:
            print(winnerText)
            printToHub(winnerText)
            hub.speaker.play_sound('Celebrate')
            wait_for_seconds(3)
            hub.light_matrix.show_image('ANGRY')
            self.gameOver()
            return

        return True

    def drawDiagonalsWinnerPaths(self, diag: int):
        # First Diagonal
        if diag == 1:
            rotateRobot(100)
            moveRobot(4)
            rotateRobot45(-100)
            moveRobot(-robotError / 2)
            # TODO rotate 45
            lowerPen()
            moveRobot(12)
            raisePen()

        # Second Diagonal
        if diag == 2:
            moveRobot(12)
            rotateRobot(100)
            moveRobot(4)
            rotateRobot45(100)
            moveRobot(-robotError / 2)
            # TODO rotate 45
            lowerPen()
            moveRobot(12)
            raisePen()

    def drawRowsWinnerPaths(self, row: int):
        # 1 Row
        if row == 1:
            moveRobot(10 + offset)
            rotateRobot(100)
            moveRobot(14)
            rotateRobot(100)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(8)
            raisePen()
        # 2 Row
        if row == 2:
            moveRobot(10 + offset)
            rotateRobot(100)
            moveRobot(10)
            rotateRobot(100)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(8)
            raisePen()
        # 3 Row
        if row == 3:
            moveRobot(10 + offset)
            rotateRobot(100)
            moveRobot(6)
            rotateRobot(100)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(8)
            raisePen()

    def drawColsWinnerPaths(self, col: int):
        # 1 Col
        if col == 1:
            moveRobot(10 + offset)
            rotateRobot(100)
            moveRobot(14)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(-8)
            raisePen()
        # 2 Col
        if col == 2:
            moveRobot(6 + offset)
            rotateRobot(100)
            moveRobot(14)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(-8)
            raisePen()
        # 3 Col
        if col == 3:
            moveRobot(2 + offset)
            rotateRobot(100)
            moveRobot(14)
            moveRobot(-robotError)
            lowerPen()
            moveRobot(-8)
            raisePen()

    def checkForWinner(self) -> [str, bool]:
        board = boardMatrix

        # Rows
        # Player X
        if board[0][0] == Player.X and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            self.drawRowsWinnerPaths(1)
            return ["{Player.X} wins", True]

        if board[1][0] == Player.X and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            self.drawRowsWinnerPaths(2)
            return ["{Player.X} wins", True]

        if board[2][0] == Player.X and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            self.drawRowsWinnerPaths(3)
            return ["{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            self.drawRowsWinnerPaths(1)
            return ["{Player.O} wins", True]

        if board[1][0] == Player.O and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            self.drawRowsWinnerPaths(2)
            return ["{Player.O} wins", True]

        if board[2][0] == Player.O and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            self.drawRowsWinnerPaths(3)
            return ["{Player.O} wins", True]

        # Columns
        # Player X
        if board[0][0] == Player.X and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            self.drawColsWinnerPaths(1)
            return ["{Player.X} wins", True]

        if board[0][1] == Player.X and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            self.drawColsWinnerPaths(2)
            return ["{Player.X} wins", True]

        if board[0][2] == Player.X and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            self.drawColsWinnerPaths(3)
            return ["{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            self.drawColsWinnerPaths(1)
            return ["{Player.O} wins", True]

        if board[0][1] == Player.O and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            self.drawColsWinnerPaths(2)
            return ["{Player.O} wins", True]

        if board[0][2] == Player.O and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            self.drawColsWinnerPaths(3)
            return ["{Player.O} wins", True]

        # Diagonal_F

        # Player X
        if board[0][0] == Player.X and board[0][0] == board[1][1] and board[2][2] == board[1][1]:
            self.drawDiagonalsWinnerPaths(1)
            return ["{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[1][1] and board[2][2] == board[1][1]:
            self.drawDiagonalsWinnerPaths(1)
            return ["{Player.O} wins", True]

        # Diagonal_S

        # Player X
        if board[0][2] == Player.X and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            self.drawDiagonalsWinnerPaths(2)
            return ["{Player.X} wins", True]

            # Player O
        if board[0][2] == Player.O and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            self.drawDiagonalsWinnerPaths(2)
            return ["{Player.O} wins", True]

        filtered_keys = getMovementFilteredKeys()
        if len(filtered_keys) == 0:
            print("Tie")
            return ["Tie", True]

        return ["", False]

    def gameOver(self):
        self.isGameOver = True


class Orientation:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    currentOrientation = "DOWN"


def calibrate():
    motor_pair.move(-4, 'cm')
    motor_pair.move(4, 'cm')


def raisePen():
    print("PEN IS UP")
    pen_motor.run_for_degrees(90)


def lowerPen():
    print("PEN IS DOWN")
    pen_motor.run_for_degrees(-90)


def moveRobot(amount):
    print("Moving on direction:", Orientation.currentOrientation, amount)
    motor_pair.move(amount, 'cm')


def rotateRobot180():
    print("Rotating robot 180deg")
    if Orientation.currentOrientation == Orientation.DOWN:
        # DOWN -> UP
        Orientation.currentOrientation = Orientation.UP
    elif Orientation.currentOrientation == Orientation.UP:
        # UP -> DOWN
        Orientation.currentOrientation = Orientation.DOWN
    elif Orientation.currentOrientation == Orientation.LEFT:
        # LEFT -> RIGHT
        Orientation.currentOrientation = Orientation.RIGHT
    elif Orientation.currentOrientation == Orientation.RIGHT:
        # RIGHT -> LEFT
        Orientation.currentOrientation = Orientation.LEFT

    print("New Orientation:", Orientation.currentOrientation)

    motor_pair.move(360, 'degrees')


def rotateRobot45(direction):
    motor_pair.move(90, 'degrees', steering=direction)


def rotateRobot(direction: int):
    # -100 - LEFT
    #  100 - RIGHT

    if Orientation.currentOrientation == Orientation.DOWN and direction == 100:
        # DOWN -> RIGHT
        Orientation.currentOrientation = Orientation.RIGHT
    elif Orientation.currentOrientation == Orientation.DOWN and direction == -100:
        # DOWN -> LEFT
        Orientation.currentOrientation = Orientation.LEFT
    elif Orientation.currentOrientation == Orientation.RIGHT and direction == 100:
        # RIGHT -> UP
        Orientation.currentOrientation = Orientation.UP
    elif Orientation.currentOrientation == Orientation.RIGHT and direction == -100:
        # RIGHT -> DOWN
        Orientation.currentOrientation = Orientation.DOWN
    elif Orientation.currentOrientation == Orientation.LEFT and direction == 100:
        # LEFT -> DOWN
        Orientation.currentOrientation = Orientation.DOWN
    elif Orientation.currentOrientation == Orientation.LEFT and direction == -100:
        # LEFT -> UP
        Orientation.currentOrientation = Orientation.UP
    elif Orientation.currentOrientation == Orientation.UP and direction == 100:
        # UP -> RIGHT
        Orientation.currentOrientation = Orientation.RIGHT
    elif Orientation.currentOrientation == Orientation.UP and direction == -100:
        # UP -> RIGHT
        Orientation.currentOrientation = Orientation.RIGHT

    motor_pair.move(182, 'degrees', steering=direction)

    print("Rotate robot to:", direction, Orientation.currentOrientation)


def calculateDirection(dir_: int):
    if dir_ % 2 == 0:
        # LEFT
        return -100
    # RIGHT
    return 100


def drawLine():
    print("Drawing Line")
    moveRobot(1)
    lowerPen()
    moveRobot(-2)
    raisePen()
    moveRobot(1)


def drawPoint():
    print("Drawing Point")
    lowerPen()
    raisePen()


def moveAndRotate(distance, rotation, upDistance, row, col):
    moveRobot(distance + offset)
    rotateRobot(rotation)

    moveRobot(upDistance)
    moveRobot(-robotError)

    if RotationTurn.rotatePlayerTurn == Player.X:
        drawPoint()
        boardMatrix[row][col] = '+'
        RotationTurn.rotatePlayerTurn = Player.O
        print("Player Turn in Rotate", RotationTurn.rotatePlayerTurn)
    else:
        drawLine()
        boardMatrix[row][col] = '-'
        print("Player Turn in Rotate", RotationTurn.rotatePlayerTurn)
        RotationTurn.rotatePlayerTurn = Player.X

    moveRobot(robotError)

    moveRobot(-upDistance)
    rotateRobot(-rotation)
    moveRobot(-distance - offset)


# First Row
def goToRR():
    moveAndRotate(10, 100, 14, 0, 0)


def goToRG():
    moveAndRotate(6, 100, 14, 0, 1)


def goToRB():
    moveAndRotate(2, 100, 14, 0, 2)


# Second Row
def goToGR():
    moveAndRotate(10, 100, 10, 1, 0)


def goToGG():
    moveAndRotate(6, 100, 10, 1, 1)


def goToGB():
    moveAndRotate(2, 100, 10, 1, 2)


# Third Row
def goToBR():
    moveAndRotate(10, 100, 6, 2, 0)


def goToBG():
    moveAndRotate(6, 100, 6, 2, 1)


def goToBB():
    moveAndRotate(2, 100, 6, 2, 2)


def drawBoard():
    # hub.speaker.play_sound('Activate')
    for i in range(gridWidth):
        lowerPen()
        moveRobot(gridSize)
        raisePen()
        moveRobot(robotError)

        if i == 3:
            rotateRobot(-100)
            moveRobot(-robotError)
        else:
            rotateRobot(calculateDirection(i))
            moveRobot(cellSize)

            rotateRobot(calculateDirection(i))
            moveRobot(-robotError)

    for i in range(gridWidth):
        lowerPen()
        moveRobot(gridSize)
        raisePen()
        moveRobot(robotError)

        rotateRobot(calculateDirection(i))
        moveRobot(cellSize)

        if i == 3:
            rotateRobot(calculateDirection(i))
        else:
            rotateRobot(calculateDirection(i))
            moveRobot(-robotError)


def scanForColors():
    choichesColors = []
    while True:
        color = color_sensor.wait_for_new_color()
        if color == 'green':
            print('green')
            choichesColors.append(color[0])
            printToHub("Green")
            wait_for_seconds(3)
        elif color == 'blue':
            print('blue')
            choichesColors.append(color[0])
            printToHub("Blue")
            wait_for_seconds(3)
        elif color == 'red':
            print('red')
            choichesColors.append(color[0])
            printToHub("Red")
            wait_for_seconds(3)

        printToHub(RotationTurn.rotatePlayerTurn)

        if len(choichesColors) == 2:
            print(choichesColors)

            key = "".join(choichesColors).upper();
            print(key)
            filtered_keys = getMovementFilteredKeys()

            if key in filtered_keys:
                return key

            # Postion already taken
            print("Position is not empty")
            hub.speaker.play_sound('Oh No')
            choichesColors = []


calibrate()

drawBoard()

game = Game()

game.startGame()











