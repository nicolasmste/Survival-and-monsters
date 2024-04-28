import pygame 

#pygame.mixer.init()

class sound :

    def __init__(self):
        self.explosion = pygame.mixer.Sound("SFX/EXPLOSION.wav")
        self.listMus = ["music/ZOO.mp3","music/DLD.mp3"]
        

    def play(self,mus):
        self.music = pygame.mixer_music.load(mus)
        self.playM = pygame.mixer.music.play(loops = -1)#-1 permet de jouer en boucle