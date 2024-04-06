import pygame 
import time
from sys import exit
import pytmx
import pyscroll
from player import *
from Attacks import * 
from ennemis import ennemi
from random import randint
from SFX import Sound


class Play:

    def __init__(self): #fenêtre du jeu
        self.screen = pygame.display.set_mode((1280, 768))
        self.PLAY = False
        self.pressplay = pygame.image.load('Menus/FOND.png')
        self.newcursor = pygame.image.load("Sprites\Cursor\Cursor.png")
        pygame.mouse.set_visible(False)
        
        self.playbutton = pygame.image.load('Menus\PRESSPLAY.png')
        self.press = self.playbutton.get_rect()
        self.press.x = self.screen.get_width()/3
        self.press.y = self.screen.get_height()/3
        
        pygame.display.set_caption("Ninja","Sprites/Cursor/Cursor.png") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps/Levels/devmap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        
        


        #générer le joueur
        self.player = Player(0,0)

        self.listEnnemis = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1
        self.nVague = 0#numéro de la vague

        self.listFireball = []
        self.sfx = Sound()


        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au CAC

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)

    def distance(self,a,b):
        x = abs(a[0] - b[0])
        y = abs(a[1] - b[1])
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
            
            if not self.PLAY:
                self.screen.blit(self.pressplay, (0, 0))
             
                self.screen.blit(self.playbutton,self.press) 
            ####################################################################"
            if self.PLAY :

                if self.listEnnemis == []:
                    self.nVague += 1
                    for i in range(0,self.tailleVague*self.coefVague):#fait apparaitre un vague d'ennemis
                        self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                        self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi
                    self.coefVague = randint(self.nVague,3*self.nVague)#plus on avance plus le coef de multiplication des vagues augmente


                for en in self.listEnnemis :
                    en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                    self.player.HP = en.damage(self.player.pos,self.player.HP)#gestion des dégats au joueur

                    if self.distance(self.player.pos , en.pos) <= self.player.range and time.time()-self.oldFire >= self.player.fireDelay:#si un ennemis est dans la range on tire si l'attaque est rechargé
                        self.oldFire = time.time()#actualisation de la derniere fois que l'on à tir
                        self.listFireball.append(fireBall(self.player.pos[0],self.player.pos[1],en.pos))
                        self.sfx.explosion.play()
                        self.group.add(self.listFireball[-1])



                    if self.listFireball != []:
                        for fir in self.listFireball:
                            if en.dead(fir.pos) or (en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay):#si l'enemis est mort tué par une firaball ou que le joueur peut l'attaquer au CAC
                                self.oldAt = time.time()
                                self.player.killcount += 1
                                self.listEnnemis.remove(en)#on supprime l'objet de l'ennemis mort
                                self.group.remove(en)#et on ne l'affiche plus

                                self.listFireball.remove(fir)#pareil pour la boule de feu qui à touché l'ennemis
                                self.group.remove(fir)
                                break
                    else: 
                        if en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay:
                            self.oldAt = time.time()
                            self.player.killcount += 1
                            self.listEnnemis.remove(en)
                            self.group.remove(en)



                for fir in self.listFireball:
                    fir.move()
                    if self.distance(fir.startPos,fir.pos) >= fir.range:
                        self.listFireball.remove(fir)
                        self.group.remove(fir)



                #print("HP = ", self.player.HP)

                self.player.update_HP_bar()

                print(f"{self.player.HPIMAGE}")
                self.keybordinput()
                self.group.update() #update position du joueur
                self.group.center(self.player.rect)
                pygame.display.update()
                self.group.draw(self.screen)
                self.screen.blit(self.player.HPIMAGE,(self.player.pos[0],self.player.pos[1]))
                self.player.end()#On verifie si le joueur à toujour des pv
            #################################################################################################""""
            mousepos = pygame.mouse.get_pos()
            self.screen.blit(self.newcursor,mousepos)
            pygame.display.update()
            clock.tick(30) #limiter les FPS
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.press.collidepoint(event.pos) :
                    self.PLAY = True
                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            #evenement du jeu:
            