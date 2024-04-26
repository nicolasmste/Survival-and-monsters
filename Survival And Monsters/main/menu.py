import pygame


class Menu:
    def __init__(self,screen):
        self.PLAY = False


       #ECRAN DE DEBUT 
        self.pressplay = pygame.image.load('Menus/FOND.png')
       #SETTINGS 
        self.SETTINGS = False
        self.playbutton = pygame.image.load('Menus/PRESSPLAY.png')
        self.settingsimage = pygame.image.load('Menus/SETTINGS.png')
        self.setrect = self.settingsimage.get_rect()
        self.press = self.playbutton.get_rect()
        self.press.x = screen.get_width()/3
        self.press.y = screen.get_height()/3
        self.setrect.x = self.press.x
        self.setrect.y = (self.press.y)+200

        self.volumeplus = pygame.image.load('Menus/VOLUME+.png')
        self.plusbutton = self.volumeplus.get_rect()
        self.plusbutton.x = (screen.get_width()/4)*2.12
        self.plusbutton.y = (screen.get_height()/4)*2.2
        self.quit = pygame.image.load('Menus/quit.png')
        self.quitbutton = self.volumeplus.get_rect()
        self.quitbutton.x = (screen.get_width()/2)
        self.quitbutton.y = (screen.get_height()/2)
        self.volumeminus = pygame.image.load('Menus/VOLUME-.png')
        self.minusbutton = self.volumeminus.get_rect()
        self.minusbutton.x = (screen.get_width()/4)*1.9
        self.minusbutton.y = (screen.get_height()/4)*2.2

       #ECRAN DE PAUSE 
        self.PAUSE =False
        self.resumebutton = pygame.image.load('Menus/PAUSE.png')
        self.resumerect = self.resumebutton.get_rect()
        self.resumerect.x = (screen.get_width()/2)
        self.resumerect.y = (screen.get_height()/2)
        self.pausemenu = pygame.image.load('Menus/pausemenu.png')
        self.pausebutton = pygame.image.load('Menus/RESUME.png')
        self.pauserect = self.pausebutton.get_rect()
        self.pauserect.x = 1230
        self.pauserect.y = 20



       #Ecran de GAME OVER 
        self.gameover = False
        self.gameoverscreen = pygame.image.load('Menus/QUITGAME.png')
        self.gorect = self.gameoverscreen.get_rect()
        self.gorect.x = screen.get_width()/3
        self.gorect.y = (screen.get_height()/6)


        


    
  