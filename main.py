import sys
import pygame
from pygame.locals import *
from mobs import Enemy, Player
from constants import *
from text import draw_text, init_text

Clock = pygame.time.Clock


def quit_game():
    pygame.quit()
    sys.exit()

def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_game()
            if event.key == K_SPACE:
                print("Space key pressed")

def main():
    pygame.init()
    init_text()

    dsurf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Hello Arp Souls')

    dsurf.fill(WHITE)


    P1 = Player()
    E1 = Enemy()

    # running = True
    while True:
        handle_events()
        P1.update()
        E1.move()

        dsurf.fill(WHITE)
        P1.draw(dsurf)
        E1.draw(dsurf)

        ms = Clock().tick_busy_loop(60)
        if ms == 0:
            ms = 1
        fps = 1000 / ms
        draw_text(dsurf, f"FPS: {fps:.2f}", BLACK, 10, 10)

        pygame.display.flip()



if __name__ == '__main__':
    main()