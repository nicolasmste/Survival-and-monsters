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

        #listes qui contiennent les différents objets
        self.listEnnemis = []
        self.listitems = []
        self.listFireball = []


        self.tailleVague = 10 #taille de la premiere vague d'ennemis
        self.coefVague = 1
        self.nVague = 0#numéro de la vague
        

        self.animation = False#variable qui dit si une annimation est en cours
        self.num_anim = 0
        self.épée = Animations_sprites('anim_épée',self.player.pos[0],self.player.pos[1])

        self.music = sound()
        self.listEtape = [1,3,4,5,6,7]#liste des vagues où la musique évolue
        self.nbMus = len(self.listEtape)
        self.etape = 0

        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au corp à corp
        self.oldZone = 0#moment de la derniere attacke de zone
        self.hitTime = 0#moment du dernier coup recu
        self.visible = True
        
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
    
    def orientation(self,angle):#permet d'orienter une image avec le bon angle (ici les boules de feux et  l'attaque)
        if angle < -45 and angle <=45:
            return ''
        if angle > 45 and angle <= 135:
            return "_haut"
        if angle > 135 or angle <-135:
            return "_g"
        else :
            return "_bas"
    
    def Experience(self,xpgive):#gère l'expérience
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

    
    def keybordinput(self) :#gère les actions du clavier
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

    def Startmenu(self):#menu d'acceuil
   
        self.screen.blit(self.menu.pressplay, (0, 0))
        self.screen.blit(self.menu.playbutton,self.menu.press)
        self.screen.blit(self.menu.settingsimage,self.menu.setrect)
        self.game_init()
        if not pygame.mixer.music.get_busy():#si il n'y a pas de musique on lance celle du menu
            self.music.playMus(self.music.musicMenu)

    def Gameovermenu(self):#menu de game over
        self.screen.blit(self.menu.gameoverscreen,self.menu.gorect) 
        self.listEnnemis = []
        for i in self.group:
            if i != self.player: self.group.remove(i)

    def Pausemenu(self):#menu pause
            self.screen.blit(self.menu.pausemenu,(0,0))
            self.screen.blit(self.menu.resumebutton,self.menu.resumerect)
            self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
            self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)
    
    def Settingsmenu(self):#menu des parametres (volume sonore et crédits)
        self.screen.blit(self.menu.pausemenu,(0,0))
        self.screen.blit(self.menu.quit,self.menu.quitbutton)
        self.screen.blit(self.menu.quit,self.menu.resumerect)
        self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
        self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)
    
    def run(self):
        
        clock = pygame.time.Clock() #Objet de type horloge
        #Boucle de run, (exit permet de sortir de la boucle quand on ferme la fenêtre)
        running = True
        self.timeStart = time()#temps auquel la partie à débuté
        
        while running:
            
            if self.menu.PLAY and not self.menu.PAUSE:#si on est dans la partie
                
                if self.listEnnemis == []:#Si il n'y a pas d'ennemis on les ajoute en fonction de la taille de la vague
                    aRemplir = True#on doit ajouter des ennemis
                    self.nVague += 1
                    self.listitems.append(effect(randint(0,1000),randint(0,600)))#On ajoute des ennemis
                    self.group.add(self.listitems[-1])#et on les fait apparaitre

                    if self.etape < self.nbMus and self.nVague >=self.listEtape[self.etape]:
                        #La musique evolue au fil des vagues
                        self.music.playMus(self.music.listMus[self.etape])
                        self.etape += 1

                    self.tailleVague = self.tailleVague*self.coefVague

                    #faire apparaitre les ennemis hors de la map

                if aRemplir == True:
                    self.listEnnemis.append(ennemi(randint(0,1000),randint(0,600)))#création d'un nouvel ennemi à des positions random 
                    self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi

                if len(self.listEnnemis) == self.tailleVague:#Si on  a ajouter le bon nombre d'ennemis
                    aRemplir = False
                    self.coefVague = randint(self.nVague,2*self.nVague)#plus on avance plus le coef de multiplication des vagues augmente
                
                for en in self.listEnnemis :#pour chaque ennemis
                    delete = False#Booléen pour savoir si l'ennemis a été supprimé
                    en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis

                    if self.player.LVL >1 and self.distance(self.player.pos , en.pos) <= self.player.range and self.delay(self.oldFire,self.player.fireDelay) and self.player.pos != en.pos:#si un ennemis est dans la range on tire si l'attaque est rechargé et si on le joueur et l'ennemis ne sont pas a la meme position
                        self.music.fireBallSound.play()
                        self.oldFire = time()#actualisation de la derniere fois que l'on à tir
                        self.listFireball.append(fireBall(self.player.pos[0],self.player.pos[1],en.pos))#on ajoute une boule de feu 
                        self.listFireball[-1].image = pygame.transform.rotate(self.listFireball[-1].image,direction(self.listFireball[-1].cible,self.listFireball[-1].startPos))#on l'oriente dans la bonne direction
                        self.group.add(self.listFireball[-1])#et on l'affiche
                              

                    if self.listFireball != []:                      
                        for fir in self.listFireball:#pour chaque boulle de feu
                            if en.hit(fir.rect):#Si elle touche un ennemis
                                self.music.explosionSound.play()#Jouer le bruit de l'xplosion
                                delete = self.kill(en,fir.degat)#Si l'ennemis n'as plus de vie on le suprime
                                self.group.remove(fir)#On désafiche la boule de feu 
                                self.listFireball.remove(fir)#et on la supprime
        
                    if en.hit(self.player.rect) and self.delay(self.oldAt,self.player.attackDelay) and delete == False:#si le joueur touche l'ennemis, peut l'attaquer et qu'il n'a pas encore été supprimé
                        self.music.epeeSound.play()
                        self.oldAt = time()
                        self.kill(en,self.player.degat)
                        if self.animation == False:#si l'annimation du coup d'épée n'est pas cours
                            self.animation = True
                            self.cote = self.orientation(direction(en.pos,self.player.pos))#savoir de quelle coté vient l'ennemis et d'orienter le coup dans la bonne direction
                            self.épée.image = pygame.image.load(f"Sprites/Move/anim_epee{self.cote}/anim_epee{self.cote}0.png")#
                            self.num_anim = 0
                            self.épée.rect.x = self.player.pos[0]#place l'annimation sur le joueur
                            self.épée.rect.y = self.player.pos[1]
                            if self.cote == "_haut":
                                self.épée.rect.y -= 32
                            if self.cote == "_g":
                                self.épée.rect.x -= 32

                    if self.player.isZone == True and delete == False:#si le joueur fait une attaque de zone
                        if(self.distance(self.player.pos,en.pos)<= self.player.zoneRange):#si l'ennemi est dans le rayon de l'attaque                        
                            self.kill(en,self.player.zoneDegat)

                    if self.delay(self.hitTime,self.player.invincibl):#Si le joueur n'est pas en état d'invicibilité
                        dam = en.damage(self.player.rect,self.player.HP)#gestion des dégats au joueur
                        if(dam[1] == True):#Si le joueur prend des dégats
                            self.music.listDegatSound[randint(0,3)].play()
                            self.player.HP = dam[0]#On met à jour les points de vie du joueur en fonction des dégats infligé par l'ennemi
                            self.hitTime = time()#On actualise le temps de du dernier coup reçu    
                
                if self.player.isZone == True:#si il y avait une attaque de zone on l'enleve
                    self.player.isZone = False
                    self.group.remove(self.zoneS)#on désafiche l'image de la zone
                    self.oldZone = time()#si on le met avant seul le premier ennemis sera touché car oldZone s'actualise donc le delai va etre trop petit
                
                for fir in self.listFireball:#Pour chaque boule de feu
                    fir.move()#on la déplace
                    if self.distance(fir.startPos,fir.pos) > self.player.range:#Si on elle est dépace la portée
                        self.group.remove(fir)#On la désafiche
                        self.listFireball.remove(fir)#On la supprime
                
                for items in self.listitems:
                    if pygame.sprite.collide_rect(items,self.player) :
                        self.group.remove(items)
                  
                if self.delay(self.hitTime,self.player.invincibl) == False:
                    self.visible = self.player.invincibility(self.visible)
                
                elif self.visible == False:#permet d'eviter de laiser le joueur invisible si à la fin de l'animation il est invisible
                    self.player.image = pygame.image.load('Sprites/Character/Base.png')
                    self.visible = True

                if self.animation == True :#si il doit y avoir l'annimation du coup d'épé

                    if self.num_anim >= self.épée.taille_anim :#si c'est la derniere image on désafiche l'animation
                        self.animation = False
                        self.group.remove(self.épée)
                    else : 
                        if self.num_anim != 0 :
                            self.group.remove(self.épée)
                        
                        self.group.add(self.épée)
                        self.num_anim += 1
                        self.épée.image = pygame.image.load(f"Sprites/Move/anim_epee{self.cote}/anim_epee{self.cote}{self.num_anim}.png")

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
                
                if self.player.end(self.timeStart,time(),self.nVague):#Si le joueur n'a plus de points de vie
                    pygame.mixer.music.stop()#On arrete la musique
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
                    pygame.mixer.music.stop()
                
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
            