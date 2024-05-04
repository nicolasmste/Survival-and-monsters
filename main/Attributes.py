import pygame
from ennemis import *

def get_image(attribute, x, y, x2,y2):
    image = pygame.Surface([x2, y2]) #surface occupée sur le jeu
    image.blit(attribute, (0, 0), (x, y, x2, y2)) #Origine du crop et coordonnées de fin du crop
    return image

#STATS ET IMAGES DES DIFFERENTS ENNEMIES
class slime():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites/Slime/slime.png')
        self.imageliste = [get_image(self.sprite_sheet,j*32,0,32,32) for j in range(0,6)]
        self.it = 0
        self.image = self.imageliste[0]
        self.delay = 10
        self.xp = 5
        self.HP = 10
        self.maxHP = 10

        self.speed = 1
        self.normalSpeed = 1 

        self.attack = 10
        self.normalAttack = 10

        self.rect = self.image.get_rect()


class kingslime():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites/King Slime/kingslime.png')
        self.imageliste = [get_image(self.sprite_sheet,j*32, 0,32,32) for j in range(0,5)]
        self.it = 0
        self.image = self.imageliste[0]
        self.HP = 10
        self.maxHP = 10
        self.speed = 1.25
        self.delay = 10
        self.normalSpeed = 1 
        self.xp = 10
        self.attack = 15
        self.normalAttack = 15
        self.rect = self.image.get_rect()

class Orc():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites/ORC/ORC.png')
        self.imageliste = [get_image(self.sprite_sheet,0, 0,64,64),get_image(self.sprite_sheet,64, 0,64,64)]
        self.it = 0
        self.image = self.imageliste[1]
        self.HP = 10
        self.maxHP = 10
        self.delay = 10
        self.speed = 0.5
        self.normalSpeed = 0.5
        self.attack = 50
        self.xp = 15
        self.normalAttack = 50
        self.rect = self.image.get_rect()
      
class Bat():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites/Boss/batright2.png')
        self.sprite_sheet2 = pygame.image.load('Sprites\Boss\DROITMurcielago1.png')
        self.sprite_sheet3 = pygame.image.load('Sprites\Boss\DROITMurcielago3.png')
        self.imageliste = [get_image(self.sprite_sheet,0, 0,32,32),get_image(self.sprite_sheet3,0, 0,32,32),get_image(self.sprite_sheet2,0, 0,32,32)]
        self.it = 0
        self.image = self.imageliste[0]
        self.delay = 10
        self.HP = 1
        self.xp = 1
        self.maxHP = 1
        self.speed = 5
        self.normalSpeed = 5
        self.attack = 5
        self.normalAttack = 5
        self.rect = self.image.get_rect()