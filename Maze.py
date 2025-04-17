import pygame
import random
from Cell import Cell

LEFT, RIGHT, TOP, BOTTOM = 'left', 'right', 'top', 'bottom'
OPPOSITE_WALL = {LEFT: RIGHT, RIGHT: LEFT, TOP: BOTTOM, BOTTOM: TOP}

class Maze:
    def __init__(self, rows, cols, cell_size):
        if rows <= 0 or cols <= 0:
            raise ValueError("Maze dimensions must be positive")
        if cell_size <= 0:
            raise ValueError("Cell size must be positive")

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self._create_grid()
        self.start_cell = self.grid[0][0]
        self.end_cell = self.grid[rows - 1][cols - 1]
        self.pixel_width = self.cols * self.cell_size
        self.pixel_height = self.rows * self.cell_size

    def _create_grid(self):
        # just makes the grid based on the global params
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(Cell(i, j))
            grid.append(row)
        return grid

    def get_unvisited_neighbors(self, current_cell):
        # finds and returns the adjacent cells which have NOT been visited yet
        neighbors = []
        i, j = current_cell.i, current_cell.j

        if i > 0 and not self.grid[i - 1][j].isVisited:
            neighbors.append((self.grid[i - 1][j], TOP))

        if i < self.rows - 1 and not self.grid[i + 1][j].isVisited:
            neighbors.append((self.grid[i + 1][j], BOTTOM))

        if j > 0 and not self.grid[i][j - 1].isVisited:
            neighbors.append((self.grid[i][j - 1], LEFT))

        if j < self.cols - 1 and not self.grid[i][j + 1].isVisited:
            neighbors.append((self.grid[i][j + 1], RIGHT))

        return neighbors

    @staticmethod
    def remove_walls(cell1, cell2, direction_from_cell1):
        # does what the name implies
        cell1.changeWall(direction_from_cell1, False)
        cell2.changeWall(OPPOSITE_WALL[direction_from_cell1], False)

    def generate(self):
        # this actually makes the maze (opens certain walls based on random depth-first search)
        stack = []
        current_cell = self.start_cell
        current_cell.isVisited = True
        stack.append(current_cell)

        while stack:
            current_cell = stack[-1]
            unvisited_neighbors = self.get_unvisited_neighbors(current_cell)

            if unvisited_neighbors:
                next_cell_tuple = random.choice(unvisited_neighbors)
                next_cell = next_cell_tuple[0]
                direction = next_cell_tuple[1]

                self.remove_walls(current_cell, next_cell, direction)
                next_cell.isVisited = True
                stack.append(next_cell)
            else:
                stack.pop()
        print(f"Maze generated for {self.rows}x{self.cols} grid.")


    def draw(self, surface, offset_x, offset_y):

        # these 6 lines just individually draw the start (top left) and end (bottom right) in
        # colour unlike the typical white squares
        start_px = offset_x + self.start_cell.j * self.cell_size
        start_py = offset_y + self.start_cell.i * self.cell_size
        pygame.draw.rect(surface, (0, 255, 0), (start_px, start_py, self.cell_size, self.cell_size))

        end_px = offset_x + self.end_cell.j * self.cell_size
        end_py = offset_y + self.end_cell.i * self.cell_size
        pygame.draw.rect(surface, (255, 0, 0), (end_px, end_py, self.cell_size, self.cell_size))

        # draws the walls
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.grid[i][j]
                px = offset_x + j * self.cell_size
                py = offset_y + i * self.cell_size

                if cell.hasTopWall():
                    pygame.draw.line(surface, (0,0,0), (px, py), (px + self.cell_size, py), 1)
                if cell.hasBottomWall():
                    pygame.draw.line(surface, (0,0,0), (px, py + self.cell_size), (px + self.cell_size, py + self.cell_size), 1)
                if cell.hasLeftWall():
                    pygame.draw.line(surface, (0,0,0), (px, py), (px, py + self.cell_size), 1)
                if cell.hasRightWall():
                    pygame.draw.line(surface, (0,0,0), (px + self.cell_size, py), (px + self.cell_size, py + self.cell_size), 1)