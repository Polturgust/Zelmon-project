import pygame

from screen import Screen
from map import Map
from player import Player


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        # create a player
        self.player = Player(self)
        # initialise the screen
        self.screen = Screen()
        # initialise the map
        self.map = Map(self.screen, self.player
                       )

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
            elif self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] > 0 and self.player.pos.get()[0] > 0:
                self.player.move("NW")
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30 and self.player.pos.get()[0] < self.screen.get_size()[1] - 30:
                self.player.move("SE")
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30 and self.player.pos.get()[0] > 0:
                self.player.move("SW")
            elif self.pressed.get(pygame.K_UP) and self.player.pos.get()[1] > 0:
                self.player.move("N")
            elif self.pressed.get(pygame.K_DOWN) and self.player.pos.get()[1] < self.screen.get_size()[1] - 30:
                self.player.move("S")
            elif self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[0] > 0:
                self.player.move("W")
            elif self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[0] < self.screen.get_size()[0] - 30:
                self.player.move("E")

            # update map
            self.map.update()

            # update player
            # if the screen still scrolls make the player appear in the center
            if self.screen.get_size()[0] // 4 < self.player.pos.get()[0] < 3 * self.screen.get_size()[0] // 4 and self.screen.get_size()[1] // 4 < self.player.pos.get()[1] < 3 * self.screen.get_size()[1] // 4:
                self.screen.get_display().blit(self.player.image, (self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2))
            elif self.screen.get_size()[0] // 4 < self.player.pos.get()[0] < 3 * self.screen.get_size()[0] // 4:
                self.screen.get_display().blit(self.player.image, (self.player.pos.get()[0], self.screen.get_size()[1]//2))
            elif self.screen.get_size()[1] // 4 < self.player.pos.get()[1] < 3 * self.screen.get_size()[1] // 4:
                self.screen.get_display().blit(self.player.image, (self.screen.get_size()[0]//2, self.player.pos.get()[1]))

            # else move the player himself
            else:
                self.screen.get_display().blit(self.player.image, (self.player.pos.get()))

            # update screen
            self.screen.update()

            for i in self.map.sprite_list:
                i.update()
        pygame.quit()
