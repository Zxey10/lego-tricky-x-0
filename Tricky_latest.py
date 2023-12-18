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

playerX = '+'
player0 = '-'

color_sensor = ColorSensor('E')
motor_pair.set_default_speed(pairMotorSpeed)
pen_motor.run_to_position(165, 'shortest path')

offset = 1

playerTurn = '+'

boardMatrix = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]


class Player:
    X = "+"
    O = '-'


movements_map = {
    'RR': {'distance': 10, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None},
    'GR': {'distance': 10, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None},
    'BR': {'distance': 10, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None},
    'BG': {'distance': 6, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None},
    'BB': {'distance': 2, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None},
    'RG': {'distance': 6, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None},
    'GG': {'distance': 6, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None},
    'GB': {'distance': 2, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None},
    'RB': {'distance': 2, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None}
}


def chooseRandomMovementKey(movementsKeys):
    if len(movementsKeys) == 0:
        return None
    movement_key = random.choice(movementsKeys)
    return movement_key


def getMovementFilteredKeys():
    filtered_keys = [key for key, value in movements_map.items() if value['isEmpty']]
    return filtered_keys


class Game:
    robotPlayer = Player.X
    humanPlayer = Player.O
    playerTurn = Player.X
    isGameOver = False
    isRobotFirst = True
    loops = 0

    def startGame(self):
        while not self.isGameOver:

            self.loops += 1

            if self.playerTurn == Player.X:
                self.drawRobotPlayer()
            else:
                self.drawHumanPlayer()

            if self.loops >= 9:
                self.gameOver()

    def changeTurn(self):
        if self.playerTurn == Player.X:
            self.playerTurn = Player.O
        else:
            self.playerTurn = Player.X

    def drawRobotPlayer(self) -> bool:
        filtered_keys = getMovementFilteredKeys()
        randomPlace = chooseRandomMovementKey(filtered_keys)
        if randomPlace is None:
            print("No Places Left")
            return False

        moveAndRotate(movements_map[randomPlace]['distance'], movements_map[randomPlace]['rotation'],
                      movements_map[randomPlace]['upDir'])
        movements_map[randomPlace]['isEmpty'] = False
        movements_map[randomPlace]['player'] = Player.X
        print("Robot Drawing X at", randomPlace)

        [winnerText, status] = self.checkForWinner()
        if status:
            print(winnerText)
            # TODO SHOW HAPPY FACE IF ROBOT WON ELSE ANGRY FACE
            self.gameOver()
            return

        self.changeTurn()
        return True

    def drawHumanPlayer(self) -> bool:
        humanPosition = scanForColors()

        if humanPosition is None:
            print("No Places Left")
            return False

        moveAndRotate(movements_map[humanPosition]['distance'], movements_map[humanPosition]['rotation'],
                      movements_map[humanPosition]['upDir'])
        movements_map[humanPosition]['isEmpty'] = False
        movements_map[humanPosition]['player'] = Player.O
        print("Human Drawing O at", humanPosition)

        [winnerText, status] = self.checkForWinner()
        if status:
            print(winnerText)
            # TODO SHOW HAPPY FACE IF ROBOT WON ELSE ANGRY FACE
            self.gameOver()
            return

        self.changeTurn()
        return True

    def drawDiagonalsWinnerPaths(self, diag: int):
        # First Diagonal
        if diag == 1:
            moveRobot(2 + offset)
            rotateRobot(100)
            moveRobot(6)
            moveRobot(-robotError)
            # TODO rotate 45
            rotateRobot45(-100)
            lowerPen()
            moveRobot(8)
            raisePen()

        # Second Diagonal
        if diag == 2:
            moveRobot(10 + offset)
            rotateRobot(100)
            moveRobot(2)
            moveRobot(-robotError)
            # TODO rotate 45
            rotateRobot45(100)
            lowerPen()
            moveRobot(8)
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
            return [f"{Player.X} wins", True]

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
            return [f"{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[1][1] and board[2][2] == board[1][1]:
            self.drawDiagonalsWinnerPaths(1)
            return [f"{Player.O} wins", True]

        # Diagonal_S

        # Player X
        if board[0][2] == Player.X and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            self.drawDiagonalsWinnerPaths(2)
            return [f"{Player.X} wins", True]

            # Player O
        if board[0][2] == Player.O and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            self.drawDiagonalsWinnerPaths(2)
            return [f"{Player.O} wins", True]

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
    moveRobot(1)
    lowerPen()
    moveRobot(-2)
    raisePen()
    moveRobot(1)


def drawPoint():
    lowerPen()


def moveAndRotate(distance, rotation, upDistance, row, col):
    moveRobot(distance + offset)
    rotateRobot(rotation)

    moveRobot(upDistance)
    moveRobot(-robotError)

    if Game.playerTurn == Player.X:
        boardMatrix[row][col] = '+'
        drawPoint()
    else:
        drawLine()
        boardMatrix[row][col] = '-'
    raisePen()

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
            wait_for_seconds(3)
        elif color == 'blue':
            print('blue')
            choichesColors.append(color[0])
            wait_for_seconds(3)
        elif color == 'red':
            print('red')
            choichesColors.append(color[0])
            wait_for_seconds(3)

        if len(choichesColors) == 2:
            print(choichesColors)

            # Check To See if it is already in the matrix
            key = "".join(choichesColors).upper();
            print(key)
            filtered_keys = getMovementFilteredKeys()

            if key in filtered_keys:
                return key
            # Postion already taken
            print("Position is not empty")
            choichesColors = []


calibrate()
drawBoard()

game = Game()

game.startGame()











