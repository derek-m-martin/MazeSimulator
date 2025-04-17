import pygame
from pygame.locals import *
import sys
from Maze import Maze

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)

GRID_ROWS = 60
GRID_COLS = 60
CELL_SIZE = 10

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Generator")
    clock = pygame.time.Clock()

    the_maze = Maze(GRID_ROWS, GRID_COLS, CELL_SIZE)
    the_maze.generate()

    offset_x = (WINDOW_WIDTH - the_maze.pixel_width) // 2
    offset_y = (WINDOW_HEIGHT - the_maze.pixel_height) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        window.fill(BACKGROUND_COLOR)
        the_maze.draw(window, offset_x, offset_y)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()