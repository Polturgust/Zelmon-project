import pygame
import pytmx
import pyscroll

from screen import Screen

class Map:
    def __init__(self, screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        #swich to map0
        self.switch_map("map0")


    def switch_map(self, map):
        #load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\map0.tmx")
        #get the map for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        #render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        #puts everythong together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)


    def update(self):
        #show the map on screen
        self.group.draw(self.screen.get_display())