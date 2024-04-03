import pygame

class XP(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.xp_bar = pygame.image.load('/home/e20230001926/Bureau/PROJET/Survival-and-monsters-main/Survival And Monsters/Sprites/XP BAR/XP.png')
        self.image = self.get_image(0,416)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.pos = [x,y]

    

    def get_image(self, x, y):
        image = pygame.Surface([320, 320]) #surface occupée sur le jeu
        image.blit(self.xp_bar, (0, 0), (x, y, 320, 32)) #Origine du crop et coordonnées de fin du crop
        return image