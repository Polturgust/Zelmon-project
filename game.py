import pygame

from screen import Screen
from map import Map



class Game:
    def __init__(self):
        #set the game to running
        self.running = True
        #initialise the screen
        self.screen = Screen()
        #initialise the map
        self.map = Map(self.screen)


    def run(self):
        #while the game is running
        while self.running:
        
            # close the game if the cross is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #update map
            self.map.update()
            #update screen
            self.screen.update()