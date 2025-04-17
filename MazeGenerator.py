import pygame
from pygame.locals import *
import sys
from Cell import Cell
import random

pygame.init()

# window parameters and creation
windowWidth = 800
windowHeight = 800
backgroundColor = (255, 255, 255)
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Maze Generator and Simulator")
window.fill(backgroundColor)
pygame.display.update()

# how many individual rows/cols within the maze
gridRows = 60
gridCols = 60
cellSize = 10
mazeGrid = []
sides = ['left', 'right', 'top', 'bottom']
excludeTop = [0, 1, 3]
excludeBottom = [0, 1, 2]
excludeRight = [0, 2, 3]
excludeLeft = [1, 2, 3]
excludeTopAndLeft = [1, 3]
excludeTopAndRight = [0, 3]
excludeBottomAndLeft = [1, 2]
excludeBottomAndRight = [0, 2]

# maze dimensions/size
maze_pixel_width = gridCols * cellSize
maze_pixel_height = gridRows * cellSize
offset_x = (windowWidth - maze_pixel_width) // 2
offset_y = (windowHeight - maze_pixel_height) // 2

# generate the grid!
for i in range(gridRows):
    grid_row = []
    for j in range(gridCols):
        cell_instance = Cell(i, j)
        grid_row.append(cell_instance)
    mazeGrid.append(grid_row)

print(f"Generated a {len(mazeGrid)}x{len(mazeGrid[0])} grid.")

# main loop
running = True

# currently randomly picks a wall to open up (1 side of each cell) NO ALGORITHM SO NOT A MAZE YET
def randomizeWalls():
    for i in range(gridRows):
        for j in range(gridCols):
            cell = mazeGrid[i][j]
            if cell.i == 0 and cell.j == 0:
                num = random.choice(excludeTopAndLeft)
            elif cell.i == 0 and cell.j == 59:
                num = random.choice(excludeTopAndRight)
            elif cell.i == 59 and cell.j == 0:
                num = random.choice(excludeBottomAndLeft)
            elif cell.i == 59 and cell.j == 59:
                num = random.choice(excludeBottomAndRight)
            elif cell.i == 0:
                num = random.choice(excludeTop)
            elif cell.i == 59:
                num = random.choice(excludeBottom)
            elif cell.j == 0:
                num = random.choice(excludeLeft)
            elif cell.j == 59:
                num = random.choice(excludeRight)
            else:
                num = random.randint(0, 3)

            cell.changeWall(sides[num])

randomizeWalls()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # clear window every loop
    window.fill(backgroundColor)

    # just setting the size of each cell
    cell_width = cellSize
    cell_height = cellSize

    # actually positions the cells on the screen
    for i in range(gridRows):
        for j in range(gridCols):
            cell = mazeGrid[i][j]
            px = offset_x + j * cell_width
            py = offset_y + i * cell_height

            # checks which walls a cell should have and then draws the cell accordingly
            if cell.hasTopWall():
                pygame.draw.line(window, (0,0,0), (px, py), (px + cell_width, py), 1)
            if cell.hasBottomWall():
                pygame.draw.line(window, (0,0,0), (px, py + cell_height), (px + cell_width, py + cell_height), 1)
            if cell.hasLeftWall():
                pygame.draw.line(window, (0,0,0), (px, py), (px, py + cell_height), 1)
            if cell.hasRightWall():
                pygame.draw.line(window, (0,0,0), (px + cell_width, py), (px + cell_width, py + cell_height), 1)

    pygame.display.flip()

pygame.quit()
sys.exit()