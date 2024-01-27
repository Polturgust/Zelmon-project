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
        # initialise the map
        self.map = Map(self.screen)
        # create a player
        self.player = Player(self, self.screen)

        # on crée un dictionnaire qui contient les touches pressées (permet de rester appuyé sur une touche --> utile pour se déplacer)
        self.pressed = dict()

    def run(self):
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

            # checking currently pressed keys and doing the according actions
            # Player movement
            if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:
                self.player.move("up")
            elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y < self.screen.height:
                self.player.move("down")
            if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
                self.player.move("left")
            elif self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < self.screen.width:
                self.player.move("right")

            # update map
            self.map.update()

            # update player
            self.player.update()

            # update screen
            self.screen.update()
        pygame.quit()
