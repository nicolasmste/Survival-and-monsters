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
from hpbar import HPbar
from menu import *
from Xpbar import XPbar



class Play:

    def __init__(self): #fenêtre du jeu
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((1280, 768))
        self.newcursor = pygame.image.load("Sprites/Cursor/Cursor.png")
    
        self.menu = Menu(self.screen)
        
        pygame.display.set_caption("Ninja","Sprites/Cursor/Cursor.png") 
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps/Levels/devmap.tmx')

        map_data = pyscroll.data.TiledMapData(tmx_data) 
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
    
    def game_init(self):
        
        #générer le joueur
        self.player = Player(0,0)
        self.hpbar = HPbar(self.player.pos[0],self.player.pos[1],self.player.ratio,self.player.speed)
        self.xpbar = XPbar(self.player.xpratio)
        self.listEnnemis = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1
        self.nVague = 0 #numéro de la vague
        self.listFireball = []
        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au CAC
        self.sfx = Sound()
        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)
        self.group.add(self.hpbar)
        self.group.add(self.xpbar)


    def distance(self,a,b):
        x = abs(a[0] - b[0])
        y = abs(a[1] - b[1])
        d = sqrt(x*x + y*y)
        return d

    def keybordinput(self) :
            touche = pygame.key.get_pressed() #Clavier
            if touche[pygame.K_UP]:
                self.player.go_up()
                self.hpbar.go_up()
            if touche[pygame.K_LEFT]:
                self.player.go_left()
                self.hpbar.go_left()
            if touche[pygame.K_RIGHT]:
                self.player.go_right()
                self.hpbar.go_right()
            if touche[pygame.K_DOWN]:
                self.player.go_down()
                self.hpbar.go_down()

    
    def Startmenu(self):
        self.screen.blit(self.menu.pressplay, (0, 0))
        self.screen.blit(self.menu.playbutton,self.menu.press)
        self.screen.blit(self.menu.settingsimage,self.menu.setrect)
        self.game_init()

    def Gameovermenu(self):
        self.screen.blit(self.menu.gameoverscreen,self.menu.gorect) 
        self.listEnnemis = []
        for i in self.group:
            if i != self.player: self.group.remove(i)

    def Pausemenu(self):
            self.screen.blit(self.menu.pausemenu,(0,0))
            self.screen.blit(self.menu.resumebutton,self.menu.resumerect)
            self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
            self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)
    
    def Settingsmenu(self):
        self.screen.blit(self.menu.pausemenu,(0,0))
        self.screen.blit(self.menu.quit,self.menu.quitbutton)
        self.screen.blit(self.menu.quit,self.menu.resumerect)
        self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
        self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)

        
                
      


    def run(self):
        clock = pygame.time.Clock() #Objet de type horloge
        running = True     #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre
        

        while running:
            
            
            if self.menu.PLAY and not self.menu.PAUSE:# 
                
                
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
                        self.sfx.explosion.play()  #bruit des explosion 
                        self.group.add(self.listFireball[-1])



                    if self.listFireball != []:
                        for fir in self.listFireball:
                            if en.dead(fir.pos) or (en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay):#si l'enemis est mort tué par une firaball ou que le joueur peut l'attaquer au CAC
                                self.oldAt = time.time()
                                self.player.killcount += 1
                                self.listEnnemis.remove(en)#on supprime l'objet de l'ennemis mort
                                self.group.remove(en)#et on ne l'affiche plus
                                
                                self.player.XP += en.givenxp
                                self.player.XPmanage()
                                print(f"XP : {self.player.XP}")
                                print(f"niv:{self.player.LVL}")
                                self.listFireball.remove(fir)#pareil pour la boule de feu qui à touché l'ennemis
                                self.group.remove(fir)
                                break
                    else: 
                        if en.dead(self.player.pos) and time.time()-self.oldAt >= self.player.attackDelay:
                            self.oldAt = time.time()
                            self.player.killcount += 1
                            self.player.XP += en.givenxp
                            self.listEnnemis.remove(en)
                            self.group.remove(en)
                            self.player.XPmanage()
                            print(f"XP : {self.player.XP}")
                            print(f"niv:{self.player.LVL}")



                for fir in self.listFireball:
                    fir.move()
                    if self.distance(fir.startPos,fir.pos) >= fir.range:
                        self.listFireball.remove(fir)
                        self.group.remove(fir)
                
                self.keybordinput()
                self.group.update()
                self.hpbar.ratio = self.player.XPratio #update position du joueur
                
                self.group.center(self.player.rect)
                pygame.display.update()
                
                self.group.draw(self.screen)
                self.screen.blit(self.menu.pausebutton,self.menu.pauserect)
                if self.player.end():
                    self.menu.gameover = True
                    self.menu.PLAY = False     
            if self.menu.PAUSE : 
                self.Pausemenu()
            
            if not self.menu.PLAY and not self.menu.gameover:
                self.Startmenu()
                print(f"Level : {self.player.XP}")   
            elif self.menu.gameover:
                self.Gameovermenu()  #Si le joueur 
            
            if self.menu.SETTINGS :
                self.Settingsmenu()
                               #On verifie si le joueur à toujour des p
                
            #################################################################################################""""
            
            if not self.menu.PAUSE : 
                mousepos = pygame.mouse.get_pos()
                self.screen.blit(self.newcursor,mousepos)
            pygame.display.update()
            clock.tick(30) #limiter les FPS
  
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.press.collidepoint(event.pos) and not self.menu.PLAY and not self.menu.SETTINGS and not self.menu.gameover:
                    self.menu.PLAY = True #SI ON APPUIE SUR PLAY LE JEU SE LANCE   
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.pauserect.collidepoint(event.pos) and self.menu.PLAY and not self.menu.gameover :
                    pygame.mouse.set_visible(True)
                    self.menu.PAUSE = True #SI ON APPUIE SUR PAUSE LE JEU SE LANCE
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.resumerect.collidepoint(event.pos) and self.menu.PAUSE:
                    self.menu.PAUSE = False#tu clique trop vite il te faut juste un menue 
                    pygame.mouse.set_visible(False)
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.gorect.collidepoint(event.pos) and self.menu.gameover:
                    self.menu.gameover = False 
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.setrect.collidepoint(event.pos) and not self.menu.PLAY and not self.menu.SETTINGS:
                    self.menu.SETTINGS = True
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.quitbutton.collidepoint(event.pos) and self.menu.SETTINGS:
                    self.menu.SETTINGS = False
                #if event.type == pygame.MOUSEBUTTONDOWN and self.menu.minusbutton.collidepoint(event.pos) and (self.menu.SETTINGS or self.menu.PAUSE):
                    #pygame.mix ... IL FAUT BAISSER LE SON
                #if event.type == pygame.MOUSEBUTTONDOWN and self.menu.plusbutton.collidepoint(event.pos) and (self.menu.SETTINGS or self.menu.PAUSE):
                    #pygame.mix ... IL FAUT AUGMENTER LE ON


                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            #evenement du jeu:
            