import Player
import Robot
import Board
import turtle
import Game

turtle.speed(1)
multiplier = 10

# Board
board = Board.Board(_cellSize=4 * multiplier, _gridSize=12 * multiplier, _gridWidth=3)

# Robot
robot = Robot.Robot()

# Player
player = Player.Player()

# Draw Board
board.drawBoard(robot=robot)

game = Game.Game(robot=robot, player=player, board=board)
game.startGame()

print(board.boardMatrix)

turtle.Screen().exitonclick()
