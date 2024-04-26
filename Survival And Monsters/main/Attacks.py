import pygame
from math import sqrt,acos,degrees
from random import randint


class fireBall(pygame.sprite.Sprite):

    def __init__(self,x,y,ePos):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Move/Fireball.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        
        self.speed = 4
        self.pos = [x,y]
        self.startPos = [x,y]
        self.degat = 5
        #self.portee = 250
        self.precision = 4#plus elle est basse plus il est précis, plus l'écart es faible
        #self.cible = ePos
        self.cible = [randint(int(ePos[0]-self.precision),int(ePos[0]+self.precision)),randint(int(ePos[1]-self.precision),int(ePos[1]+self.precision))]
        
        if self.startPos[0] == self.cible[0] :#si les coordonnées en X sont égales, évite la division par 0
            self.coef = 0
        else :
            self.coef = (self.cible[1]-self.pos[1])/(self.cible[0]-self.pos[0])#coefficient directeur de la droite
        
        self.tan = sqrt((self.speed*self.speed)/(1+self.coef*self.coef))#variable qui permet d'avoir toujour la bonne vitesse de déplacement en fonction de self.speed peut importe le coef


    def direction(self):
        #mieux d'utiliser le cos
        adj = self.cible[0] - self.startPos[0]
        opp = self.cible[1] - self.startPos[1]
        hypo = sqrt(adj*adj + opp*opp)
        
        if(hypo == 0):#evite la division par 0
            angle = 0
        else:
            angle = degrees(acos(adj/hypo))
        
        if opp > 0:
            angle = -angle
        self.image = pygame.transform.rotate(self.image,angle)


    def move(self):#tire à l'opposé qund l'ennemis est en bas à droite et en haut à gauche
        
        if self.cible[0] != self.pos[0]:
            #self.pos[1] += self.speed * self.coef
            if self.startPos[0] < self.cible[0]:
                self.pos[1] += self.tan * self.coef
            else:
                self.pos[1] -= self.tan * self.coef
            
            if self.startPos[0]>self.cible[0]:
                self.pos[0] -= self.tan
            else :
                self.pos[0] += self.tan
        
        else:#il faut juste déplacer en Y
            if self.startPos[1]>self.cible[1]:
                self.pos[1] -= self.tan
            else :
                self.pos[1] += self.tan

    def update(self):
        self.rect.topleft = self.pos

    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
        return image
    
    
        