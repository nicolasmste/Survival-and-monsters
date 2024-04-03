import pygame
from game import *


if __name__ == '__main__':
    pygame.init()   #initialisation du jeu
    game = Play()
    game.run()

