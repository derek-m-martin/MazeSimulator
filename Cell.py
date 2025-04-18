class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.isVisited = False

    def changeWall(self, side, state):
        if side in self.walls:
            self.walls[side] = state

    def hasTopWall(self):
        return self.walls['top']

    def hasBottomWall(self):
        return self.walls['bottom']

    def hasLeftWall(self):
        return self.walls['left']

    def hasRightWall(self):
        return self.walls['right']