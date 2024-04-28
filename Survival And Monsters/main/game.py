import pygame 
from time import time
from sys import exit
import pytmx
import pyscroll
from player import *
from Attacks import *
from animations import *
from sound import sound
from ennemis import ennemi
from itemspawn import effect
from random import randint,choices
from hpbar import HPbar
from menu import *
from Xpbar import XPbar

#a faire :
#   les items
#   régler le problème de la souris (si je trouve où c'est)
#

class Play:

    def __init__(self): #fenêtre du jeu
        
        self.screen = pygame.display.set_mode((1280, 768))

        pygame.mouse.set_visible(False)
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
        
        self.zoneS = zoneAf()

        self.hpbar = HPbar(self.player.pos[0],self.player.pos[1],self.player.ratio,self.player.speed)
        self.xpbar = XPbar(self.player.pos[0],self.player.pos[1],self.player.xpratio)

        self.listEnnemis = []
        self.listitems = []
        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1
        self.nVague = 0#numéro de la vague

        self.animation = False
        self.num_anim = 0
        self.épée = Animations_sprites('anim_épée',self.player.pos[0],self.player.pos[1])

        self.music = sound()
        self.listEtape = [1,3]#liste des vagues où la musique évolue
        #faire qqchose quand onn arrive à la fin de la liste pour éviter index out of range
        self.nbMus = len(self.listEtape)
        self.etape = 0

        self.listFireball = []

        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au CAC
        self.hitTime = 0#moment du dernier coup recu
        self.oldZone = 0#moment de la derniere attacke de zone

        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)
        self.group.add(self.listitems)
        self.group.add(self.hpbar)

    def distance(self,a,b):
        x = a[0] - b[0]
        y = a[1] - b[1]
        d = sqrt(x*x + y*y)
        return d
    
    def delay(self,old,d):
        if time() - old >= d:
            return True
        return False
    
    def Experience(self,xpgive):
        self.player.XP += xpgive
        self.player.XPmanage()
        print(f"XP : {self.player.XP}")
        print(f"niv:{self.player.LVL}")


    def kill(self,ennemi,degat):#enleve de la vie à l'ennemis, si il est mort, on le supprime et ont ajoute 1 au kill count
        ennemi.HP -= degat
        if ennemi.HP<=0:#si l'ennemis n'a plus de pv
            self.player.killcount += 1
            self.listEnnemis.remove(ennemi)#on supprime l'objet de l'ennemis mort
            self.group.remove(ennemi)#et on ne l'affiche plus
            self.Experience(ennemi.givenxp)
            return True
        return False

    
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
            
            if touche[pygame.K_SPACE] and self.delay(self.oldZone,self.player.zoneDelay):
                self.player.isZone = True
                self.zoneS.pos = self.player.pos
                self.zoneS.resize(self.player.zoneRange)
                self.group.add(self.zoneS)
                #affiche l'image de l'attaque de zone
                print("Zone attack")

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
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        self.timeStart = time()
        
        while running:

            if self.menu.PLAY and not self.menu.PAUSE:# 
            
                if self.listEnnemis == []:#4eme vague avec 180 elements = un peu beaucoup
                    aRemplir = True
                    self.nVague += 1
                    self.listitems.append(effect(randint(0,1000),randint(0,600)))
                    self.group.add(self.listitems[-1])

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
                    #faire en sorte que qu'il y ai des nombres à virgule
                
                for en in self.listEnnemis :
                    en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis
                    if self.delay(self.hitTime,self.player.invincibl):#temps d'invincibilité
                        dam = en.damage(self.player.pos,self.player.HP)#gestion des dégats au joueur
                        if(dam[1] == True):
                            self.player.HP = dam[0]
                            self.hitTime = time()


                    if self.distance(self.player.pos , en.pos) <= self.player.range and self.delay(self.oldFire,self.player.fireDelay) and self.player.pos != en.pos:#si un ennemis est dans la range on tire si l'attaque est rechargé et si on le joueur et l'ennemis ne sont pas a la meme position
                        self.oldFire = time()#actualisation de la derniere fois que l'on à tir
                        self.listFireball.append(fireBall(self.player.pos[0],self.player.pos[1],en.pos))
                        self.listFireball[-1].direction()
                        self.group.add(self.listFireball[-1])
                        self.music.explosion.play()         

                    if self.listFireball != []:                      
                        for fir in self.listFireball:
                            if en.hit(fir.pos):# or (en.hit(self.player.pos) and self.delay(self.oldAt,self.player.attackDelay)):#cas où une boule de feu touche un ennemi
                                #self.oldAt = time.time()
                                self.kill(en,fir.degat)
                                self.listFireball.remove(fir)#pareil pour la boule de feu qui à touché l'ennemis
                                self.group.remove(fir)
                                
                                break#pour ne pas retirer 2 fois un ennemis de la liste
                    else: 
                        if en.hit(self.player.pos) and self.delay(self.oldAt,self.player.attackDelay):#si le joueur attaque un ennemis au CAC
                            self.oldAt = time()
                            self.kill(en,self.player.degat)
                            if self.animation  == False :
                                self.animation = True
                                self.épée.image = pygame.image.load(f"Sprites/Move/anim_épée/anim_épée0.png")
                                self.num_anim = 0
                                self.épée.rect.x = self.player.pos[0]
                                self.épée.rect.y = self.player.pos[1]

                        elif self.player.isZone == True:#si le joueur fait une attaque de zone
                            if(self.distance(self.player.pos,en.pos)<= self.player.zoneRange):                              
                                self.kill(en,self.player.zoneDegat)
                                #faire l'attaque de zone et apres la boucle mettre isZone à false
                                
                
                if self.player.isZone == True:
                    self.player.isZone = False
                    self.group.remove(self.zoneS)#on désafiche l'image de la zone
                    self.oldZone = time()#si on le met avant seul le premier ennemis sera touché car oldZone s'actualise donc le delai va etre trop petit
                
                for fir in self.listFireball:
                    fir.move()
                    if self.distance(fir.startPos,fir.pos) > self.player.range:
                        self.listFireball.remove(fir)
                        self.group.remove(fir)
                
                for items in self.listitems:
                    if pygame.sprite.collide_rect(items,self.player) :
                        self.group.remove(items)
                
                if self.animation == True :#si il doit y avoir l'annimation du coup d'épé

                    if self.num_anim >= self.épée.taille_anim :#si c'est la derniere image on désafiche l'animation
                        self.animation = False
                        self.group.remove(self.épée)
                    else : 
                        if self.num_anim != 0 :
                            self.group.remove(self.épée)
                        self.group.add(self.épée)
                        self.num_anim += 1
                        self.épée.image = pygame.image.load(f"Sprites/Move/anim_épée/anim_épée{self.num_anim}.png")

                self.keybordinput()
                self.group.update() #update position du joueur
                self.xpbar.update()
                self.hpbar.ratio = self.player.ratio #update position du joueur
                self.xpbar.ratio = self.player.xpratio
                self.group.center(self.player.rect)
                pygame.display.update()
                
                self.group.draw(self.screen)
                self.screen.blit(self.xpbar.image,self.xpbar.rect)
                self.screen.blit(self.menu.pausebutton,self.menu.pauserect)
                
                if self.player.end(self.timeStart,time(),self.nVague):#On verifie si le joueur à toujour des pv
                    pygame.mixer.music.stop()
                    pygame.mouse.set_visible(True)
                    self.menu.gameover = True
                    self.menu.PLAY = False

            if self.menu.PAUSE :
                pygame.mixer.music.pause()
                self.Pausemenu()
            
            if not self.menu.PLAY and not self.menu.gameover:
                self.Startmenu()  
                
            elif self.menu.gameover:
                self.Gameovermenu()  #Si le joueur 
            
            if self.menu.SETTINGS :
                self.Settingsmenu()   

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
                    pygame.mixer.music.unpause()
                    pygame.mouse.set_visible(False)
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.gorect.collidepoint(event.pos) and self.menu.gameover:
                    self.menu.gameover = False 
                    pygame.mouse.set_visible(False)
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.setrect.collidepoint(event.pos) and not self.menu.PLAY and not self.menu.SETTINGS:
                    self.menu.SETTINGS = True
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.quitbutton.collidepoint(event.pos) and self.menu.SETTINGS:
                    self.menu.SETTINGS = False

                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()

                
            #evenement du jeu:
            