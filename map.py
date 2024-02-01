import pygame
import pytmx
import pyscroll
from collisions import Collisions


class Map:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.map_data = None

        # switch to map0
        self.switch_map("city0(spawn)")

    def switch_map(self, map):
        # load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\{map}.tmx")
        # get the map for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        # render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size(), zoom=1)
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)
        self.map_layer._x_offset = 240

        self.group.add(self.player)

        # print(self.tmx_data.objects)
        self.sprite_list = []
        for i in self.tmx_data.visible_layers:
            print(i)

            if isinstance(i, pytmx.TiledObjectGroup):
                for j in i:
                    if i.name == "collisions":
                        self.sprite_list.append(Collisions(j.width, j.height, None, j.x, j.y))

        for j in self.sprite_list:
            j.add(self.group)

        self.group.center(self.player.pos.get())

    def update(self):
        # show the map on screen with the player centered
        self.group.center(self.player.pos.get())
        self.group.draw(self.screen.get_display())

    def get_size(self):
        """
        Renvoie la taille de la map en pixel dans un tuple
        """
        return self.map_data.map_size[0] * 16, self.map_data.map_size[1] * 16
