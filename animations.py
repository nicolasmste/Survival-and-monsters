import pygame

class Animations_sprites(pygame.sprite.Sprite) :

    #definir les choses à faire à la création de l'entité 
    def __init__(self, sprite_name) :
        super().__init__()
        self.image = pygame.image.load(f"Sprites/Move/anim_épée/{sprite_name}.png")
        self.current_image = 0
        self.image = animations.get(sprite_name)
        self.animation= False

    #définir une méthode pour démarrer l'Animations
    def start_animation(self) :
        self.animation = True

    def animate(self) :     #definir une méthode pour animer le sprite 
        if self.animation : #vérifie si l'animation est active 
            self.current_image += 1
            if self.current_image >= len(self.images) :     #vérifie si on a atteint la fin de l'animation 
                self.current_image = 0
                self.animation = False
            self.image = self.images[self.current_image]    #modifie l'image précédente par la suivante

def load_images(sprite_name) :      #passe à l'image suivante
    images = []
    path = f"Sprites/Move/anim_épée/{sprite_name}"
    for num in range(1,14) :                             #mets les sprites dans une liste
        image_path = path + str(num) + ".png"
        images.append(pygame.image.load(image_path))
    return images

animations = {
    "anim_épée" : load_images("anim_épée")
}
