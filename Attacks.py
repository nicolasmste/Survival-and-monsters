import pygame
from game import *
import animations

class Attack(animations.Animations_sprites):

    def __init__(self, player,x,y):
        super().__init__("anim_épée0")
        self.velocity = 4
        #self.image = pygame.image.load("Sprites/Move/FIREBALL.png")
        self.rect = self.image.get_rect()
        self.player = player
        self.pos =[x,y]
        self.origin_image = self.image.copy()
        self.angle = 0

    #def rotate(self) :  ## permet de faire touner le projectile sur lui-meme 
    #    self.angle += 15
    #    self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
#
    #def remove(self) : # supprime le projectile
    #    self.player.all_projectiles.remove(self)
#
    #def moove (self) : ## fait avancer le projectile et le supprime s'il dépasse les 1250 pixels
    #    self.rect.x += self.velocity 
    #    self.rotate()
#
    #    if self.rect.x > 1250 :
    #        self.remove()
    
    def update_animation(self) :
        self.animate()

    
    def update(self):#actualisation de la position
        self.rect.topleft = self.pos  #position


    def get_image(self, x, y):
        image = pygame.Surface([64, 64]) #surface occupée sur le jeu
        image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64)) #Origine du crop et coordonnées de fin du crop
        return image
        
    
    