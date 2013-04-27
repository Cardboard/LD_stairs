import pygame
import random

class Game:
    def __init__(self, font):
        print('GAME!')

    def run(self, display, events, keys, ticks):
        if keys[pygame.K_RIGHT]:
            print("RIGHT STEP")
        if keys[pygame.K_LEFT]:
            print("LEFT STEP")
