import sys

import pygame
import pygame_widgets
from pygame.locals import *
from pygame_widgets.button import Button as button

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

    the_maze = None

    def generate_maze_wilsons():
        nonlocal the_maze
        the_maze = Maze(GRID_ROWS, GRID_COLS, CELL_SIZE)
        the_maze.generate_wilsons()

    def generate_maze_dfs():
        nonlocal the_maze
        the_maze = Maze(GRID_ROWS, GRID_COLS, CELL_SIZE)
        the_maze.generate_random_depth_first()

    depth_first = button(
        window, 0, 0, 200, 50, text='Random Depth-First Search',
        fontSize=15, margin=20,
        inactiveColour=(209, 209, 209),
        pressedColour=(0, 255, 0), radius=20,
        onClick = generate_maze_dfs
    )

    kruskals = button(
        window, 200, 0, 200, 50, text = 'Kruskals',
        fontSize = 15, margin = 20,
        inactiveColour = (209, 209, 209),
        pressedColour = (0, 255, 0), radius = 20,
        onClick = lambda: print("not yet implemented")
    )

    prims = button(
        window, 400, 0, 200, 50, text = 'Prims',
        fontSize = 15, margin = 20,
        inactiveColour = (209, 209, 209),
        pressedColour = (0, 255, 0), radius = 20,
        onClick = lambda: print("not yet implemented")
    )

    wilsons = button(
        window, 600, 0, 200, 50, text='Wilsons',
        fontSize=15, margin=20,
        inactiveColour=(209, 209, 209),
        pressedColour=(0, 255, 0), radius=20,
        onClick = generate_maze_wilsons
    )

    hunt_and_kill = button(
        window, 0, 50, 200, 50, text = 'Hunt-and-Kill',
        fontSize = 15, margin = 20,
        inactiveColour = (209, 209, 209),
        pressedColour = (0, 255, 0), radius = 20,
        onClick = lambda: print("not yet implemented")
    )

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False

        window.fill(BACKGROUND_COLOR)

        pygame_widgets.update(events)

        if the_maze is not None:
            offset_x = (WINDOW_WIDTH - the_maze.pixel_width) // 2
            offset_y = (WINDOW_HEIGHT - the_maze.pixel_height) // 2
            the_maze.draw(window, offset_x, offset_y)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ ==  "__main__":
    main()