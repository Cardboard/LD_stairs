import sys
import pygame

from intro import *
from game import *
#from endgame import *

pygame.init()
fps = 60
clock = pygame.time.Clock()
ticks = pygame.time.get_ticks()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("stairs")
font = pygame.font.Font(None, 36)


state = 'intro'

intro = Intro(font)
game = Game(font)
#endgame = Endgame(font)


if __name__ == '__main__':
    while True:
        ticks = pygame.time.get_ticks() - ticks
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        if state == 'intro':
            intro.run(display, events, keys, ticks)
            if intro.finished:
                state = 'game'
        if state == 'game':
            game.run(display, events, keys, ticks)
        if state == 'endgame':
            endgame.run(display, events, keys, ticks)

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
                pygame.quit()

        clock.tick(fps)
