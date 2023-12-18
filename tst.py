import random


class Player:
    X = "+"
    O = '-'
    playerSize = 2
    playerOffset = 1


class Orientation:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    DIAG_F = "DIAG_F"
    DIAG_S = "DIAG_S"


class Board:
    boardMatrix = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    centerPoints: [dict[str, int | bool]] = []

    def __init__(self, _cellSize: int, _gridSize: int, _gridWidth: int):
        self.cellSize = _cellSize
        self.gridSize = _gridSize
        self.gridWidth = _gridWidth
        self.initCenterPoints()

    def initCenterPoints(self):
        self.centerPoints = self.calculateCenterCellPosition()

    def calculateCenterCellPosition(self):
        gridWidth = self.gridWidth
        cellSize = self.cellSize
        currentX = -cellSize / 2
        currentY = -cellSize / 2
        centerPoints: [dict[str, int | bool | None | str]] = []

        for i in range(gridWidth):
            currentY += cellSize
            for j in range(gridWidth):
                currentX += cellSize
                centerPoints.append({
                    'x': currentX,
                    'y': -currentY,
                    'isEmpty': True,
                    'player': None
                })
            currentX = -cellSize / 2
        return centerPoints

    def drawBoard(self, robot):
        for i in range(self.gridWidth - 1):
            robot.lowerPen()
            robot.rotateRobot(100, 90)
            robot.moveRobot(amount=self.gridSize, orientation=Orientation.DOWN)
            robot.raisePen()
            robot.rotateRobot(-100, 90)
            robot.moveRobot(amount=self.cellSize, orientation=Orientation.RIGHT)
            robot.rotateRobot(-100, 90)
            robot.lowerPen()
            robot.moveRobot(amount=self.gridSize, orientation=Orientation.UP)
            robot.rotateRobot(100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Orientation.RIGHT)

        robot.rotateRobot(100, 90)
        robot.moveRobot(amount=self.cellSize, orientation=Orientation.LEFT)
        for i in range(self.gridWidth - 1):
            robot.lowerPen()
            robot.rotateRobot(100, 90)
            robot.moveRobot(amount=self.gridSize, orientation=Orientation.LEFT)

            robot.rotateRobot(-100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Orientation.DOWN)

            robot.rotateRobot(-100, 90)
            robot.lowerPen()
            robot.moveRobot(amount=self.gridSize, orientation=Orientation.RIGHT)

            robot.rotateRobot(100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Orientation.DOWN)

        print(robot.pos)


class Robot:
    pos = {
        'x': 0,
        'y': 0
    }
    orientation: str = Orientation.DOWN
    centerPoints: [dict[str, int | bool]] = []
    multiplier = 1

    @property
    def x(self):
        return self.pos['x']

    @property
    def y(self):
        return self.pos['y']

    def moveRobot(self, amount, orientation):

        if orientation == "DOWN":
            self.pos['y'] += (amount * -1)
        elif orientation == "UP":
            self.pos['y'] += (-amount * -1)
        elif orientation == "RIGHT":
            self.pos['x'] += amount
        elif orientation == "LEFT":
            self.pos['x'] += -amount
        elif orientation == "DIAG_F":
            self.pos['x'] += amount
            self.pos['y'] -= amount
        elif orientation == "DIAG_S":
            self.pos['x'] -= amount
            self.pos['y'] -= amount

        # motor_pair.move(amount, 'cm')
        # turtle.goto(self.x, self.y)

    def getTo(self, currPos: dict[str, int], nextPos: dict[str, int]):
        currX, currY = currPos['x'], currPos['y']
        nextX, nextY = nextPos['x'], nextPos['y']

        # print(f"Get to x: {nextX}, y: {nextY}")

        if currX > nextX:
            self.orientation = Orientation.LEFT
            self.moveRobot(currX - nextX, self.orientation)
            # turtle.goto(self.x, self.y)
        else:
            self.orientation = Orientation.RIGHT
            self.moveRobot(nextX - currX, self.orientation)
            # turtle.goto(self.x, self.y)

        if currY > nextY:
            self.orientation = Orientation.UP
            self.moveRobot(nextY - currY, self.orientation)
            # turtle.goto(self.x, self.y)
        else:
            self.orientation = Orientation.DOWN
            self.moveRobot(currY - nextY, self.orientation)
            # turtle.goto(self.x, self.y)

        self.updateRobotCoordinates(nextX, nextY)

    def pickRandomPlace(self, board: Board, player: str):
        emptyCenterPoints = list(filter(lambda x: x['isEmpty'], board.centerPoints))
        print("CENTER POINTS")
        print(board.centerPoints)

        if len(emptyCenterPoints) == 0:
            return None
        else:
            print(len(emptyCenterPoints))

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

        print("BOARD MATRIX")
        print(board.boardMatrix)
        return randomCell

    def rotateRobot(self, direction: int, angle: int):

        if direction == 100:
            self.orientation = Orientation.RIGHT
        else:
            # turtle.left(angle)
            self.orientation = Orientation.LEFT

        # motor_pair.move(180, 'degrees')
        # motor_pair.move(184, 'degrees', steering=direction)
        # motor_pair.move(-163, 'degrees')

    def updateRobotCoordinates(self, x, y):
        self.pos['x'] = x
        self.pos['y'] = y

    def lowerPen(self):
        print("Pen is Up")
        # pen_motor.run_for_degrees(90)

    def raisePen(self):
        print("Pen is Down")
        # pen_motor.run_for_degrees(-90)

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


###############################################
# motor_pair.set_default_speed(pairMotorSpeed)
# pen_motor.run_to_position(165, 'shortest path')


class Game:
    robotPlayer = Player.X
    humanPlayer = Player.O
    playerTurn = Player.X
    isGameOver = False
    isRobotFirst = True
    loops = 0
    multiplier = 1

    def __init__(self, player: Player, board: Board, robot: Robot):
        self.player = player
        self.board = board
        self.robot = robot

    def startGame(self):
        # turtle.speed(1)
        while not self.isGameOver:
            self.loops += 1
            if self.playerTurn == Player.X:
                self.drawRobotPlayer()
            else:
                self.drawHumanPlayer()

            [winnerText, status] = self.checkForWinner()
            if status:
                print(winnerText)
                break

            if self.loops >= 9:
                self.gameOver()

    def changeTurn(self):
        if self.playerTurn == Player.X:
            self.playerTurn = Player.O
        else:
            self.playerTurn = Player.X

    def drawRobotPlayer(self) -> bool:
        randomPlace = self.robot.pickRandomPlace(self.board, player=self.playerTurn)
        if randomPlace is None:
            print("No Places Left")
            return False
        self.robot.getTo(self.robot.pos, randomPlace)
        print(randomPlace)
        self.robot.drawPlus()
        self.changeTurn()
        return True

    def drawHumanPlayer(self) -> bool:
        randomPlace = self.robot.pickRandomPlace(self.board, player=self.playerTurn)
        if randomPlace is None:
            print("No Places Left")
            return False
        self.robot.getTo(self.robot.pos, randomPlace)
        # print(f"Human Drawing O at {randomPlace}")
        self.robot.drawMinus()
        self.changeTurn()
        return True

    def changePenColor(self):
        # turtle.colormode(255)
        # turtle.pencolor(50, 168, 82)
        pass

    def drawWinnerDiagonallyPaths(self, x: int, y: int, orientation: Orientation):
        self.changePenColor()
        self.robot.getTo(self.robot.pos, {'x': x, 'y': y})
        self.robot.lowerPen()
        self.robot.moveRobot(amount=self.board.gridSize, orientation=orientation)
        self.robot.raisePen()

    def drawWinnerPath(self, xEnd: int, yEnd: int, x: int, y: int):
        self.changePenColor()
        self.robot.getTo(self.robot.pos, {'x': x, 'y': y})
        self.robot.lowerPen()
        self.robot.getTo(self.robot.pos, {'x': xEnd, 'y': yEnd})
        self.robot.raisePen()

    def drawRowsWinnerPaths(self, row: int):
        # 1 Row
        if row == 1:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize // 2, x=0,
                                y=-self.board.cellSize // 2)
        # 2 Row
        if row == 2:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize // 2, x=0,
                                y=-(self.board.cellSize + self.board.cellSize // 2))
        # 3 Row
        if row == 3:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize * 2 - self.board.cellSize // 2, x=0,
                                y=-self.board.cellSize * 2 - self.board.cellSize // 2)

    def drawColsWinnerPaths(self, col: int):
        # 1 Col
        if col == 1:
            self.drawWinnerPath(xEnd=self.board.cellSize // 2, yEnd=-self.board.gridSize, x=self.board.cellSize // 2,
                                y=0)
        # 2 Col
        if col == 2:
            self.drawWinnerPath(xEnd=self.board.cellSize + self.board.cellSize // 2, yEnd=-self.board.gridSize,
                                x=self.board.cellSize + self.board.cellSize // 2,
                                y=0)
        # 3 Col
        if col == 3:
            self.drawWinnerPath(xEnd=self.board.cellSize * 2 + self.board.cellSize // 2, yEnd=-self.board.gridSize,
                                x=self.board.cellSize * 2 + self.board.cellSize // 2,
                                y=0)

    def drawDiagonalsWinnerPaths(self, diag: int):
        # First Diagonal
        if diag == 1:
            self.drawWinnerDiagonallyPaths(x=0, y=0, orientation=Orientation.DIAG_F)
        # Second Diagonal
        if diag == 2:
            self.drawWinnerDiagonallyPaths(x=self.board.gridSize, y=0, orientation=Orientation.DIAG_S)

    def checkForWinner(self) -> [str, bool]:
        board = self.board.boardMatrix

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

        emptyCenterPoints = list(filter(lambda x: x['isEmpty'], self.board.centerPoints))
        if len(emptyCenterPoints) == 0:
            print("Tie")
            return ["Tie", True]

        return ["", False]

    def gameOver(self):
        self.isGameOver = True


multiplier = 1

# Board
board = Board(_cellSize=4 * multiplier, _gridSize=12 * multiplier, _gridWidth=3)

# Robot
robot = Robot()

# Player
player = Player()

# Draw Board
board.drawBoard(robot=robot)

game = Game(robot=robot, player=player, board=board)
game.startGame()

print(board.boardMatrix)
