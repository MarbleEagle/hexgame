'''
Created on Jun 28, 2015

@author: Joseph Lim
'''

import pygame
from map.hexmap import HexMap


class InfoMap(HexMap):

    """ UI containing panels """

    def __init__(self, context):
        self.context = context

        self.rect = pygame.Rect((self.context.display_map_width +
                                 self.context.display_border,
                                 self.context.display_border),
                                (self.context.display_info_width,
                                 self.context.display_info_height))
        self.canvas = pygame.Surface((
            self.rect.width,
            self.rect.height),
            pygame.HWSURFACE,
            32)

        self.selectedElement = None
        self.elements = []
        self.font = pygame.freetype.Font(None)
        self.font.pad = True
        self.images = {}

        self._setupUIImages()
        self._setupElements()

    def _setupUIImages(self):
        """ Cache all ui image data locally """
        import os
        ui = {}
        resourceDir = os.path.join(
            os.path.dirname(__file__),
            '..', 'sprites', 'ui')

        for file in os.listdir(resourceDir):
            ui[file] = pygame.image.load(os.path.join(resourceDir, file))

        self.images['ui'] = ui

    def _setupElements(self):
        """ Terrain info panel """
        # Terrain name
        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'terrain_name', ''),
            rect=((20, 0), (200, 30)),
        ))

        # Cover and concealment bonuses
        self.elements.append(UIElement(
            self.context,
            image=self.images['ui'].get('icon_terrain_defense.png'),
            tooltip='Terrain defence bonus',
            rect=((20, 40), (30, 30))
        ))

        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'defense_cover', ''),
            tooltip='+ Damage Reduction',
            rect=((60, 40), (40, 30)),
        ))

        self.elements.append(UIElement(
            self.context,
            image=self.images['ui'].get('icon_terrain_camo.png'),
            tooltip='Terrain camouflage bonus',
            rect=((20, 80), (30, 30))
        ))

        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'defense_concealment', ''),
            tooltip='+ Initiative, - Enemy Range',
            rect=((60, 80), (40, 30)),
        ))

        # Terrain movement costs
        self.elements.append(UIElement(
            self.context,
            image=self.images['ui'].get('icon_terrain_camo.png'),
            tooltip='Foot movement cost',
            rect=((120, 40), (30, 30))
        ))

        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'passability_foot', ''),
            tooltip='Movement cost per hex',
            rect=((160, 40), (40, 30)),
        ))

        self.elements.append(UIElement(
            self.context,
            image=self.images['ui'].get('icon_terrain_camo.png'),
            tooltip='Tracked vehicle movement cost',
            rect=((120, 80), (30, 30))
        ))

        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'passability_track', ''),
            tooltip='Movement cost per hex',
            rect=((160, 80), (40, 30)),
        ))

        self.elements.append(UIElement(
            self.context,
            image=self.images['ui'].get('icon_terrain_camo.png'),
            tooltip='Wheeled vehicle movement cost',
            rect=((120, 120), (30, 30))
        ))

        self.elements.append(UITextField(
            self.context,
            getValue=lambda self: getattr(
                self.selectedCell, 'passability_wheel', ''),
            tooltip='Movement cost per hex',
            rect=((160, 120), (40, 30)),
        ))

    def renderMap(self, selectedCell):
        self.canvas.fill((255, 255, 255))

        # Render terrain info panel
        self.selectedCell = selectedCell
        if self.selectedCell:
            for e in self.elements:
                e.render()

        # Render tool-tip if selected and info panel is rendered
        if self.selectedElement and self.selectedCell:
            e = self.selectedElement
            self.font.render_to(self.canvas,
                                dest=(0, e.rect.top + e.rect.height),
                                text=str(e.tooltip or ''),
                                bgcolor=(32, 32, 32),
                                fgcolor=(255, 255, 255),
                                size=16)

        # Render to main screen
        self.context.view_main.blit(
            self.canvas,
            dest=(self.rect.left, self.rect.top),
        )

    def getSelectedObject(self, cursorPosition):
        x, y = cursorPosition
        cx = self.rect.left
        cy = self.rect.top
        cursorPosition = (x - cx, y - cy)

        [self.selectedElement] = [
            e for e in self.elements if e.isSelected(cursorPosition)] or [None]


class UIElement(object):

    image = None
    rect = pygame.Rect((0, 0), (0, 0))
    tooltip = None

    def __init__(self, context, image, tooltip, rect):
        self.context = context
        self.image = image
        self.tooltip = tooltip
        self.rect = pygame.Rect(rect)

    def render(self):
        """ Render this UI element """
        self.image = pygame.transform.smoothscale(
            self.image,
            (self.rect.width, self.rect.height))

        self.context.view_ui.canvas.blit(
            self.image,
            self.rect)

    def isSelected(self, cursorPosition):
        """ Check if the mouse is within this element """
        x, y = cursorPosition
        return self.rect.collidepoint(x, y)


class UITextField(UIElement):

    def __init__(self, context, getValue, rect, tooltip=None):
        self.context = context
        self.tooltip = tooltip
        self.getValue = getValue
        self.rect = pygame.Rect(rect)

    def render(self):
        """ Render this UI element """
        font = self.context.view_ui.font
        canvas = self.context.view_ui.canvas
        value = self.getValue(self.context.view_ui)

        try:
            if float(value) < 0:
                colour = (220, 0, 0)
            else:
                colour = (0, 0, 0)
            value = round(float(value))
        except:
            colour = (0, 0, 0)

        font.render_to(canvas,
                       dest=(self.rect.left, self.rect.top),
                       text=str(value),
                       fgcolor=colour,
                       size=self.rect.height)
