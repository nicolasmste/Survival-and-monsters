from typing import Any
import pygame
from Attributes import *
from random import randint


types = [slime(),kingslime(),Orc(),Bat()]
def newtype():
    return types[randint(0,3)]


class ennemi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.type = newtype()
        self.sprite_sheet = pygame.image.load('Sprites/Tengu/Tengu.png')
        self.image = self.type.image
        self.givenxp = 2

        self.HP = self.type.HP
        self.maxHP = self.type.maxHP
        
        self.speed = self.type.speed
        self.normalSpeed = self.type.normalSpeed
        
        self.attack = self.type.attack
        self.normalAttack = self.type.normalAttack

        self.pos = [x,y]
        self.rect = self.image.get_rect()



    def moveTo(self,Px,Py):
        
        Ex = self.pos[0]
        Ey = self.pos[1]
        if Ex < Px:
            if Ex + self.speed > Px :
                self.pos[0] = Px
            else:
                self.pos[0] += self.speed
        
        else:
            if Ex - self.speed < Px :
                self.pos[0] = Px
            else:
                self.pos[0] -= self.speed
        
        if Ey < Py:
            if Ey + self.speed > Py :
                self.pos[1] = Py
            else:
                self.pos[1] += self.speed
        
        else:
            if Ey - self.speed < Py:
                self.pos[1] = Py
            else:
                self.pos[1] -= self.speed

    def damage(self,Ppos,PHP):
        if (self.pos[0] == Ppos[0]) and (self.pos[1] == Ppos[1]):
            PHP -= self.attack
            print("damage HP - ",self.attack)
            del self
        return PHP

    def dead(self,Ppos):
        r = 13
        if (self.pos[0] <= Ppos[0]+r and self.pos[0] >= Ppos[0]-r) and (self.pos[1] <= Ppos[1]+r and self.pos[1] >= Ppos[1]-r):#si la position en X est compris entre PosPx + a et PosPx -a
            return True

    def update(self):
        self.rect.topleft = self.pos 

    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
        return image

