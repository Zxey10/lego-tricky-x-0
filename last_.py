from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, \
    not_equal_to
import math

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


def rotateRobot(direction: int):
    # -100 - LEFT
    # 100 - RIGHT
    # moveRobot(rotateRobotSize)

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
    # moveRobot(rotateRobotSize)


def calculateDirection(dir_: int):
    if dir_ % 2 == 0:
        # LEFT
        return -100
    # RIGHT
    return 100


def goToRR():
    moveRobot(10 + offset)
    rotateRobot(100)

    moveRobot(14)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-14)
    rotateRobot(-100)

    moveRobot(-10 - offset)
    # boardMatrix[0][0] = '+'


def goToGR():
    moveRobot(10 + offset)
    rotateRobot(100)

    moveRobot(10)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-10)
    rotateRobot(-100)

    moveRobot(-10 - offset)
    # boardMatrix[0][0] = '+'


def goToBR():
    moveRobot(10 + offset)
    rotateRobot(100)

    moveRobot(6)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-6)
    rotateRobot(-100)

    moveRobot(-10 - offset)
    # boardMatrix[0][0] = '+'


def goToBG():
    moveRobot(6 + offset)
    rotateRobot(100)

    moveRobot(6)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-6)
    rotateRobot(-100)

    moveRobot(-6 - offset)
    # boardMatrix[0][0] = '+'


def goToBB():
    moveRobot(2 + offset)
    rotateRobot(100)

    moveRobot(6)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-6)
    rotateRobot(-100)

    moveRobot(-2 - offset)
    # boardMatrix[0][0] = '+'


def goToRG():
    moveRobot(6 + offset)
    rotateRobot(100)

    moveRobot(14)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-14)
    rotateRobot(-100)

    moveRobot(-6 - offset)
    # TODO UPDATE MATRIX


def goToGG():
    moveRobot(6 + offset)
    rotateRobot(100)

    moveRobot(10)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-10)
    rotateRobot(-100)

    moveRobot(-6 - offset)
    # TODO UPDATE MATRIX


def goToGB():
    moveRobot(2 + offset)
    rotateRobot(100)

    moveRobot(10)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-10)
    rotateRobot(-100)

    moveRobot(-2 - offset)
    # TODO UPDATE MATRIX


def goToRB():
    moveRobot(2 + offset)
    rotateRobot(100)

    moveRobot(14)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-14)
    rotateRobot(-100)

    moveRobot(-2 - offset)
    # boardMatrix[0][0] = '+'


def goToRB():
    moveRobot(2 + offset)
    rotateRobot(100)

    moveRobot(14)
    moveRobot(-robotError)
    lowerPen()
    raisePen()
    moveRobot(robotError)

    moveRobot(-14)
    rotateRobot(-100)

    moveRobot(-2 - offset)
    # boardMatrix[0][0] = '+'


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
            choichesColors.append(color[0])
            print('blue')
            wait_for_seconds(3)
        elif color == 'red':
            choichesColors.append(color[0])
            wait_for_seconds(3)
            print('red')
        if len(choichesColors) == 2:
            print(choichesColors)
            return choichesColors


calibrate()

drawBoard()

goToRR()
goToRG()
goToRB()

goToGR()
goToGG()
goToGB()

goToBR()
goToBG()
goToBB()









