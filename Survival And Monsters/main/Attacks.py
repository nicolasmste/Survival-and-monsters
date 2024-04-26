import pygame
from math import sqrt


class fireBall(pygame.sprite.Sprite):

    def __init__(self,x,y,cible):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Move/Fireball.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        self.speed = 10
        self.pos = [x,y]
        self.startPos = [x,y]
        self.degat = 10
        self.range = 250
        if cible[0] == self.pos[0] :#si les coordonnées en X sont égales, évite la division par 0
            self.coef = 0
        else :
            self.coef = (cible[1]-self.pos[1])/(cible[0]-self.pos[0])#division par 0 si cible[0] == self.pos[0]
        self.cible = [cible[0],cible[1]]

    def move(self):#probleme (peut etre) tire n'importe où des fois
        if self.cible[0] != self.pos[0]:
            self.pos[1] += self.speed * self.coef
            if self.pos[0]>self.cible[0]:
                self.pos[0] -= self.speed
            else :
                self.pos[0] += self.speed
        
        else:#il faut juste déplacer en Y
            if self.pos[1]>self.cible[1]:
                self.pos[1] -= self.speed
            else :
                self.pos[1] += self.speed

    def update(self):
        self.rect.topleft = self.pos

    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
        return image

#Boule de feu de zone, coup d'épée, whip, fleche