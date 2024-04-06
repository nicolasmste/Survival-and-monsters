import pygame
from ennemis import *

def get_image(attribute, x, y, x2,y2):
    image = pygame.Surface([x2, y2]) #surface occupée sur le jeu
    image.blit(attribute, (0, 0), (x, y, x2, y2)) #Origine du crop et coordonnées de fin du crop
    return image


class slime():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites\Slime\slime.png')
        self.image = get_image(self.sprite_sheet,0, 0,32, 32)
        self.image.set_colorkey([0, 0, 0])

        self.HP = 10
        self.maxHP = 10

        self.speed = 1
        self.normalSpeed = 1 

        self.attack = 10
        self.normalAttack = 10

        self.rect = self.image.get_rect()


class kingslime():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites\King Slime\kingslime.png')
        self.image = get_image(self.sprite_sheet,0, 0 , 32,32)
        self.image.set_colorkey([0, 0, 0])
        self.HP = 50
        self.maxHP = 50
        self.speed = 1.25
        self.normalSpeed = 1 
        self.attack = 15
        self.normalAttack = 15
        self.rect = self.image.get_rect()
      


class Orc(pygame.sprite.Sprite):
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites\ORC\ORC.png')
        self.image = get_image(self.sprite_sheet,0, 0,64,64)
        self.image.set_colorkey([0, 0, 0])
        self.HP = 50000
        self.maxHP = 50000
        self.speed = 0.5
        self.normalSpeed = 0.5
        self.attack = 50
        self.normalAttack = 50
        self.rect = self.image.get_rect()
      
class BOSS():
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Sprites/Boss/boss-1.png.png')
        self.image = get_image(self.sprite_sheet,0, 0,256,256)
        self.image.set_colorkey([0, 0, 0])
        self.HP = 500000000000000000000
        self.maxHP = 50000000000000000000000000000000000000
        self.speed = 0.5
        self.normalSpeed = 0.5
        self.attack = 50
        self.normalAttack = 50
        self.rect = self.image.get_rect()

