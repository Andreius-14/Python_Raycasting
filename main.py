# Estandar
import pygame as pg
import sys
# Complemento
from settings import *          # Constantes
from map import *
from player import *
from raycasting import *



class Game:

    def __init__(self):
        # Inicia - pygame
        pg.init()
        # Inicia - Basico
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        # propiedades
        pg.mouse.set_visible(False)  # Mouse Invisible
        pg.event.set_grab(True)      # Mouse Evita que se salga de la pantalla
    
    def new_game(self):    
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)

    def update(self):
        # Update - Instancia
        self.player.update()
        self.raycasting.update()
        # Update - Basica
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # Draw - 2D
        self.screen.fill('black')
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    """ Bucle Principal - Se ejecuta Constantemente """
    def run(self):
        while True:
            #Eventos
            self.check_events()
            #Actualiza Data
            self.update()
            #Dibuja
            self.draw()


# El Inicia
if __name__ == '__main__':
    game = Game()
    game.run()
