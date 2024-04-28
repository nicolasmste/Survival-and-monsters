import pygame



def get_image(sprite,x, y):
    image = pygame.Surface([32, 32]) #surface occupée sur le jeu
    image.blit(sprite, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
    return image

class HPPOTION():
    def __init__(self):
        super().__init__()
        self.descritpion = "Une potion magique qui vous redonnera un peu de vie."
        self.HEAL = 12 #Pourcentage de vie rendue
        self.sprite_sheet = pygame.image.load('Sprites/items/HPPOTION.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()


class Shield():
    def __init__(self):
        super().__init__()
        self.descritpion = "Behold, the SUPREME DEITY provides you a shield."
        self.shield = 1
        self.sprite_sheet = pygame.image.load('Sprites/items/Shield.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
      
class Clover():
    def __init__(self):
        super().__init__()
        self.descritpion = "LAPLACE the MASTER OF MISCHIEF, challenge you ! Succeed and you you'll be rewarded"
        Boost = 2
        self.sprite_sheet = pygame.image.load('Sprites/items/HPPOTION.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
       


class BlackClover():  #QUI PORTE
    def __init__(self):
        super().__init__()
        self.descritpion = "Your gluttony disdained Laplace ! Be punished for your sin.  "
        Boost = 2
        self.sprite_sheet = pygame.image.load('Sprites/items/HPPOTION.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
  


        
class Philo():
    def __init__(self):
        super().__init__()
        self.descritpion = "Philosopher's stone "
        self.sprite_sheet = pygame.image.load('Sprites/items/PS.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

