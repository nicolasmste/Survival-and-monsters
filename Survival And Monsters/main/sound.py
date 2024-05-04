import pygame 

class sound :

    def __init__(self):

        self.nbBoucles = 6#nb de boucles de musique
        self.explosionSound = pygame.mixer.Sound("music/SFX/Explosion.wav")#bruitage de l'explosion
        self.fireBallSound = pygame.mixer.Sound("music/SFX/FireBall.wav")#bruitage du tire de boule de feu
        self.epeeSound = pygame.mixer.Sound("music/SFX/degatEpee.wav")#bruitage du coup d'épé
        
        self.nbDegat = 4#nb de différents bruitage lorsque le héro prend des dégats
        self.listDegatSound = []#liste des bruitages des cris de douleur du personnage principal

        self.musicMenu = "music/Boucle/boucleMenu.wav"#musique du menu principal
        self.listMus = []
        for i in range(self.nbBoucles):# remplissage de la liste avec les noms des des musiques
            name = "music/Boucle/boucle"+str(i)+".wav"
            self.listMus.append(name)    
        
        for j in range(self.nbDegat):
            name = "music/SFX/degat"+str(j)+".wav"
            self.listDegatSound.append(pygame.mixer.Sound(name))
    
    def playMus(self,mus):#fonction pour jouer les musiques
        self.music = pygame.mixer_music.load(mus)
        self.playM = pygame.mixer.music.play(loops = -1)#-1 permet de jouer en boucle