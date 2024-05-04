import pygame
from items import *
from random import choices

blessings = [HPPOTION(),Shield(),Philo()]
probas = [0.7,0.2,0.1]

def Blessing(): #Un item au hasard
        chosen_object = choices(blessings, weights=probas)[0]
        return chosen_object


class effect(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.used = False
        self.blessing = Blessing()
        self.image = pygame.transform.scale(self.blessing.image,(20,20))
        self.comment = self.blessing.description
        self.pos = [x,y]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos 

    def use(self,cible): 
        self.blessing.useitem(cible) #On applique son effet
