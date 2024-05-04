import pygame

class Animations_sprites(pygame.sprite.Sprite) :#objet qui représente l'annimation de l'épée

    def __init__(self, sprite_name,x,y) :
        super().__init__()
        self.current_image = 0
        self.image = pygame.image.load(f"Sprites/Move/anim_epee/anim_epee0.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.animation= False
        self.taille_anim = 13#nombre d'images de l'anniimation
        self.pos = [x,y]
