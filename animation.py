import pygame

from spritesheet import SpriteSheet


class Animation:
    def __init__(self):
        self.walking = False
        self.prev_dir = None  # Direction du dernier mouvement. Permet de savoir si le joueur à changé de direction
        self.direction = "S"  # par défaut le joueur regarde vers le bas (permet au joueur de voir son visage -> position neutre)
        self.frame_rate = 8  # l'animation change toutes les 8 frames
        self.current_frame = 0
        self.player_waking_images_north = SpriteSheet("assets/Spritesheets/Walking-North_Link.png").images(1, 10)
        self.player_waking_images_south = SpriteSheet("assets/Spritesheets/Walking-South_Link.png").images(1, 10)
        self.player_waking_images_west = SpriteSheet("assets/Spritesheets/Walking-West_Link.png").images(1, 10)

        self.walking_index = 0  # Numéro de l'image actuelle

    def get_current_image(self):
        """
        Fonction qui permet de récupérer l'image à afficher selon la direction du joueur et son walking_index
        """
        if self.direction == "E":
            if self.prev_dir != "E":
                self.prev_dir = "E"
                self.walking_index = 0
            current_image = pygame.transform.flip(self.player_waking_images_west[self.walking_index], True, False)
        elif self.direction == "W":
            if self.prev_dir != "W":
                self.prev_dir = "W"
                self.walking_index = 0
            current_image = self.player_waking_images_west[self.walking_index]
        elif self.direction == "N":
            if self.prev_dir != "N":
                self.prev_dir = "N"
                self.walking_index = 0
            current_image = self.player_waking_images_north[self.walking_index]
        elif self.direction == "S":
            if self.prev_dir != "S":
                self.prev_dir = "S"
                self.walking_index = 0
            current_image = self.player_waking_images_south[self.walking_index]
        return current_image

    def update(self, step):
        """
        Fonction qui permet de faire défiler les images pour créer l'animation
        """
        self.current_frame += 1
        if self.current_frame >= self.frame_rate:
            self.current_frame = 0
            if self.walking_index < 10-step:
                self.walking_index += step
            else:
                self.walking_index = 0
