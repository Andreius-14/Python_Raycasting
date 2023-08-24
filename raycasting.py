import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):

        """ Variables """
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1

        # Position: Personaje 
        ox, oy = self.game.player.pos
        # Position: Grid Enteros
        x_map, y_map = self.game.player.map_pos

        # Angulo entre Rayos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        # Bucle - N° de Rayos 
        for ray in range(NUM_RAYS):
            # Largo C.O
            sin_a = math.sin(ray_angle)
            # Largo C.A
            cos_a = math.cos(ray_angle)

            """ GRID: horizontals - Hallar X - Facil Y """

            # [y_hor: dy primera Interseccion], [dy: Distancia dy General]
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            # Distancia - Hipotenusa Firts
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            # Distancia - Hipotenusa General
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth



            """ GRID: verticals - Hallar Y - Facil X """
            
            # [x_vert: dx primera Interseccion], [dx: Distancia dx General]
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            # Distancia - Hipotenusa Firts
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            
            # Distancia - Hipotenusa General
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # 📉📉📉 depth, texture offset
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor


            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Draw wall
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            pg.draw.rect(self.game.screen, color
                         , (ray * SCALE, HALF_HEIGHT - proj_height // 2 , SCALE , proj_height))


            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
