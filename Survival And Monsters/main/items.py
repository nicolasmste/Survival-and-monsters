import pygame


class HPPOTION(pygame.sprite.Sprite):
    def __init__(self,x,y,cible):
        super().__init__()
        self.descritpion = "Une potion magique qui vous redonnera un peu de vie."
        self.HEAL = 1.2 #Pourcentage de vie rendue

class Shield(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.descritpion = "Behold, the SUPREME DEITY provides you a shield."
        self.shield = 1

class Clover(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.descritpion = "LAPLACE the MASTER OF MISCHIEF, challenge you ! Succeed and you you'll be rewarded"
        Boost = 2

class BlackClover(pygame.sprite.Sprite):  #QUI PORTE
    def __init__(self,x,y):
        super().__init__()
        self.descritpion = "Your gluttony disdained Laplace ! Be punished for your sin.  "
        Boost = 2

class BlackClover(pygame.sprite.Sprite):  #QUI PORTE
    def __init__(self,x,y):
        super().__init__()
        self.descritpion = "Your gluttony disdained Laplace ! Be punished for your sin.  "
        Boost = 2


class Graal(pygame.sprite.Sprite):
    def __init__(self,x,y,cible):
        super().__init__()
        self.descritpion = "..."

        
class Philo(pygame.sprite.Sprite):
    def __init__(self,x,y,cible):
        super().__init__()
        self.descritpion = "Philosopher's stone "

