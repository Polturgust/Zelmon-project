import pygame
import pytmx
import pyscroll


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
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size(), zoom=2)
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)

        self.group.add(self.player)

        # Center the camera on the sprite
        self.group.center(self.player.pos.get())

        # self.collisions = pytmx.util_pygame.build_rects(self.tmx_data, "map_changes", None, )
        # print(self.collisions)

    def update(self):
        # show the map on screen
        self.group.center(self.player.pos.get())
        # print(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def get_size(self):
        """
        Renvoie la taille de la map en pixel dans un tuple
        """
        return self.map_data.map_size[0] * 16, self.map_data.map_size[1] * 16
