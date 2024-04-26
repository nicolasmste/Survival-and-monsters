from typing import Any
import pygame
from Attacks import * 

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Character/Base.png')
        self.image = self.get_image(0, 0) #coordonées de début du get
        self.image.set_colorkey([0, 0, 0]) #on sup le noir
        self.rect = self.image.get_rect()
        
        self.pos = [x,y] #position du joueur
        self.speed = 7 #vitesse du joueur
        self.old_pos = self.pos.copy()
        #self.sprite = { }  dictionnaire des images
        self.HP = 200
        self.maxHP = 200
        self.degat = 2


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

    


    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
        return image
        