import pygame
from sys import exit
import pytmx
import pyscroll
from player import *
from ennemis import ennemi
from random import randint


class Play:

    def __init__(self): #fenêtre du jeu
        
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Ninja") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps/Levels/devmap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        #print(tmx_data.get_object_by_name("image"))
        #bordure des maps
        # bord = []
        # for obj in tmx_data.objects :
        #     if obj.name == "collision":
        #         self.bord.append(pygame.Rect(obj.x,obj.y,obj.width,obj.heigh))
        


        #générer le joueur
        #playerpos = tmx_data.get_object_by_name("player")
        #self.player = Player(playerpos.x,playerpos.y)
        self.player = Player(0,0)

        self.listEnnemis = []

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)

    def keybordinput(self) :
            touche = pygame.key.get_pressed() #Clavier
            if touche[pygame.K_UP]:
                self.player.go_up()
            if touche[pygame.K_LEFT]:
                self.player.go_left()
            if touche[pygame.K_RIGHT]:
                self.player.go_right()
            if touche[pygame.K_DOWN]:
                self.player.go_down()

    def run(self):
        clock = pygame.time.Clock() #Objet de type horloge
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        while running:
            
            if (pygame.time.get_ticks()) > 500 and (pygame.time.get_ticks()) < 550:#trouver un meilleur moyen de faire apparaitre les ennemis
                print("new ennemi")
                self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi
            
            for en in self.listEnnemis :
                en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                self.player.HP = en.damage(self.player.pos,self.player.HP)#gestion des dégats
            print("HP = ", self.player.HP)

            self.keybordinput()
            self.group.update() #update position du joueur
            self.group.center(self.player.rect)
            pygame.display.update()
            self.group.draw(self.screen)
            clock.tick(30) #limiter les FPS
            self.player.end()#On verifie si le joueur à toujour des pv
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            #evenement du jeu:
            