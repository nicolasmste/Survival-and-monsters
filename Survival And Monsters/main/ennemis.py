from typing import Any
import pygame
from math import sqrt
from Attributes import *
from random import choices

types = [slime(),kingslime(),Orc(),Bat()]#différents ennemis
probas = [0.3,0.2,0.2,0.3]#proba de l'apparition des différents ennemis

def color(me): #On modifie la couleur
    for i in range(0,len(me)):
        me[i].set_colorkey([0, 0, 0])

def newtype():#fonction qui permet de choisit le type du nouvel ennemi
    chosen_object = choices(types, weights=probas)[0]
    return chosen_object

class ennemi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        
        self.type = newtype()#type de l'ennemi
        color(self.type.imageliste)
        self.image = self.type.image#image
        self.givenxp = self.type.xp #XP donnée

        #tous les parametres(points de vie, vitesse, dégats et image) dépend du tyoe de l'ennemi
        
        self.HP = self.type.HP
        self.maxHP = self.type.maxHP
        
        self.speed = self.type.speed
        self.normalSpeed = self.type.normalSpeed
        
        self.attack = self.type.attack
        self.normalAttack = self.type.normalAttack

        self.pos = [x,y]
        self.rect = self.image.get_rect()

    def move(self): #Change Sprite
        if self.type.delay == 0:
            if self.type.it == len(self.type.imageliste)-1:
                self.type.image = self.type.imageliste[0]
                self.type.it = 0
            else : 
                self.type.it += 1
                self.type.image = self.type.imageliste[self.type.it]
                self.image.set_colorkey([0, 0, 0])
            self.type.delay = 10
        else: self.type.delay -= 1

    def moveTo(self,Px,Py):#fonction qui déplace les ennemis vers le joueur
        
        if self.pos[0] == Px :#si les coordonnées en X sont égales, évite la division par 0
            coef = 0
        else :
            coef = (Py-self.pos[1])/(Px-self.pos[0])#coefficient directeur de la droite

        self.tan = sqrt((self.speed*self.speed)/(1+coef*coef))#distance a parcourir en abscisse pour que l'ennemis parcours une distance égale à la variable speed

        if Px != self.pos[0]:#Si le joueur et l'ennemi n'ont pas la même abscisse
      
            if self.pos[0] < Px:#Si l'ennemi est à gauche du joueur
                self.pos[1] += self.tan * coef
                self.pos[0] += self.tan
            else:#Si l'ennemi est à droite du joueur
                self.pos[1] -= self.tan * coef
                self.pos[0] -= self.tan
            
        
        else:#il faut juste déplacer en Y
            if self.pos[1]>Py:
                self.pos[1] -= self.tan
            else :
                self.pos[1] += self.tan

    def damage(self,Prect,PHP):#Si le joueur est touché
        
        if pygame.Rect.colliderect(self.rect,Prect):
            PHP -= self.attack
            
            return PHP,True
        return PHP,False

    def hit(self,Prect):#si un ennemis est touché
        if pygame.Rect.colliderect(self.rect,Prect):
            return True
        return False

    def update(self):
        self.move()
        self.image = self.type.image
        self.rect.topleft = self.pos 

    def get_image(self, x, y):
        image = pygame.Surface([32, 32]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
        return image

