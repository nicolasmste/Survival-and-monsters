import pygame 
import time
from sys import exit
import pytmx
import pyscroll
from player import *
from Attacks import * 
from sound import sound
from ennemis import ennemi
from random import randint



class Play:

    def __init__(self): #fenêtre du jeu
        tailleMap = [925,605]
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Ninja") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps/Levels/devmap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #générer le joueur
        self.player = Player(0,0)
        self.music = sound()

        self.listEnnemis = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1
        self.nVague = 0#numéro de la vague

        self.listEtape = [1,3]#liste des vagues où la musique évolue
        #faire qqchose quand onn arrive à la fin de la liste pour éviter index out of range
        self.nbMus = len(self.listEtape)
        self.etape = 0

        self.listFireball = []

        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au CAC
        self.hitTime = 0#moment du dernier coup recu

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)

    def distance(self,a,b):
        x = a[0] - b[0]
        y = a[1] - b[1]
        d = sqrt(x*x + y*y)
        return d

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
            #print(self.player.pos)
            
            if self.listEnnemis == []:#4eme vague avec 180 elements = pas un peu beaucoup
                aRemplir = True
                self.nVague += 1

                if self.etape < self.nbMus and self.nVague >=self.listEtape[self.etape]:
                    self.music.play(self.music.listMus[self.etape])
                    self.etape += 1

                self.tailleVague = self.tailleVague*self.coefVague
                print("vague n°", self.nVague)
                print("ennemis = ",self.tailleVague)
                #faire apparaitre les ennemis hors de la map

            if aRemplir == True:   
                self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi

            if len(self.listEnnemis) == self.tailleVague:
                aRemplir = False
                self.coefVague = randint(self.nVague,2*self.nVague)#plus on avance plus le coef de multiplication des vagues augmente
                #faire en soret que ya des nombres à virgule
            
            for en in self.listEnnemis :
                en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                if time.time()-self.hitTime >= self.player.invincibl:#temps d'invincibilité
                    dam = en.damage(self.player.pos,self.player.HP)#gestion des dégats au joueur
                    if(dam[1] == True):
                        self.player.HP = dam[0]
                        #print("HP = ", self.player.HP)
                        self.hitTime = time.time()
                        #print("hit")
                
                if self.distance(self.player.pos , en.pos) <= self.player.range and time.time()-self.oldFire >= self.player.fireDelay and self.player.pos != en.pos:#si un ennemis est dans la range on tire si l'attaque est rechargé et si on le joueur et l'ennemis ne sont pas a la meme position
                    self.oldFire = time.time()#actualisation de la derniere fois que l'on à tir
                    self.listFireball.append(fireBall(self.player.pos[0],self.player.pos[1],en.pos))
                    self.listFireball[-1].direction()
                    self.group.add(self.listFireball[-1])
                
                if self.listFireball != []:
                    #print(self.listFireball)
                    for fir in self.listFireball:
                        if en.dead(fir.pos) or (en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay):#si l'enemis est mort tué par une firaball ou que le joueur peut l'attaquer au CAC
                            self.oldAt = time.time()
                            en.HP -= fir.degat
                            
                            if en.HP<=0:#si l'ennemis n'a plus de pv
                                self.player.killcount += 1
                                self.listEnnemis.remove(en)#on supprime l'objet de l'ennemis mort
                                self.group.remove(en)#et on ne l'affiche plus
                            
                            self.listFireball.remove(fir)#pareil pour la boule de feu qui à touché l'ennemis
                            self.group.remove(fir)
                            break#pour ne pas retirer 2 fois un ennemis de la liste
                else: 
                    if en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay:
                        self.oldAt = time.time()
                        self.player.killcount += 1
                        self.listEnnemis.remove(en)
                        self.group.remove(en)
                    
                
            
            for fir in self.listFireball:
                fir.move()
                if self.distance(fir.startPos,fir.pos) > self.player.range:
                    self.listFireball.remove(fir)
                    self.group.remove(fir)

        
                    
            #print("HP = ", self.player.HP)

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
            