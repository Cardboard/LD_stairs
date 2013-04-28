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
if '-serious' in sys.argv:
    mode = True
else:
    mode = False
game = Game(display, font, mode)

text1 = "GAME OVER"
text2 = "PRESS SPACE TO TRY AGAIN"
gameoverMessage = [[font.render(text1, 1, (220,220,220)), font.size(text1)[0]],
                    [font.render(text2, 1, (220,220,220)), font.size(text2)[0]]]

if __name__ == '__main__':
    while True:
        ticks = pygame.time.get_ticks() - ticks
        if state == 'intro':
            intro.run(display, ticks)
            if intro.finished:
                state = 'game'
        if state == 'game':
            game.run(display, ticks)
            if game.gameOver():
                state = 'gameover'
        if state == 'gameover':
            display.fill((16,16,16))
            display.blit(gameoverMessage[0][0], (width/2-gameoverMessage[0][1]/2, 100))
            display.blit(gameoverMessage[1][0], (width/2-gameoverMessage[1][1]/2, 110+font.get_height()))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game.reset()
                    state = 'game'
                    print("RESTARTING GAME...")

        clock.tick(fps)
