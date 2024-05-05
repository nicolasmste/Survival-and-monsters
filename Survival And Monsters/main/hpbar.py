import pygame
from math import ceil

class HPbar(pygame.sprite.Sprite):

    def __init__(self,x,y,hpratio,speed):
        super().__init__()
        self.ratio = hpratio
        self.pos = [x,y+37]
        self.sprite_HP = pygame.image.load('Sprites/Bars/hpBarGIF.png')
        self.HPIMAGES = [self.get_image(self.sprite_HP, 0+j*64 , 0 , 64, 64) for j in range (0,13)]
        self.image = self.HPIMAGES[0]
        self.rect = self.image.get_rect()

    def update(self):#actualisation de la vie
        if self.ratio != 0: self.image = self.HPIMAGES[13-ceil(self.ratio*13)]
        else: self.image = self.HPIMAGES[0]
        self.image.set_colorkey([0, 0, 0])

    def updatepos(self,x,y): #Update vitesse et position
        self.pos = [x,y+37]
        self.rect.topleft = self.pos

    def get_image(self, myimage, x, y, x1, y1):
        image = pygame.Surface([x1, y1]) #surface occupée sur le jeu
        image.blit(myimage, (0, 0), (x, y, x1, y1)) #Origine du crop et coordonnées de fin du crop
        return image