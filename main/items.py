import pygame

def get_image(sprite,x, y):
    image = pygame.Surface([32, 32]) #surface occupée sur le jeu
    image.blit(sprite, (0, 0), (x, y, 32, 32)) #Origine du crop et coordonnées de fin du crop
    return image

class HPPOTION(): #Item Potion
    def __init__(self):
        super().__init__()
        self.description = "+50% HP"
        self.HEAL = 12 #Pourcentage de vie rendue
        self.sprite_sheet = pygame.image.load('Sprites/items/HPPOTION.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
    
    def useitem(self,cible): #redonne 50% de vie au joueur
        cible.player.HP += (cible.player.maxHP * 0.50)
        if cible.player.HP > cible.player.maxHP : cible.player.HP = cible.player.maxHP
        cible.player.ratio = cible.player.HP / cible.player.maxHP
        

class Shield(): #Item bouclier
    def __init__(self):
        super().__init__()
        self.description = "INVULNERABLE"
        self.sprite_sheet = pygame.image.load('Sprites/items/Shield.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
    
    def useitem(self,cible): #Active le bouclier du joueur
        cible.player.shield = True
    

class Philo(): #Item pierre philosophale 
    def __init__(self):
        super().__init__()
        self.description = "MAX HP "
        self.sprite_sheet = pygame.image.load('Sprites/items/PS.png')
        self.image = get_image(self.sprite_sheet,0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
    
    def useitem(self,cible): #redonne toute sa vie au joueur
        cible.player.HP = cible.player.maxHP
        cible.player.ratio = cible.player.HP / cible.player.maxHP