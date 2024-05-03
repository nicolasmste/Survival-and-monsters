import pygame

class Animations_sprites(pygame.sprite.Sprite) :

    #definir les choses à faire à la création de l'entité 
    def __init__(self, sprite_name,x,y) :
        super().__init__()
        self.current_image = 0
        self.image = pygame.image.load(f"Sprites/Move/anim_epee/anim_epee0.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.image = animations.get(sprite_name)
        self.animation= False
        self.taille_anim = 13
        self.pos = [x,y]
        #self.image_li = [pygame.image.load("Sprites/Move/anim_épée/anim_épée0.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée1.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée2.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée3.png"),
        #pygame.image.load("Sprites/Move/anim_épée/anim_épée4.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée5.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée6.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée7.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée8.png"),
        #pygame.image.load("Sprites/Move/anim_épée/anim_épée9.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée10.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée11.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée12.png"),pygame.image.load("Sprites/Move/anim_épée/anim_épée13.png")]

#     #définir une méthode pour démarrer l'Animations
#     def start_animation(self) :
#         self.animation = True

#     def animate(self) :     #definir une méthode pour animer le sprite 
#         if self.animation : #vérifie si l'animation est active 
#             self.current_image += 1
#             if self.current_image >= len(get_images) :     #vérifie si on a atteint la fin de l'animation 
#                 self.current_image = 0
#                 self.animation = False
#             self.image = self.get_images[self.current_image]    #modifie l'image précédente par la suivante

#     #def coup(self,x,y) :# pour faire l'animation du coup d'épée
#     #    self.pos = [x,y]
#     #    self.start_animation()
#     #    for i in range(len(get_images)) :
#     #        update_animation()



# def load_images(sprite_name,long) :     #passe à l'image suivante
#     get_images = []
#     path = f"Sprites/Move/anim_épée/{sprite_name}"
#     for num in range(long) :                             #mets les sprites dans une liste
#         image_path = path + str(num) + ".png"
#         get_images.append(pygame.image.load(image_path))    #ajoute les sprites dans une liste 
#     return get_images

# animations = {
#     "anim_épée" : load_images("anim_épée",14)
# }
