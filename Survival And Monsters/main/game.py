import pygame
from sys import exit
import pytmx
import pyscroll
from player import *


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
        bord = []
        for obj in tmx_data.objects :
            if obj.name == "collision":
                self.bord.append(pygame.Rect(obj.x,obj.y,obj.width,obj.heigh))
        


        #générer le joueur
        playerpos = tmx_data.get_object_by_name("player")
        self.player = Player(playerpos.x,playerpos.y)

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

    def run(self):
        clock = pygame.time.Clock() #Objet de type horloge
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        while running:
            
            self.keybordinput()
            self.group.update() #update position du joueur
            self.group.center(self.player.rect)
            pygame.display.update()
            self.group.draw(self.screen)
            clock.tick(30) #limiter les FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            #evenement du jeu:
            