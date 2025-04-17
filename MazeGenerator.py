import pygame
from pygame.locals import *
import sys
from Cell import Cell

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