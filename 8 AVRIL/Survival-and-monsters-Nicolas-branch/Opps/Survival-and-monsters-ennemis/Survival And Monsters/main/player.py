from typing import Any
import pygame
from Attacks import * 
from math import ceil

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Character/Base.png')
        self.image = self.get_image(self.sprite_sheet, 0, 0, 32, 32) #coordonées de début du get

        self.image.set_colorkey([0, 0, 0]) #on sup le noir
        self.rect = self.image.get_rect()
        self.pos = [x,y] #position du joueur
        self.speed = 7 #vitesse du joueur
        self.old_pos = self.pos.copy()
        #self.sprite = { }  dictionnaire des images
        #gestion de la vie
        self.HP = 200
        self.maxHP = 200
        self.ratio = self.HP / self.maxHP

        self.sprite_HP = pygame.image.load('Sprites/Bars/hpBarGIF.png')
        self.HPIMAGES = [self.get_image(self.sprite_HP, 0+j*64 , 0 , 64, 64) for j in range (0,13)]
        
        self.HPIMAGE = self.HPIMAGES[0]
        self.rectHP = self.HPIMAGE.get_rect()

        self.stats = 10
        self.killcount = 0
        self.range = 250
        self.attackDelay = 1
        self.fireDelay = 1
        #XP
        self.XP = 0
        self.coeffXP = 1.5
        self.maxXP = 10 
        self.LVL = 0
        self.totalXP = 0
        self.xpratio = self.XP / self.maxXP 

    def go_left(self): self.pos[0] -= self.speed

    def go_right(self): self.pos[0] += self.speed

    def go_up(self): self.pos[1] -= self.speed

    def go_down(self): self.pos[1] += self.speed

    

        
        
    def XPmanage(self):
        if self.XP >= self.maxXP and self.LVL<999 :
            self.XP = self.XP - self.maxXP
            self.totalXP += self.maxXP
            self.maxXP = ceil(self.maxXP * self.coeffXP)
            self.LVL += 1 
            

        


    def end(self):
        if self.HP <= 0:
            self.totalXP += self.XP
            print("game over")
            print("nombre de kill : ", self.killcount)
            print(f"mon xp: {self.totalXP} ")
            return True
        else: return False

    def update(self):#actualisation de la position
        if self.HP < 0: self.HP = 0
        self.xpratio = self.XP / self.maxXP
        self.ratio = self.HP / self.maxHP
        self.rect.topleft = self.pos  #position
    

    


    def get_image(self, myimage, x, y, x1, y1):
        image = pygame.Surface([x1, y1]) #surface occupée sur le jeu
        image.blit(myimage, (0, 0), (x, y, x1, y1)) #Origine du crop et coordonnées de fin du crop
        return image
        