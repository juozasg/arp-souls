import sys
import pygame
from pygame.locals import *

Clock = pygame.time.Clock

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    pygame.init()
    disp = pygame.display.set_mode((1920, 1080))
    disp.fill(WHITE)
    pygame.display.set_caption('Hello Arp Souls')

    # running = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        ms = Clock().tick_busy_loop(60)




if __name__ == '__main__':
    main()