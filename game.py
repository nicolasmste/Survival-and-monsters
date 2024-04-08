import pygame
from sys import exit
import pytmx
import pyscroll
from player import *
from ennemis import ennemi
from random import randint
import time
import Attacks



class Play:

    def __init__(self): #fenêtre du jeu
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Ninja") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('/home/e20230005608/Bureau/projet/Survival-and-monsters-main/Survival-And-Monsters/Maps/Levels/devmap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #bordure des mapsself.player
        #bord = []
        #for obj in tmx_data.objects :
        #    if obj.name == "collision":
        #        self.bord.append(pygame.Rect(obj.x,obj.y,obj.width,obj.heigh))
        
        #générer le joueur
        playerpos_x = 460
        playerpos_y = 300
        self.player = Player(playerpos_x,playerpos_y)
        self.attaq = Attack(self,playerpos_x,playerpos_y)

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
    
        self.listEnnemis = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis    
        self.coefVague = 1
        
    def keybordinput(self) :
            touche = pygame.key.get_pressed() #Clavier
            if touche[pygame.K_SPACE] :
                self.attaq.image()
                self.attaq.update_animation()
                
            if touche[pygame.K_z]:
                self.player.go_up()
            if touche[pygame.K_q]:
                self.player.go_left()
            if touche[pygame.K_d]:
                self.player.go_right()
            if touche[pygame.K_s]:
                self.player.go_down()
            
    
    def run(self):
        clock = pygame.time.Clock() #Objet de type horloge
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        while running:
            
           # print(clock)
            print(self.player.HP)
            if self.listEnnemis ==[]:
                for i in range(0,self.tailleVague*self.coefVague):#fait apparaitre un vague d'ennemis
                    self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                    self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi
                self.coefVague = randint(1,3)
            
            for en in self.listEnnemis :
                en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                self.player.HP = en.damage(self.player.pos,self.player.HP)#gestion des dégats
                if time.time() - self.player.old_attack > self.player.attack_delay :   
                    if en.dead(self.player.pos) == True : #or en.deadF(self.player.pos) == True :
                        self.att_epee()
                        self.player.killcount +=1
                        self.listEnnemis.remove(en)
                        self.group.remove(en)
                        self.player.old_attack = time.time()
            #print("HP = ", self.player.HP)

            self.keybordinput()
            self.group.update() #update position du joueur
            self.group.center(self.player.rect)
            pygame.display.update()
            self.group.draw(self.screen)
            self.player.all_projectiles.draw(self.screen)
            clock.tick(30) #limiter les FPS

            for Attacks in self.player.all_projectiles :
                Attacks.moove()
    
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            