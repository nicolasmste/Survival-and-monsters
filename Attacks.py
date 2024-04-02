import pygame
from game import *


class Attack(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 4
        self.image = pygame.image.load("Sprites/Move/FIREBALL.png")
        #self.fireball.set_colorkey([0, 0, 0])
        #self.image = self.get_fireball(0, 0)
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.x = player.rect.x + 250
        self.rect.y = player.rect.y + 100
        self.origin_image = self.image.copy()
        self.angle = 0

    def rotate(self) :
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)

    def remove(self) :
        self.player.all_projectiles.remove(self)

    def moove (self) :
        self.rect.x += self.velocity 
        self.rotate()

        if self.rect.x > 1250 :
            self.remove()
    
    #def get_fireball(self,x,y) :
    #    image = pygame.Surface([32, 32]) #surface occupée sur le jeu
    #    image.blit(self.fireball, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
    #    return image
        