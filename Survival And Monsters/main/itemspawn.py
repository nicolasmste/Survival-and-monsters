import pygame
from items import *
from random import choices



blessings = [HPPOTION(),Shield(),Clover(),BlackClover(),Philo()]
probas = [0.7,0.15,0.05,0.05,0.05]

def Blessing():
        chosen_object = choices(blessings, weights=probas)[0]
        return chosen_object


class effect(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.used = False
        self.blessing = Blessing()
        self.image = pygame.transform.scale(self.blessing.image,(20,20))
        comment = self.blessing.descritpion
        self.used = False
        self.pos = [x,y]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos 
