import pygame
from math import floor

class XPbar():

    def __init__(self,x,y,xpratio):
        super().__init__()
        self.ratio = xpratio #initalise l'xp en fontion du ratio
        self.sprite_HP = pygame.image.load('Sprites/Bars/XP.png') #image de plusieurs 
        self.XPIMAGES = [self.get_image(self.sprite_HP, 8320-j*320 , 0 , 320, 32) for j in range (0,26)] 
        self.sprite_LVLup = pygame.image.load('Sprites/Bars/l0_Level6.png')
        self.LVLimage = self.get_image(self.sprite_LVLup,0 , 0 , 132, 132)
        self.it = 0 #Afficher LVLUP
        self.LVLimage.set_colorkey([0, 0, 0])
        self.image = self.XPIMAGES[0] #initalisation à la 1ère image
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect() #placer l'xp en haut
        self.rect.x = 0
        self.rect.y = 0
    
    def update(self):#actualisation de la position et la barre en fontion du ratio    
        self.image = self.XPIMAGES[floor(self.ratio*26)]
        self.image.set_colorkey([0, 0, 0]) #retirer le fond

    def get_image(self, myimage, x, y, x1, y1):
        image = pygame.Surface([x1, y1]) #surface occupée sur le jeu
        image.blit(myimage, (0, 0), (x, y, x1, y1)) #Origine du crop et coordonnées de fin du crop
        return image