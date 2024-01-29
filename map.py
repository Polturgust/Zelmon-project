import pygame
import pytmx
import pyscroll

from screen import Screen


class Map:
    def __init__(self, screen,player):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player=player

        # switch to map0
        self.switch_map("city0(spawn)")
        self.check_collide()

    def switch_map(self, map):
        # load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\{map}.tmx")
        # get the map for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        # render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        print(self.tmx_data.objects_by_name)

        self.collisions=pytmx.util_pygame.build_rects(self.tmx_data,"map_changes",None,)
        print(self.collisions)
    def update(self):
        # show the map on screen
        self.group.draw(self.screen.get_display())

    def check_collide(self):
        """
        for i in self.tmx_data.objects:
            if self.player.rect.colliderect(i.get_rect()):
                print("Lul")
        """
