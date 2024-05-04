import pygame
from os import path
from game import *

if __name__ == '__main__':
    if not(path.exists("main/Score.csv")):#Si c'est la premiere fois qu'on lance le jeu, il faut créer le fichier score
        f = open("main/Score.csv","w")
        f.close()
        print("le fichier Score.csv à été crée dans main")
    else :
         print("le fichier existait deja")
    
    pygame.init()   #initialisation du jeu
    game = Play()
    game.run()