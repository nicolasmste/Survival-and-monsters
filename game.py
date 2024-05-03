import pygame
from sys import exit
import pytmx
import pyscroll
from player import *
from XP import *
from ennemis import *
from random import randint


class Play:

    def __init__(self): #fenêtre du jeu
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Ninja") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps\Levels\devmap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2  

         #bordure des maps
        self.bord = []
        for obj in tmx_data.objects :
           if obj.name == "collision":
               self.bord.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        


        #générer le joueur
        #playerpos = tmx_data.get_object_by_name("player")
        #self.player = Player(playerpos.x,playerpos.y)
        
        self.player = Player(50,50)

        self.listEnnemis = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)


        self.xpbar = XP()

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
    

    def keybordinput(self) :
            touche = pygame.key.get_pressed() #Clavier
            if touche[pygame.K_UP]:
                self.player.go_up()
            elif touche[pygame.K_LEFT]:
                self.player.go_left()
            elif touche[pygame.K_RIGHT]:
                self.player.go_right()
            elif touche[pygame.K_DOWN]:
                self.player.go_down()

    def update(self):#vérifie s'il le rectangle du joueur touche le bord de la maps
        self.group.update()
        for element in self.group.sprites():
            if element.feet.collidelist(self.bord) > -1 : 
                element.rollback()

    def run(self):
        clock = pygame.time.Clock() #Objet de type horloge
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        while running:
            print(clock)
            if self.listEnnemis ==[]:
                for i in range(0,self.tailleVague*self.coefVague):#fait apparaitre un vague d'ennemis
                    self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                    self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi
                self.coefVague = randint(1,3)
            
            for en in self.listEnnemis :
                en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                self.player.HP = en.damage(self.player.pos,self.player.HP)#gestion des dégats
            #print("HP = ", self.player.HP)
            
            self.player.saveloc() #ancienne position sauvegardée
            self.keybordinput()
            self.update()#update position du joueur
            self.group.center(self.player.rect)
            pygame.display.update()
            
            self.group.draw(self.screen)
            self.xpbar.afficher(self.screen)
            clock.tick(30) #limiter les FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            #evenement du jeu:
            