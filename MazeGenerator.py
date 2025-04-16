import pygame
from pygame.locals import *
import sys

pygame.init()

windowWidth = 800
windowHeight = 800
backgroundColor = (255, 255, 255)

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Maze Generator and Simulator")

window.fill(backgroundColor)

pygame.display.update()

running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
sys.exit()