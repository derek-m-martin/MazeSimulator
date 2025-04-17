class Cell:
    # initializes the cell with its location in the grid/array
    def __init__(self, i, j):
        self.i = i
        self.j = j

        # currently sets walls on all sides but this will be dealt with through maze generation algos in the main file
        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }

    # simple checks so the main file knows which walls to draw (definitely could do better than 4 methods maybe ill refactor later)
    def hasTopWall(self):
        return self.walls["top"]

    def hasRightWall(self):
        return self.walls["right"]

    def hasBottomWall(self):
        return self.walls["bottom"]

    def hasLeftWall(self):
        return self.walls["left"]