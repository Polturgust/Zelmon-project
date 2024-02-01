import pygame
import pytmx
import pyscroll
from collisions import Collisions
from vector import Vector


class Map:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.map_data = None
        self.zonearr = None
        self.changes = None
        self.collisions = None

        # switch to map0
        self.switch_map("city1")

    def switch_map(self, map):
        # load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\{map}.tmx")
        # get the map for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        # render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size(), zoom=2)
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)
        self.map_layer._x_offset = 240

        self.group.add(self.player)

        # print(self.tmx_data.objects)
        self.collisions = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)
        self.changes = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)

        print("Current location : ",self.zonearr)
        for i in self.tmx_data.visible_layers:

            if isinstance(i, pytmx.TiledObjectGroup):
                for j in i:
                    if i.name == "collisions":
                        self.collisions.add(Collisions(j.width, j.height, j.x, j.y, ""))

                    if i.name == "map_changes":
                        #print(j.name)
                        if j.name != None and "to_route" in j.name:
                            dest = j.name.split("to_route")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "route" + dest[1]))
                        elif j.name != None and "to_city" in j.name:
                            dest=j.name.split("to_city")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "city" + dest[1]))

                    if i.name == "spawn_points":
                        print(self.zonearr, j.name)
                        if self.zonearr != None and self.zonearr in j.name:
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("S")
                            self.player.move("N")
                            print("Changed zone yay")
                        elif self.zonearr == None and j.name == "default_spawn":
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("S")
                            self.player.move("N")
                            print("Default location loaded")

        self.zonearr = map
        self.changes.center(self.player.pos.get())
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
