cellSize = 4
gridSize = 12
gridWidth = 4
gridHeight = 4
pairMotorSpeed = 15
rotateRobotSize = 4

boardMatrix = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
rotationMap = {
    'UP': 0,
    'LEFT': 0,
    'RIGHT': 0,
    'DOWN': 0
}


class Orientation:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    currentOrientation = "DOWN"


def raisePen():
    print("PEN IS UP")
    # pen_motor.run_for_degrees(-90)


def lowerPen():
    print("PEN IS DOWN")
    # pen_motor.run_for_degrees(90)


def moveRobot(amount):
    print("Moving on direction:", Orientation.currentOrientation, amount)
    # motor_pair.move(amount, 'cm')


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

    # motor_pair.move(360, 'degrees')


def rotateRobot(direction: int):
    # -100 - LEFT
    #  100 - RIGHT
    moveRobot(rotateRobotSize)

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

    # motor_pair.move(180, 'degrees', steering=direction)

    print("Rotate robot to:", direction, Orientation.currentOrientation)
    moveRobot(rotateRobotSize)


def calculateDirection(dir_: int):
    if dir_ % 2 == 0:
        # LEFT
        return -100
    # RIGHT
    return 100


def drawBoard():
    for i in range(gridWidth):
        lowerPen()
        moveRobot(gridSize)
        raisePen()

        rotateRobot(calculateDirection(i))
        moveRobot(cellSize)

        rotateRobot(calculateDirection(i))
        moveRobot(gridWidth)

    rotateRobot(calculateDirection(1))
    moveRobot(cellSize)
    for i in range(4):
        lowerPen()
        moveRobot(gridSize)
        raisePen()
        moveRobot(cellSize)
        rotateRobot(calculateDirection(i))
        moveRobot(cellSize)
        rotateRobot(calculateDirection(i))
        moveRobot(cellSize)


drawBoard()


