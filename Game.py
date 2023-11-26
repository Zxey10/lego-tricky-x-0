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

            if self.checkForWinner():
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

    def drawWinnerPath(self):
        print("Drawing winner path")
        pass

    def checkForWinner(self) -> bool:
        xCells = list(filter(lambda x: x['player'] == Player.X, self.board.centerPoints))
        oCells = list(filter(lambda x: x['player'] == Player.O, self.board.centerPoints))

        if len(xCells) < 3:
            return False

        if len(oCells) < 3:
            return False

        # TODO

        self.drawWinnerPath()
        return False

    def gameOver(self):
        self.isGameOver = True
