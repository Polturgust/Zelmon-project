import pygame


class Menus:
    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.running = True
        self.pressed = {}

    def update(self):
        while self.running:
            self.screen.update()
            self.map.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            if pygame.K_ESCAPE in self.pressed.keys():
                self.running = False
