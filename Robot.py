import random

from Player import Player
from Board import Board
from enum import Enum
import turtle


class Orientation(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    DIAG_F = "DIAG_F"
    DIAG_S = "DIAG_S"


class Robot:
    pos = {
        'x': 0,
        'y': 0
    }
    orientation: Orientation = Orientation.DOWN
    centerPoints: [dict[str, int | bool]] = []
    multiplier = 10

    @property
    def x(self):
        return self.pos['x']

    @property
    def y(self):
        return self.pos['y']

    def moveRobot(self, amount: int, orientation: Orientation):
        print(f"Moving robot {amount} on {orientation}:")
        match orientation:
            case Orientation.DOWN:
                self.pos['y'] += (amount * -1)
            case Orientation.UP:
                self.pos['y'] += (-amount * -1)
            case Orientation.RIGHT:
                self.pos['x'] += amount
            case Orientation.LEFT:
                self.pos['x'] += -amount
            case Orientation.DIAG_S:
                self.pos['x'] += amount
                self.pos['y'] -= amount
            case Orientation.DIAG_F:
                self.pos['x'] -= amount
                self.pos['y'] -= amount
        turtle.goto(self.x, self.y)

    def getTo(self, currPos: dict[str, int], nextPos: dict[str, int]):
        currX, currY = currPos['x'], currPos['y']
        nextX, nextY = nextPos['x'], nextPos['y']

        print(f"Get to x: {nextX}, y: {nextY}")

        if currX > nextX:
            self.orientation = Orientation.LEFT
            self.moveRobot(currX - nextX, self.orientation)
            turtle.goto(self.x, self.y)
        else:
            self.orientation = Orientation.RIGHT
            self.moveRobot(nextX - currX, self.orientation)
            turtle.goto(self.x, self.y)

        if currY > nextY:
            self.orientation = Orientation.UP
            self.moveRobot(nextY - currY, self.orientation)
            turtle.goto(self.x, self.y)
        else:
            self.orientation = Orientation.DOWN
            self.moveRobot(currY - nextY, self.orientation)
            turtle.goto(self.x, self.y)

        self.updateRobotCoordinates(nextX, nextY)

    def pickRandomPlace(self, board: Board, player: Player):
        emptyCenterPoints = list(filter(lambda x: x['isEmpty'], board.centerPoints))

        if len(emptyCenterPoints) == 0:
            return None
        else:
            print(f"{len(emptyCenterPoints)} cells remained")

        randomCell = random.choice(emptyCenterPoints)
        randomCellIndex = board.centerPoints.index(randomCell)
        board.centerPoints[randomCellIndex]['isEmpty'] = False
        board.centerPoints[randomCellIndex]['player'] = player

        print("Random cell")
        print(randomCell)

        for col in range(board.gridWidth):
            for row in range(board.gridWidth):
                target_x = (2 + col * 4) * self.multiplier
                target_y = (-2 - row * 4) * self.multiplier

                if randomCell['x'] == target_x and randomCell['y'] == target_y:
                    board.boardMatrix[row][col] = player

        print(randomCell)
        return randomCell

    def rotateRobot(self, direction: int, angle: int):
        # TODO
        if direction == 100:
            self.orientation = Orientation.RIGHT
            turtle.right(angle)
        else:
            turtle.left(angle)
            self.orientation = Orientation.LEFT

    def updateRobotCoordinates(self, x, y):
        self.pos['x'] = x
        self.pos['y'] = y

    def lowerPen(self):
        print("Pen is Up")
        turtle.pendown()

    def raisePen(self):
        print("Pen is Down")
        turtle.penup()

    def drawMinus(self):
        self.raisePen()
        self.moveRobot(Player.playerOffset, Orientation.LEFT)
        self.lowerPen()
        self.moveRobot(Player.playerSize, Orientation.RIGHT)
        self.raisePen()
        self.moveRobot(Player.playerOffset, Orientation.LEFT)

    def drawPlus(self):
        self.drawMinus()
        self.raisePen()
        self.moveRobot(Player.playerOffset, Orientation.UP)
        self.lowerPen()
        self.moveRobot(Player.playerSize, Orientation.DOWN)
        self.raisePen()
        self.moveRobot(Player.playerOffset, Orientation.UP)
