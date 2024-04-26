import pygame
from itemps import *

blessings = [HPPOTION(),Shield(),Clover(),BlackClover(),Philo()]
probas = [0.7,0.15,0.05,0.05,0.05]

def Blessing(self):
        chosen_object = random.choices(blessings, weights=probas)[0]


class ennemi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.blessing = chosen_object
        self.sprite_sheet = pygame.image.load('Sprites/Tengu/Tengu.png')
        self.image = self.type.image
        self.used = False


        self.pos = [x,y]
        self.rect = self.image.get_rect()




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