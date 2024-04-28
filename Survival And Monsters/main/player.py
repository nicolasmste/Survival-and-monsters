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
        self.hitBox = [0,0]
        self.speed = 7 #vitesse du joueur
        self.old_pos = self.pos.copy()
        self.HP = 200
        self.maxHP = 200
        self.degat = 5
        self.ratio = self.HP / self.maxHP

        #barre de vie
        self.sprite_HP = pygame.image.load('Sprites/Bars/hpBarGIF.png')
        self.HPIMAGES = [self.get_image(self.sprite_HP, 0+j*64 , 0 , 64, 64) for j in range (0,13)]
        
        self.HPIMAGE = self.HPIMAGES[0]
        self.rectHP = self.HPIMAGE.get_rect()

        #expérience
        self.XP = 0
        self.coeffXP = 1.5
        self.maxXP = 10 
        self.LVL = 0
        self.totalXP = 0
        self.xpratio = self.XP / self.maxXP 

        self.killcount = 0
        
        self.range = 250
        self.attackDelay = 0.5
        self.fireDelay = 10
        
        self.zoneDelay = 0.5
        self.zoneRange = 150# cercle de 150 px de rayon
        self.zoneDegat = 50
        self.zoneSpeed  = 10#vitesse à laquelle la zone grossi  
        self.isZone = False# booléen ppour savoir si une attaque de zone est lancé
        self.invincibl = 1 #periode pendant laquelle

    def XPmanage(self):#gestion de l'expérience
        if self.XP >= self.maxXP and self.LVL<999 :
            self.XP = self.XP - self.maxXP
            self.totalXP += self.maxXP
            self.maxXP = ceil(self.maxXP * self.coeffXP)
            self.LVL += 1 

    def go_left(self): self.pos[0] -= self.speed

    def go_right(self): self.pos[0] += self.speed

    def go_up(self): self.pos[1] -= self.speed

    def go_down(self): self.pos[1] += self.speed

    def end(self):
        if self.HP <= 0:
            print("game over")
            print("nombre de kill : ", self.killcount)
            return True
        return False
            #faire un fichier qui enregistre les scores à ouvrir en 'r+' :
            #   le temps -> créer une variable temps début et temps fin
            #   le nb de kill
            #   le nb de vague
            #   le niveau
            

    def update(self):#actualisation de la position
        self.rect.topleft = self.pos  #position

    def get_image(self, myimage, x, y, x1, y1):
        image = pygame.Surface([x1, y1]) #surface occupée sur le jeu
        image.blit(myimage, (0, 0), (x, y, x1, y1)) #Origine du crop et coordonnées de fin du crop
        return image
        