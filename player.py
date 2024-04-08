from typing import Any
import pygame
from Attacks import *
from game import * 
import animations

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Move/derecha.png')
        self.image = self.get_image(0, 0) #coordonées de début du get

        self.image.set_colorkey([0, 0, 0]) #on sup le noir
        self.rect = self.image.get_rect()
        self.pos = [x,y] #position du joueur
        self.speed = 4 #vitesse du joueur
        self.all_projectiles = pygame.sprite.Group()
        self.old_pos = self.pos.copy()
        #self.sprite = { }  dictionnaire des images
        self.HP = 200
        self.maxHP = 200
        self.stats = 10
        self.killcount = 0
        self.attack_delay =0.3
        self.old_attack = 0
      
    
    #def anim_epee(self) :
    #    for key in self.att_epee :
    #        self.epee = self.att_epee[key]
    #        self.epee.set_colorkey((0,0,0))

    def coup(self) :
        self.start_animation()

    def launch(self) : ## fait apparaitre le projectile 
        self.all_projectiles.add(Attack(self,self.pos[0], self.pos[1]))

    def go_left(self): self.pos[0] -= self.speed

    def go_right(self): self.pos[0] += self.speed

    def go_up(self): self.pos[1] -= self.speed

    def go_down(self): self.pos[1] += self.speed


    def update(self):#actualisation de la position
        self.rect.topleft = self.pos  #position


    def get_image(self, x, y):
        image = pygame.Surface([64, 64]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64)) #Origine du crop et coordonnées de fin du crop
        return image
        