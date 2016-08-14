'''
Created on Jun 2, 2015

@author: Joseph Lim
'''

import sys

from numpy import array
import pygame
import pygame.freetype
from pygame.locals import *

from engine.constants import GameContext
from map.camera import Camera
from map.hexmap import HexMap
from map.infomap import InfoMap
from map.terrain import randomTerrain, RandomMap
from map.unitmap import UnitMap


class GameEngine(object):

    def __init__(self):
        pygame.init()

        #######################################################################
        #    Initialisation
        #######################################################################

        # Game constants
        self.standardText = pygame.font.SysFont('monospace', 20)
        self.context = GameContext()
        self.camera = Camera(self.context)
        self.fps = 120
        self.fpsClock = pygame.time.Clock()

        # Initial values
        self.selectedHex = None
        self.debugLabel = self.standardText.render(
            "DEBUG", True, (128, 196, 196))

        # Random map
        randomMap = RandomMap(40, 40).getMap()

        # Test unit
        from units.basetypes import UnitCell
        from units.infantryunits import getNATOReservePlatoon
        from units.infantrytypes import NATOReservist
        from units.smallarms import RifleNATOBasic
        platoon1 = getNATOReservePlatoon(
            NATOReservist, RifleNATOBasic, name='A1')
        unit1 = UnitCell(
            platoon1, 1, (0, -5, 5), iconFlags=['Infantry', 'Armour'])
        unit2 = UnitCell(
            platoon1, 2, (-1, -4, 5), iconFlags=['Infantry', 'Armour'])

        # Game window - warning: affected by Windows DPI scaling
        pygame.display.set_caption('PyGame: TBS')
        view = pygame.display.set_mode(
            (self.context.display_width, self.context.display_height),
            pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN, 32)
        view.fill((255, 255, 255))
        self.context.view_main = view

        # Map window layers (terrain/highlights<objectives<units)
        self.context.view_terrain = HexMap(
            self.context, randomMap, renderWholeMap=True)
        self.context.view_ui = InfoMap(self.context)
        self.context.view_units = UnitMap(self.context, [unit1, unit2])
        #self.unitMap.canvas = self.context.view_main

    def run(self):
        #######################################################################
        #    Main Loop
        #######################################################################
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse motion events
                elif event.type == pygame.MOUSEMOTION:
                    self.debugHandler(event)
                    self.scrollingHandler(event)
                    self.context.view_ui.getSelectedObject(event.pos)

                # Mouse motion left click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.context.view_terrain.getSelectedHex(event.pos)
                    self.context.view_units.getSelectedHex(event.pos)

            # Rendering calls
            self.context.view_main.fill((255, 255, 255))
            self.camera.updateCamera()
            self.context.view_terrain.renderMap()
            self.context.view_ui.renderMap(
                self.context.view_terrain.selectedCell)
            self.context.view_units.renderMap()

            # self.context.view_main.blit(
            # self.unitMap.canvas,
            # self.context.display_map_rect)
            self.context.view_main.blit(self.debugLabel, (100, 100))
            pygame.display.flip()

            # Internal clock
            tick = self.fpsClock.tick(self.fps)
            self.context.clock_tick = tick
            self.context.clock_elapsed += tick

    def debugHandler(self, event):
        """ Used to insert a debug string as an overlay """
        self.debugLabel = self.standardText.render(
            "Cursor: {0}p, Camera:{1}, FPS:{2} Selected: {3} - {4}.".format(
                event.pos,
                self.context.display_camera,
                self.fpsClock.get_fps(),
                getattr(
                    self.context.view_terrain.selectedCell, 'terrain_name', None),
                getattr(self.context.view_units.selectedCell, 'unit', None)),
            True, (255, 255, 255))

    def scrollingHandler(self, event):
        """ Camera handling logic - scrolls the map when the mouse is near a boundary.
        Scroll rate increases linearly as mouse approaches the window edge """
        x, y = event.pos
        if x < self.context.display_border:
            self.camera.scroll_x = -1 * abs(self.context.display_border - x)
        elif x > self.context.display_width - self.context.display_border:
            self.camera.scroll_x = abs(
                x - self.context.display_width + self.context.display_border)
        else:
            self.camera.scroll_x = 0

        if y < self.context.display_border:
            self.camera.scroll_y = -1 * abs(self.context.display_border - y)
        elif y > self.context.display_height - self.context.display_border:
            self.camera.scroll_y = abs(
                y - self.context.display_height + self.context.display_border)
        else:
            self.camera.scroll_y = 0


if __name__ == '__main__':
    game = GameEngine()
    game.run()
