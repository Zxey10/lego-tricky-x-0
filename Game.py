import time
import turtle

from Player import Player
import Robot


class Game:
    robotPlayer = Player.X
    humanPlayer = Player.O
    playerTurn = Player.X
    isGameOver = False
    isRobotFirst = True
    loops = 0
    winner = None
    multiplier = 10

    def __init__(self, player: Player, board: Robot.Board, robot: Robot):
        self.player = player
        self.board = board
        self.robot = robot

    def startGame(self):
        turtle.speed(1)
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
        print(f"Robot Drawing X at {randomPlace}")
        self.robot.drawPlus()
        self.changeTurn()
        return True

    def drawHumanPlayer(self) -> bool:
        randomPlace = self.robot.pickRandomPlace(self.board, player=self.playerTurn)
        if randomPlace is None:
            print("No Places Left")
            return False
        self.robot.getTo(self.robot.pos, randomPlace)
        print(f"Human Drawing O at {randomPlace}")
        self.robot.drawMinus()
        self.changeTurn()
        return True

    def changePenColor(self):
        turtle.colormode(255)
        turtle.pencolor(50, 168, 82)
    def drawWinnerDiagonallyPaths(self, x: int, y: int, orientation: Robot.Orientation):
        self.changePenColor()
        self.robot.getTo(self.robot.pos, {'x': x, 'y': y})
        self.robot.lowerPen()
        self.robot.moveRobot(amount=self.board.gridSize,orientation=orientation)
        self.robot.raisePen()

    def drawWinnerPath(self, xEnd: int, yEnd: int, x: int, y: int):
        self.changePenColor()
        self.robot.getTo(self.robot.pos, {'x': x, 'y': y})
        self.robot.lowerPen()
        self.robot.getTo(self.robot.pos, {'x': xEnd, 'y': yEnd})
        self.robot.raisePen()

    def drawRowsWinnerPaths(self, row: int):
        #1 Row
        if row == 1:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize // 2, x=0,
                                y=-self.board.cellSize // 2)
        #2 Row
        if row == 2:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize // 2, x=0,
                                y=-(self.board.cellSize + self.board.cellSize // 2))
        #3 Row
        if row == 3:
            self.drawWinnerPath(xEnd=self.board.gridSize, yEnd=-self.board.cellSize * 2 - self.board.cellSize//2, x=0,
                            y=-self.board.cellSize * 2 - self.board.cellSize//2)

    def drawColsWinnerPaths(self, col: int):
        #1 Col
        if col == 1:
            self.drawWinnerPath(xEnd=self.board.cellSize // 2, yEnd=-self.board.gridSize, x=self.board.cellSize // 2,
                            y=0)
        #2 Col
        if col == 2:
            self.drawWinnerPath(xEnd=self.board.cellSize + self.board.cellSize // 2, yEnd=-self.board.gridSize,
                            x=self.board.cellSize + self.board.cellSize // 2,
                            y=0)
        #3 Col
        if col == 3:
            self.drawWinnerPath(xEnd=self.board.cellSize * 2 + self.board.cellSize//2, yEnd=-self.board.gridSize, x=self.board.cellSize * 2 + self.board.cellSize//2,
                            y=0)

    def drawDiagonalsWinnerPaths(self, diag: int):
        #First Diagonal
        if diag == 1:
            self.drawWinnerDiagonallyPaths(x=0, y=0, orientation=Robot.Orientation.DIAG_F)
        #Second Diagonal
        if diag == 2:
            self.drawWinnerDiagonallyPaths(x=self.board.gridSize, y=0, orientation=Robot.Orientation.DIAG_S)
    def checkForWinner(self) -> [str, bool]:
        board = self.board.boardMatrix

        # Rows
        # Player X
        if board[0][0] == Player.X and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            self.drawRowsWinnerPaths(1)
            return [f"{Player.X} wins", True]

        if board[1][0] == Player.X and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            self.drawRowsWinnerPaths(2)
            return [f"{Player.X} wins", True]

        if board[2][0] == Player.X and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            self.drawRowsWinnerPaths(3)
            return [f"{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            self.drawRowsWinnerPaths(1)
            return [f"{Player.O} wins", True]

        if board[1][0] == Player.O and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            self.drawRowsWinnerPaths(2)
            return [f"{Player.O} wins", True]

        if board[2][0] == Player.O and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            self.drawRowsWinnerPaths(3)
            return [f"{Player.O} wins", True]

        # Columns
        # Player X
        if board[0][0] == Player.X and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            self.drawColsWinnerPaths(1)
            return [f"{Player.X} wins", True]

        if board[0][1] == Player.X and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            self.drawColsWinnerPaths(2)
            return [f"{Player.X} wins", True]

        if board[0][2] == Player.X and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            self.drawColsWinnerPaths(3)
            return [f"{Player.X} wins", True]

        # Player O
        if board[0][0] == Player.O and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            self.drawColsWinnerPaths(1)
            return [f"{Player.O} wins", True]

        if board[0][1] == Player.O and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            self.drawColsWinnerPaths(2)
            return [f"{Player.O} wins", True]

        if board[0][2] == Player.O and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            self.drawColsWinnerPaths(3)
            return [f"{Player.O} wins", True]

        #Diagonal_F

        #Player X
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

        emptyCenterPoints = list(filter(lambda x: x['isEmpty'], self.board.centerPoints))
        if len(emptyCenterPoints) == 0:
            print("Tie")
            return ["Tie", True]

        return ["", False]

    def gameOver(self):
        self.isGameOver = True
