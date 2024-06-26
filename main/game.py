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

class Play:

    def __init__(self): #fenêtre du jeu
        
        self.screen = pygame.display.set_mode((1280, 768))

        pygame.mouse.set_visible(False)
        self.newcursor = pygame.image.load("Sprites/Cursor/Cursor.png")
        
        self.menu = Menu(self.screen)
        
        pygame.display.set_caption("Survival & Monsters","Sprites/Cursor/Cursor.png")
        
        #charger la carte 
        tmx_data = pytmx.util_pygame.load_pygame('Maps/Levels/Mapita.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

    #constantes utiles pour l'écriture de texte
        self.setfont = pygame.font.SysFont("CopperPlate Gothic",40)
        self.textcooldown = 100
        self.writet=False
        self.writeele = ""
        
        
        #volume:
        paramFichier = open("main/param.txt","r")#fichier qui contient les parametres
        for i in paramFichier :
            l = i.split(":")#les parametres (pour l'instant il n'y en a qu'un) sont sous la forme param:val
            if l[0] == "vol": 
                self.volume = int(l[1])
                

        self.bord = []#zone interdite
        self.zone = []#zone disponible
        

        for obj in tmx_data.objects :
            if obj.name == "colisiones":
               self.bord.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            if obj.name == "pop":
               self.zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

    def game_init(self):
        
        #générer le joueur
        self.player = Player(500,500)
        self.zoneS = zoneAf(self.player.zoneRange)

        self.hpbar = HPbar(self.player.pos[0],self.player.pos[1],self.player.ratio,self.player.speed)
        self.xpbar = XPbar(self.player.pos[0],self.player.pos[1],self.player.xpratio)

        #listes qui contiennent les différents objets
        self.listEnnemis = []
        self.listitems = []
        self.listFireball = []


        self.tailleVague = 5 #taille de la premiere vague d'ennemis
        self.coefVague = 4
        self.nVague = 0#numéro de la vague
        

        self.animation = False#variable qui dit si une annimation est en cours
        self.num_anim = 0
        self.épée = Animations_sprites(self.player.pos[0],self.player.pos[1])

        self.music = sound()
        self.listEtape = [1,2,3,4,5,6]#liste des vagues où la musique évolue
        self.nbMus = len(self.listEtape)
        self.etape = 0

        self.oldFire = 0#moment auquel la derniere fireBall à été tiré
        self.oldAt = 0#moment auquel à eu lieu la derniere attaque au corp à corp
        self.oldZone = 0#moment de la derniere attacke de zone
        self.hitTime = 0#moment du dernier coup recu
        
        self.visible = True#Booléen qui indique si le personnage est visibe
        
        #dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1 )
        self.group.add(self.player)
        self.group.add(self.listEnnemis)
        self.group.add(self.listitems)
        self.group.add(self.hpbar)

    def distance(self,a,b):#fonction qui calcule la distance entre 2 points
        x = a[0] - b[0]
        y = a[1] - b[1]
        d = sqrt(x*x + y*y)
        return d
    
    def delay(self,old,d):#fonction qui vérifie si assez de temps se s'est écoulé
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

    def modifParam(self,param,val):#fonction  qui modifie un paramtre dans le fichier parametre
        paramFichier = open("main/param.txt","r")
        
        lines = []#On sauve les lignes qui ne changent pas
        for i in paramFichier:
            if i.split(":")[0] == param:#on modifie celle qui nous interesse
                lines.append(i.split(":")[0]+":"+str(val))
            else :
                lines.append(i)
        paramFichier.close()

        paramFichier = open("main/param.txt","w")
        for l in lines:#on réécrit le fichier
            paramFichier.write(l)
        paramFichier.close()

    def modifVol(self,old):
        if old != self.volume:#si le volume à été modifié:
            self.modifParam("vol",self.volume)  

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
            
            if touche[pygame.K_LEFT]:
                self.player.go_left()
                        
            if touche[pygame.K_RIGHT]:
                self.player.go_right()
                
            if touche[pygame.K_DOWN]:
                self.player.go_down()
                
            if touche[pygame.K_SPACE] and self.delay(self.oldZone,self.player.zoneDelay):
                self.player.isZone = True
                self.zoneS.pos = self.player.pos
                self.zoneS.resize(self.player.zoneRange)
                self.group.add(self.zoneS)
                #affiche l'image de l'attaque de zone

    def write(self,text,x,y): #écrire
        todisplay = self.setfont.render(text,True,(0,255,0))
        self.screen.blit(todisplay,(x,y))

    def writeingame(self): #écrire en game
        if self.textcooldown>0:
            self.textcooldown -= 1
            self.write(self.writeele,(self.screen.get_width()/10)*4,(self.screen.get_height()/10)*7)
        else:
            self.textcooldown = 100
            self.writet = False

#gestion des écrans
    def Startmenu(self):
        self.screen.blit(self.menu.pressplay, (0, 0))
        self.screen.blit(self.menu.playbutton,self.menu.press)
        self.screen.blit(self.menu.settingsimage,self.menu.setrect)
        self.game_init()
        if not pygame.mixer.music.get_busy():#si il n'y a pas de musique on lance celle du menu
            self.music.playMus(self.music.musicMenu,self.volume)

    def Gameovermenu(self):
        self.group.draw(self.screen)
        self.screen.blit(self.menu.gameoverscreen,self.menu.gorect) 
        self.write("GAME OVER",(self.screen.get_width()/10)*4,(self.screen.get_height()/10))
        self.write(f"SCORE:{self.player.totalXP}",(self.screen.get_width()/10)*4,(self.screen.get_height()/5)*3)
        if self.player.maxscore == -1:#si c'est la premiere partie joué
            pass
        elif self.player.maxscore < self.player.totalXP :#si on bat le meilleur score
            self.write(f"NOUVEAU RECORD !!!",(self.screen.get_width()/10)*4,(self.screen.get_height()/5)*3+30)
            self.write(f"L'ancien record était de :{self.player.maxscore} ",(self.screen.get_width()/10)*4,(self.screen.get_height()/5)*3+60)
        else :
            self.write(f"RECORD:{self.player.maxscore} ",(self.screen.get_width()/10)*4,(self.screen.get_height()/5)*3+30)

        for i in self.group:
            if i != self.player: self.group.remove(i)

    def Pausemenu(self):
            self.group.draw(self.screen)
            self.screen.blit(self.menu.pausemenu,((self.screen.get_width()/30)*5,(self.screen.get_height()/20)*2))
            self.screen.blit(self.menu.resumebutton,self.menu.resumerect)
            self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
            self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)
            self.write(f"Volume: {self.volume}",(self.screen.get_width()/20)*9,(self.screen.get_height()/10)*2+150)
    
    def Settingsmenu(self):
        self.screen.blit(self.menu.pausemenu,((self.screen.get_width()/30)*5,(self.screen.get_height()/20)*2))
        self.screen.blit(self.menu.quit,self.menu.quitbutton)
        self.screen.blit(self.menu.quit,self.menu.resumerect)
        self.screen.blit(self.menu.volumeplus,self.menu.plusbutton)
        self.screen.blit(self.menu.volumeminus,self.menu.minusbutton)
        self.write(f"{self.volume}",(self.screen.get_width()/31)*16,(self.screen.get_height()/10)*2+300)
        self.write("  CREDIT: Ernest Niederman,", (self.screen.get_width()/8)*2+10,(self.screen.get_height()/10)*2+20)
        self.write("  Francisco Ernesto Suarez Roca, ",(self.screen.get_width()/8)*2+10,(self.screen.get_height()/10)*2+60)
        self.write("  Nicolas-Thomas Marie-Sainte,", (self.screen.get_width()/8)*2+10,(self.screen.get_height()/10)*2+100)
        self.write("  Lohan Morvan",(self.screen.get_width()/8)*2+10,(self.screen.get_height()/10)*2+140)
        self.write("  Remerciment pour la musique : Kiri",(self.screen.get_width()/8)*2+10,(self.screen.get_height()/10)*2+180)

    def update(self):
        
        self.group.update()
        
        self.xpbar.update()
        self.hpbar.ratio = self.player.ratio #update position du joueur
        self.xpbar.ratio = self.player.xpratio
        for en in self.listEnnemis:
            if en.rect.collidelist(self.bord) > -1 : 
                en.rollback()
        if self.player.rect.collidelist(self.bord) > -1 : 
            self.player.rollback()
        self.hpbar.updatepos(self.player.pos[0],self.player.pos[1])
    
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
                    a = randint(0,8)
                    self.listitems.append(effect(randint(self.zone[a].x,self.zone[a].x+self.zone[a].width),randint(self.zone[a].y,self.zone[a].y+self.zone[a].height)))#création d'un nouvel ennemi à des positions random 
                    self.group.add(self.listitems[-1])

                    if self.etape < self.nbMus and self.nVague >=self.listEtape[self.etape]:
                        #La musique evolue au fil des vagues
                        self.music.playMus(self.music.listMus[self.etape],self.volume)
                        self.etape += 1

                    self.tailleVague = self.tailleVague*self.coefVague

                if aRemplir == True:   
                    a = randint(0,8)
                    self.listEnnemis.append(ennemi(randint(self.zone[a].x,self.zone[a].x+self.zone[a].width),randint(self.zone[a].y,self.zone[a].y+self.zone[a].height)))#création d'un nouvel ennemi à des positions random 
                    self.group.add(self.listEnnemis[-1])#affichage du dernier ennemi

                if len(self.listEnnemis) == self.tailleVague and aRemplir == True:#Si on  a ajouter le bon nombre d'ennemis
                    aRemplir = False
                    self.coefVague = self.coefVague * 0.6#plus on avance plus le coef de multiplication de la taille des vagues diminue
                    if self.coefVague<1:#pour que la taile des vagues ne diminue pas
                        self.coefVague = 1.3
                
                for en in self.listEnnemis :#pour chaque ennemis
                    
                    delete = False#Booléen pour savoir si l'ennemis a été supprimé
                    en.saveloc()
                    en.moveTo(self.player.pos[0],self.player.pos[1])#deplacement de l'ennemis

                    

                    if self.player.LVL >3 and self.distance(self.player.pos , en.pos) <= self.player.range and self.delay(self.oldFire,self.player.fireDelay) and self.player.pos != en.pos:#si un ennemis est dans la range on tire si l'attaque est rechargé et si on le joueur et l'ennemis ne sont pas a la meme position
                        
                        pygame.mixer.Sound.play(self.music.fireBallSound)
                        pygame.mixer.Sound.set_volume(self.music.fireBallSound,float(self.volume)/10)
                        self.oldFire = time()#actualisation de la derniere fois que l'on à tir
                        self.listFireball.append(fireBall(self.player.pos[0],self.player.pos[1],en.pos))#on ajoute une boule de feu 
                        self.listFireball[-1].image = pygame.transform.rotate(self.listFireball[-1].image,direction(self.listFireball[-1].cible,self.listFireball[-1].startPos))#on l'oriente dans la bonne direction
                        self.group.add(self.listFireball[-1])#et on l'affiche
                              

                    if self.listFireball != []:                      
                        for fir in self.listFireball:#pour chaque boulle de feu
                            if en.hit(fir.rect):#Si elle touche un ennemis
                               
                                pygame.mixer.Sound.play(self.music.explosionSound)#Jouer le bruit de l'xplosion
                                pygame.mixer.Sound.set_volume(self.music.explosionSound,float(self.volume)/10)
                                delete = self.kill(en,fir.degat)#Si l'ennemis n'as plus de vie on le suprime
                                self.group.remove(fir)#On désafiche la boule de feu 
                                self.listFireball.remove(fir)#et on la supprime
        
                    if en.hit(self.player.rect) and self.delay(self.oldAt,self.player.attackDelay) and delete == False:#si le joueur touche l'ennemis, peut l'attaquer et qu'il n'a pas encore été supprimé
                        
                        pygame.mixer.Sound.play(self.music.epeeSound)
                        pygame.mixer.Sound.set_volume(self.music.epeeSound,float(self.volume)/10)
                        self.oldAt = time()
                        delete = self.kill(en,self.player.degat)
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
                            delete = self.kill(en,self.player.zoneDegat)

                    if self.delay(self.hitTime,self.player.invincibl):#Si le joueur n'est pas en état d'invicibilité
                        if not self.player.shield:#Si le joueur n'a pas de bouclier 
                            dam = en.damage(self.player.pos,self.player.HP)#gestion des dégats au joueur
                            if(dam[1] == True):#Si le joueur prend des dégats
                              
                                pygame.mixer.Sound.play(self.music.listDegatSound[randint(0,3)])
                                pygame.mixer.Sound.set_volume(self.music.listDegatSound[randint(0,3)],float(self.volume)/10)
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
                        items.use(self)
                        self.writeele = items.comment
                        self.writet = True
                        self.listitems.remove(items)
                        self.group.remove(items)
                  
                if self.delay(self.hitTime,self.player.invincibl) == False:
                    self.visible = self.player.invincibility(self.visible)
                
                elif self.visible == False:#permet d'eviter de laisser le joueur invisible si à la fin de l'animation il est invisible
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

                self.player.saveloc()
                self.keybordinput()
                self.update()

                self.group.center(self.player.rect)
                
                pygame.display.update()  
                                
                self.group.draw(self.screen)
                self.screen.blit(self.xpbar.image,self.xpbar.rect)
                if self.writet : self.writeingame()
                self.screen.blit(self.menu.pausebutton,self.menu.pauserect)

                if self.player.LVLED: 
                    if self.xpbar.it == 100:
                        self.player.LVLED = False
                        self.xpbar.it = 0
                    else:
                        self.write(self.player.p,500,0)
                        self.screen.blit(self.xpbar.LVLimage,self.xpbar.rect)
                        self.xpbar.it += 1

                if self.player.end(self.timeStart,time(),self.nVague):#Si le joueur n'a plus de points de vie
                    pygame.mixer.music.stop()#On arrete la musique
                    self.menu.gameover = True
                    self.menu.PLAY = False

            if self.menu.PAUSE :
                self.Pausemenu()
            
            if not self.menu.PLAY and not self.menu.gameover:
                self.Startmenu()  
                
            elif self.menu.gameover:
                self.Gameovermenu() 
            
            if self.menu.SETTINGS :
                self.Settingsmenu()

            mousepos = pygame.mouse.get_pos()
            self.screen.blit(self.newcursor,mousepos)
            
            pygame.display.update()
            clock.tick(30) #limiter les FPS

            self.music.update(self.volume)
  
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.press.collidepoint(event.pos) and not self.menu.PLAY and not self.menu.SETTINGS and not self.menu.gameover:
                    self.menu.PLAY = True #SI ON APPUIE SUR PLAY LE JEU SE LANCE 
                    pygame.mixer.music.stop()  
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.pauserect.collidepoint(event.pos) and self.menu.PLAY and not self.menu.gameover :#Bouton pour mettre en pause le jeu
                    self.menu.PAUSE = True #SI ON APPUIE SUR PAUSE LE JEU SE LANCE
                    oldVol = self.volume
                    pygame.mixer.music.pause()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.resumerect.collidepoint(event.pos) and self.menu.PAUSE:#Bouton pour revenir au jeu
                    self.menu.PAUSE = False#tu clique trop vite il te faut juste un menue
                    self.modifVol(oldVol)#on regarde si le volume à été modifié
                    pygame.mixer.music.unpause()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.gorect.collidepoint(event.pos) and self.menu.gameover:
                    self.menu.gameover = False 
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.setrect.collidepoint(event.pos) and not self.menu.PLAY and not self.menu.SETTINGS:#Bouton pour accéder aux parametres
                    self.menu.SETTINGS = True
                    oldVol = self.volume
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.quitbutton.collidepoint(event.pos) and self.menu.SETTINGS:#Bouton pour quitter les parametres
                    self.menu.SETTINGS = False
                    self.modifVol(oldVol)#on regarde si le volume à été modifié
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.minusbutton.collidepoint(event.pos) and (self.menu.SETTINGS or self.menu.PAUSE):
                    if self.volume > 0 :
                        self.volume -= 1

                
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu.plusbutton.collidepoint(event.pos) and (self.menu.SETTINGS or self.menu.PAUSE):
                    if self.volume < 10 : self.volume += 1

                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
            