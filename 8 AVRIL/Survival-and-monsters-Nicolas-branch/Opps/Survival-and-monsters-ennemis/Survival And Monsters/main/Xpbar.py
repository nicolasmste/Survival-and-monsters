import pygame
from math import ceil,floor

class XPbar():

    def __init__(self,x,y,xpratio):
        super().__init__()
        self.ratio = xpratio
        self.pos = [x-35,y-50]
        self.sprite_HP = pygame.image.load('Sprites/Bars/XP.png')
        self.XPIMAGES = [self.get_image(self.sprite_HP, 8320-j*320 , 0 , 320, 32) for j in range (0,26)]
        self.image = self.XPIMAGES[0]
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


    
    def update(self):#actualisation de la position
        print(f"AAAAAARATIO AA{self.ratio}")
    
        self.image = self.XPIMAGES[floor(self.ratio*26)]
        self.image.set_colorkey([0, 0, 0])
        


    def get_image(self, myimage, x, y, x1, y1):
        image = pygame.Surface([x1, y1]) #surface occupée sur le jeu
        image.blit(myimage, (0, 0), (x, y, x1, y1)) #Origine du crop et coordonnées de fin du crop
        return image
        