import pygame

from spritesheet import SpriteSheet


class Animation:
    def __init__(self, walking_north=None, walking_south=None, walking_west=None, walking_east=None, idle=None):
        self.prev_dir = None  # Direction du dernier mouvement. Permet de savoir si le joueur à changé de direction
        self.direction = "S"  # par défaut le joueur regarde vers le bas (permet au joueur de voir son visage -> position neutre)
        self.frame_rate = 8  # l'animation change toutes les 8 frames
        self.current_frame = 0
        self.walking_north = walking_north
        self.walking_south = walking_south
        self.walking_west = walking_west
        self.walking_east = walking_east
        self.idle = idle

        self.walking_index = 0  # Numéro de l'image actuelle

    def get_current_image(self):
        """
        Fonction qui permet de récupérer l'image à afficher selon la direction du joueur et son walking_index
        """
        if self.direction == "E":
            if self.prev_dir != "E":
                self.prev_dir = "E"
                self.walking_index = 0
            if self.walking_east is not None:
                current_image = self.walking_east[self.walking_index]
            else:
                current_image = pygame.transform.flip(self.walking_west[self.walking_index], True, False)
        elif self.direction == "W":
            if self.prev_dir != "W":
                self.prev_dir = "W"
                self.walking_index = 0
            if self.walking_west is not None:
                current_image = self.walking_west[self.walking_index]
            else:
                current_image = pygame.transform.flip(self.walking_east[self.walking_index], True, False)
        elif self.direction == "N":
            if self.prev_dir != "N":
                self.prev_dir = "N"
                self.walking_index = 0
            current_image = self.walking_north[self.walking_index]
        elif self.direction == "S":
            if self.prev_dir != "S":
                self.prev_dir = "S"
                self.walking_index = 0
            current_image = self.walking_south[self.walking_index]
        return current_image

    def update(self, step):
        """
        Fonction qui permet de faire défiler les images pour créer l'animation
        """
        self.current_frame += 1
        if self.current_frame >= self.frame_rate:
            self.current_frame = 0
            if self.direction == "E" and self.walking_east is not None:
                if self.walking_index < len(self.walking_east)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
            elif self.direction == "E":
                if self.walking_index < len(self.walking_west)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
            elif self.direction == "W" and self.walking_west is not None:
                if self.walking_index < len(self.walking_west)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
            elif self.direction == "W":
                if self.walking_index < len(self.walking_east)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
            elif self.direction == "N":
                if self.walking_index < len(self.walking_north)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
            elif self.direction == "S":
                if self.walking_index < len(self.walking_south)-step:
                    self.walking_index += step
                else:
                    self.walking_index = 0
