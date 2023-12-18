import Robot


# https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/class_motorpair.html
# https://primelessons.org/en/PyLessons.html
# https://www.antonsmindstorms.com/2021/01/14/advanced-undocumented-python-in-spike-prime-and-mindstorms-hubs/
# https://pybricks.com/projects/sets/mindstorms-robot-inventor/main-models/tricky/
# https://github.com/azzieg/mindstorms-inventor/tree/main/word_blocks
# https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/examples/programs
# https://github.com/LukaAndrojna/LEGO_Mindstorms_51515/blob/main/Tricky/first_project/drive2.py

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
        centerPoints: [dict[str, int | bool | Robot.Player]] = []

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

    def drawBoard(self, robot: Robot):
        for i in range(self.gridWidth - 1):
            robot.lowerPen()
            robot.rotateRobot(100, 90)
            robot.moveRobot(amount=self.gridSize, orientation=Robot.Orientation.DOWN)
            robot.raisePen()
            robot.rotateRobot(-100, 90)
            robot.moveRobot(amount=self.cellSize, orientation=Robot.Orientation.RIGHT)
            robot.rotateRobot(-100, 90)
            robot.lowerPen()
            robot.moveRobot(amount=self.gridSize, orientation=Robot.Orientation.UP)
            robot.rotateRobot(100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Robot.Orientation.RIGHT)

        robot.rotateRobot(100, 90)
        robot.moveRobot(amount=self.cellSize, orientation=Robot.Orientation.LEFT)
        for i in range(self.gridWidth - 1):
            robot.lowerPen()
            robot.rotateRobot(100, 90)
            robot.moveRobot(amount=self.gridSize, orientation=Robot.Orientation.LEFT)

            robot.rotateRobot(-100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Robot.Orientation.DOWN)

            robot.rotateRobot(-100, 90)
            robot.lowerPen()
            robot.moveRobot(amount=self.gridSize, orientation=Robot.Orientation.RIGHT)

            robot.rotateRobot(100, 90)
            robot.raisePen()
            robot.moveRobot(amount=self.cellSize, orientation=Robot.Orientation.DOWN)

        print(robot.pos)
