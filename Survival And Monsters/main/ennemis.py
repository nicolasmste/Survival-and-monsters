from typing import Any
import pygame
#import Attacks

class ennemi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Slime/New Piskel (2).png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])

        self.HP = 1
        self.maxHP = 10
        
        self.speed = 1
        self.normalSpeed = 1
        
        self.attack = 10
        self.normalAttack = 10

        self.pos = [x,y]
        self.rect = self.image.get_rect()



    def moveTo(self,Px,Py):
        
        # Ex = self.pos[0]
        # Ey = self.pos[1]
        # if Ex < Px:
        #     if Ex + self.speed > Px :
        #         self.pos[0] = Px
        #     else:
        #         self.pos[0] += self.speed
        
        # else:
        #     if Ex - self.speed < Px :
        #         self.pos[0] = Px
        #     else:
        #         self.pos[0] -= self.speed
        
        # if Ey < Py:
        #     if Ey + self.speed > Py :
        #         self.pos[1] = Py
        #     else:
        #         self.pos[1] += self.speed
        
        # else:
        #     if Ey - self.speed < Py:
        #         self.pos[1] = Py
        #     else:
        #         self.pos[1] -= self.speed
        if Px != self.pos[0]:
            #self.pos[1] += self.speed * self.coef
            if self.pos[0] < Px:
                self.pos[1] += self.speed * self.coef
            else:
                self.pos[1] -= self.tan * self.coef
            
            if self.startPos[0]>self.cible[0]:
                self.pos[0] -= self.tan
            else :
                self.pos[0] += self.tan
        
        else:#il faut juste déplacer en Y
            if self.startPos[1]>self.cible[1]:
                self.pos[1] -= self.tan
            else :
                self.pos[1] += self.tan

    def damage(self,Ppos,PHP):
        if (self.pos[0] == Ppos[0]) and (self.pos[1] == Ppos[1]):
            PHP -= self.attack
            print("damage HP - ",self.attack)
            return PHP,True
        return PHP,False

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

