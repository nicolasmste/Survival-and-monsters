import pygame 

#pygame.mixer.init()

class sound :

    def __init__(self):

        self.nbBoucles = 6
        self.explosionSound = pygame.mixer.Sound("music/SFX/Explosion.wav")
        self.fireBallSound = pygame.mixer.Sound("music/SFX/FireBall.wav")
        self.epeeSound = pygame.mixer.Sound("music/SFX/degatEpee.wav")
        
        self.nbDegat = 4
        self.listDegatSound = []

        self.musicMenu = "music/Boucle/boucleMenu.wav"
        self.listMus = []
        for i in range(self.nbBoucles):# remplissage de la liste avec les noms des des musiques
            name = "music/Boucle/boucle"+str(i)+".wav"
            self.listMus.append(name)    
        
        for j in range(self.nbDegat):
            name = "music/SFX/degat"+str(j)+".wav"
            self.listDegatSound.append(pygame.mixer.Sound(name))
    
    def playMus(self,mus):
        self.music = pygame.mixer_music.load(mus)
        self.playM = pygame.mixer.music.play(loops = -1)#-1 permet de jouer en boucle