import pygame

from screen import Screen
from map import Map
from player import Player


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        # initialise the screen
        self.screen = Screen()
        # create a player
        self.player = Player(self)
        # initialise the map
        self.map = Map(self.screen, self.player)

        self.player.move("E")

        self.last_move = ""
        self.inverse = {"NW": "SE", "NE": "SW", "SW": "NE", "SE": "NW", "N": "S", "S": "N", "E": "W", "W": "E"}
        # on crée un dictionnaire qui contient les touches pressées (permet de rester appuyé sur une touche --> utile pour se déplacer)
        self.pressed = dict()

    def run(self):
        print(self.screen.get_size())
        # while the game is running
        while self.running:
            # capture all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # close the game if the cross is pressed
                    self.running = False
                elif event.type == pygame.KEYDOWN:  # if a key is pressed
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False  # if a key is released

            # Checking currently pressed keys and doing the according actions

            # Player movement
            # sans le -30 on peut sortir de l'écran je pense que c'est dû à la largeur du carré (ses coordonnées sont le point en haut à gauche)
            if self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] > 0 and self.player.pos.get()[0] < self.screen.get_size()[0] - 30:
                self.player.move("NE")
                self.last_move = "NE"
            elif self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] > 0 and self.player.pos.get()[0] > 0:
                self.player.move("NW")
                self.last_move = "NW"
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30 and self.player.pos.get()[0] < self.screen.get_size()[0] - 30:
                self.player.move("SE")
                self.last_move = "SE"
                print(self.player.pos.get())
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30 and self.player.pos.get()[0] > 0:
                self.player.move("SW")
                self.last_move = "SW"
            elif self.pressed.get(pygame.K_UP) and self.player.pos.get()[1] > 0:
                self.player.move("N")
                self.last_move = "N"
            elif self.pressed.get(pygame.K_DOWN) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30:
                self.player.move("S")
                self.last_move = "S"
            elif self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[0] > 0:
                self.player.move("W")
                self.last_move = "W"
            elif self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[0] < self.screen.get_size()[0]:
                self.player.move("E")
                self.last_move = "E"

            # Vérifie si le joueur est en collision avec un élément du décor
            for i in self.map.group:
                if self.player.rect.colliderect(i.rect) and not isinstance(i, Player):
                    print("Collision détectée >:(")
                    self.player.move(self.inverse[self.last_move])
            # update map
            self.map.update()

            # update player
            # if the screen still scrolls make the player appear in the center

            # self.screen.get_display().blit(self.player.image, (self.player.pos.get()))




            # update screen
            self.screen.update()
        pygame.quit()
