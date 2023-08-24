from settings import *
import pygame as pg
import math

"""
Todo Esto es sobre el Jugador Incluso su vision del Mundo
"""

class Player:
    def __init__(self, game):
        self.game = game

        # settings
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        # Variables
        self.shot = False
        self.rel = 0
        self.health_recovery_delay = 700
        # Funciones
        self.time_prev = pg.time.get_ticks()
        self.diag_move_corr = 1 / math.sqrt(2)         # diagonal movement correction

    # 🔃 In Update - La Vida
    def recover_health(self):
        """ Aumenta Vida """
        # Que Tiempo Transcurrido sea TRUE && La Salud no ha llegado al Maximo 
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        """ Determina Tiempo Transcurrido """
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
    
    def check_game_over(self):
        """ TRUE: Pantalla de Muerte y Reinicio """
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    # # Daño
    # def get_damage(self, damage):
    #     """ OUT - lo Ejecutan factores Externos"""
    #     self.health -= damage
    #     self.game.object_renderer.player_damage()
    #     # self.game.sound.player_pain.play()
    #     self.check_game_over()
    # # Daño - Sonido
    # def single_fire_event(self, event):
    #     """ OUT - lo Ejecutan factores Externos"""
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         if event.button == 1 and not self.shot and not self.game.weapon.reloading:
    #             # self.game.sound.shotgun.play()
    #             self.shot = True
    #             self.game.weapon.reloading = True

    # 🔃 In Update
    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
 
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        """ Checar Colision """
        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        # Reestablece Radianes al Superar su Limite
        self.angle %= math.tau

    """ COLISIONES """
    # Funcion Extra - Reutilizable
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    # Funcion Principal
    # Condicional - Movimiento del Personaje . Colision de Pareres
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    """ 2D Personaje - Draw"""
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    # 🔃 In Update
    """ MOUSE - Determina Angulo del Personaje"""
    def mouse_control(self):
        # Posicion del Mouse
        mx, my = pg.mouse.get_pos()
        # Precindible - Te saliste te devuelve al centro
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        # Tupla - x,y - solo x - Cuanto se desplazo con respecto a su ubicacion Anterior
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    # 🔃 Funcion Update
    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
