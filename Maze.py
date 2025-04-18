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
        self.grid = self.create_grid ()
        self.start_cell = self.grid[0][0]
        self.end_cell = self.grid[rows - 1][cols - 1]
        self.pixel_width = self.cols * self.cell_size
        self.pixel_height = self.rows * self.cell_size

    def create_grid (self):
        # just makes the grid based on the global params
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(Cell(i, j))
            grid.append(row)
        return grid

    def get_neighbors(self, current_cell, visit_check):
        neighbors = []
        i, j = current_cell.i, current_cell.j
        if visit_check:
            if i > 0 and not self.grid[i - 1][j].isVisited:
                neighbors.append((self.grid[i - 1][j], TOP))
            if i < self.rows - 1 and not self.grid[i + 1][j].isVisited:
                neighbors.append((self.grid[i + 1][j], BOTTOM))
            if j > 0 and not self.grid[i][j - 1].isVisited and j != 0:
                neighbors.append((self.grid[i][j - 1], LEFT))
            if j < self.cols - 1 and not self.grid[i][j + 1].isVisited and j != self.cols - 1:
                neighbors.append((self.grid[i][j + 1], RIGHT))
        else:
            if i > 0:
                neighbors.append((self.grid[i - 1][j], TOP))
            if i < self.rows - 1:
                neighbors.append((self.grid[i + 1][j], BOTTOM))
            if j > 0 and j != 0:
                neighbors.append((self.grid[i][j - 1], LEFT))
            if j < self.cols - 1 and j != self.cols - 1:
                neighbors.append((self.grid[i][j + 1], RIGHT))
        return neighbors

    @staticmethod
    def remove_walls(cell1, cell2, direction_from_cell1):
        # does what the name implies
        cell1.changeWall(direction_from_cell1, False)
        cell2.changeWall(OPPOSITE_WALL[direction_from_cell1], False)

    def generate_random_depth_first(self):
        # creates a maze using a random depth-first search algorithm
        stack = []
        current_cell = self.start_cell
        current_cell.isVisited = True
        stack.append(current_cell)

        while stack:
            current_cell = stack[-1]
            unvisited_neighbors = self.get_neighbors(current_cell, True)

            if unvisited_neighbors:
                next_cell_tuple = random.choice(unvisited_neighbors)
                next_cell = next_cell_tuple[0]
                direction = next_cell_tuple[1]

                self.remove_walls(current_cell, next_cell, direction)
                next_cell.isVisited = True
                stack.append(next_cell)
            else:
                stack.pop()
        print(f"Maze generated for {self.rows}x{self.cols} grid using random depth-first search algorithm")

    # picks a random cell in the grid, if not visited, return it, otherwise repeat
    def pick_random_non_visited(self):
        found = False
        while not found:
            check = self.grid[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)]
            if not check.isVisited:
                return check
        return None

    # not my best work but literally just returns which direction connects the two provided cells
    def find_direction(self, current_focus, next_focus):
        if current_focus.i != next_focus.i:
            if current_focus.i > next_focus.i:
                return TOP
            else:
                return BOTTOM
        else:
            if current_focus.j > next_focus.j:
                return LEFT
            else:
                return RIGHT

    def walk(self, start_node):
        path = [start_node]
        curr = start_node

        # loop until one of the if statements returns (either all adjacent cells are visited or there are
        # non-visited adjacent cells and it randomly chooses one
        while True:
            neighbors_tuples = self.get_neighbors(curr, False)
            if not neighbors_tuples:
                return path, None

            next_cell = random.choice([n[0] for n in neighbors_tuples])

            if next_cell.isVisited:
                return path, next_cell

            elif next_cell in path:
                index = path.index(next_cell)
                path = path[:index + 1]
                curr = path[-1]

            else:
                path.append(next_cell)
                curr = next_cell

    def generate_wilsons(self):
        # generates a maze using wilsons algorithm

        if not self.grid:
            return

        # picks the random first cell for the first 'walk'
        first_cell = self.grid[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)]
        first_cell.isVisited = True
        remaining = (self.rows * self.cols) - 1

        # just loops until ALL cells have been marked visited meaning the full grid has been mapped (or mazed I could say)
        while remaining > 0:
            start_point = self.pick_random_non_visited()
            returned_path, connecting_cell = self.walk(start_point)

            if connecting_cell:
                last_cell_in_path = None
                for i in range(len(returned_path)):
                    current_cell = returned_path[i]

                    # if the current cell isnt visited then mark it as and deincrement
                    if not current_cell.isVisited:
                        current_cell.isVisited = True
                        remaining -= 1

                    # if a viable cell was found then find the direction that connects the prev and next
                    # then remove the walls separating them
                    if i + 1 < len(returned_path):
                        next_cell_in_path = returned_path[i + 1]
                        direction = self.find_direction(current_cell, next_cell_in_path)
                        self.remove_walls(current_cell, next_cell_in_path, direction)

                    last_cell_in_path = current_cell

                if last_cell_in_path:
                    direction_to_maze = self.find_direction(last_cell_in_path, connecting_cell)
                    self.remove_walls(last_cell_in_path, connecting_cell, direction_to_maze)
                else:
                    direction_to_maze = self.find_direction(start_point, connecting_cell)
                    self.remove_walls(start_point, connecting_cell, direction_to_maze)

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