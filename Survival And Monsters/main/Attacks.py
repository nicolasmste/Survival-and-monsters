import pygame
from math import sqrt,tan,degrees
from random import randint


class fireBall(pygame.sprite.Sprite):

    def __init__(self,x,y,ePos):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Sprites/Move/Fireball.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        self.speed = 10
        self.pos = [x,y]
        self.startPos = [x,y]
        self.degat = 10
        #self.portee = 250
        self.precision = 0#plus elle est basse plus il est précis, plus l'écart es faible
        #self.cible = ePos
        self.cible = [randint(ePos[0]-self.precision,ePos[0]+self.precision),randint(ePos[1]-self.precision,ePos[1]+self.precision)]
        
        if self.startPos[0] == self.cible[0] :#si les coordonnées en X sont égales, évite la division par 0
            self.coef = 0
        else :
            self.coef = (self.cible[1]-self.pos[1])/(self.cible[0]-self.pos[0])#coefficient directeur de la droite
        
        self.tan = sqrt((self.speed*self.speed)/(1+self.coef*self.coef))#variable qui permet d'avoir toujour la bonne vitesse de déplacement en fonction de self.speed peut importe le coef


    def direction(self):
        if self.startPos[1] == self.cible[1]:
            if self.startPos[0] > self.cible[0]:
                self.image = pygame.transform.rotate(self.image,180)
        
        elif self.startPos[0] == self.cible[0]:
            if self.startPos[1] > self.cible[1]:
                self.image = pygame.transform.rotate(self.image,-90)
            else :
                self.image = pygame.transform.rotate(self.image,90)
        else :
            adj = abs(self.startPos[0] - self.cible[0])#longueur de l'angle adjacent
            opp = abs(self.startPos[1] - self.cible[1])#longueur de l'angle opposé
            angle = degrees(tan(opp/adj))
            self.image = pygame.transform.rotate(self.image,-angle)

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