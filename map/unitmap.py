'''
Created on Jun 15, 2015

@author: Joseph Lim
'''
from numpy import array
import pygame

from hex.cell import getMovementRange


class UnitMap(object):

    '''
    Graphic layer for units - implements APP-6 military symbols
    '''

    def renderMap(self):
        """ Renders the hexes into a viewable map

        :Override: Custom rendering method """
        self._renderUnitIcons(self.cells)
        self._renderMovementRange(self.cells[0])

    def _renderMovementRange(self, unitCell):
        cellHexCoords = getMovementRange(unitCell.ordinate, 5)

        for c in movementRangeCells:
            self.renderHighlightedHex(
                c, border=2, colour=(255, 255, 0), freq=10)

    def _renderUnitIcons(self, unitCells):
        xBasis, yBasis = self.context.hex_width, self.context.hex_height
        cx, cy = self.context.display_camera

        for unitCell in filter(self._isCellVisible, unitCells):
            icon = self._renderUnitIcon(unitCell)
            x, y = unitCell.cartesianOrdinate

            # Blit at top left corner of the hexagon
            xdest = xBasis * (x - cx - 0.5) + self.context.display_border
            ydest = yBasis * (y - cy - 0.5) + self.context.display_border
            self.context.view_main.blit(icon,
                                        dest=(xdest, ydest),
                                        area=((0, 0), (xBasis, yBasis))
                                        )

    def _renderUnitIcon(self, unitCell):
        """ Renders the unit icon from the given unit Cell. Caches the rendered
        surface in the unitCell. The cached surface is used for blitting back
        onto the main map screen

        :param: unitCell: UnitCell:
            HexCell object containing a fighting unit """
        # If nothing has change, do not re-render, just retrieve cached icon
        if not unitCell.reRender and getattr(unitCell, 'icon', None):
            return unitCell.icon
        unitCell.reRender = False

        # Scaling
        xBasis = self.context.hex_width
        yBasis = self.context.hex_height

        # IFF colours (Self blue, enemy red)
        if unitCell.owner == self.context.turn_player_index:
            colour = (0, 0, 255)
        else:
            colour = (255, 0, 0)

        icon = pygame.Surface(
            (yBasis, xBasis),
            flags=pygame.HWSURFACE | pygame.SRCALPHA)

        # NATO standard icon
        self._artStandardFrame(xBasis, yBasis, icon, colour)
        unit = unitCell.unit

        # NATO icon data:
        if len(unit._internalSubUnits) == 0:
            self._artSquad(xBasis, yBasis, icon, colour)
        elif len(unit.internalCriticals) <= 12:
            self._artSection(xBasis, yBasis, icon, colour)
        elif len(unit.internalCriticals) <= 50:
            self._artPlatoon(xBasis, yBasis, icon, colour)
        else:
            self._artHQ(xBasis, yBasis, icon, colour)

        self._artName(xBasis, yBasis, icon, colour, unit.name)
        self._artManpower(
            xBasis, yBasis, icon, colour, len(unit.internalCriticals),
            unit.softDefense, unit.softDefenseMax)

        # NATO icon unit type:
        for iconFlag in unitCell.iconFlags:
            renderingFunction = getattr(
                self, '_art{0}'.format(iconFlag), lambda *args: None)
            points = renderingFunction(xBasis, yBasis, icon, colour)

            if points:
                pygame.draw.lines(icon,
                                  colour,
                                  True,
                                  points,
                                  2
                                  )

        unitCell.icon = icon
        return icon

###################################################################
# APP-6 NATO unit types
# Placement within frame
###################################################################

    def _artStandardFrame(self, xBasis, yBasis, surface, colour):
        # Standard NATO Rectangle frame 0.6 wide by 0.4 high
        points = [(xBasis * 0.8,  yBasis * 0.3),
                  (xBasis * 0.8, yBasis * 0.7),
                  (xBasis * 0.2,  yBasis * 0.7),
                  (xBasis * 0.2,  yBasis * 0.3),
                  ]
        pygame.draw.lines(surface,
                          colour,
                          True,
                          points,
                          2
                          )

    def _artArmour(self, xBasis, yBasis, surface, colour):
        """ Graphics - APP-6 Armour """
        rect = [(xBasis * 0.3, yBasis * 0.4),
                (xBasis * 0.4, yBasis * 0.2)
                ]
        pygame.draw.ellipse(surface, colour, rect, 2)

    def _artAntiAir(self, xBasis, yBasis, surface, colour):
        """ Graphics - APP-6 Anti air """
        rect = [(xBasis * 0.2,  yBasis * 0.6),
                (xBasis * 0.6,  yBasis * 0.2),
                ]
        pygame.draw.ellipse(surface, colour, rect, 2)

    def _artAntiTank(self, xBasis, yBasis, *args, **kwargs):
        """ Graphics - APP-6 Anti tank """
        points = [(xBasis * 0.2,  yBasis * 0.7),
                  (xBasis * 0.5,  yBasis * 0.3),
                  (xBasis * 0.8,  yBasis * 0.7),
                  ]
        return points

    def _artArtillery(self, xBasis, yBasis, surface, colour):
        """ Graphics - APP-6 Artillery """
        position = [round(xBasis * 0.5),  round(yBasis * 0.5)]
        pygame.draw.circle(surface, colour, position, 5, 0)

    def _artInfantry(self, xBasis, yBasis, *args, **kwargs):
        """ Graphics - APP-6 Infantry """
        points = [(xBasis * 0.8,  yBasis * 0.3),
                  (xBasis * 0.2,  yBasis * 0.7),
                  (xBasis * 0.2,  yBasis * 0.3),
                  (xBasis * 0.8, yBasis * 0.7)
                  ]
        return points

    def _artMedical(self, xBasis, yBasis, *args, **kwargs):
        """ Graphics - APP-6 Medical """
        points = [(xBasis * 0.2,  yBasis * 0.5),
                  (xBasis * 0.8,  yBasis * 0.5),
                  (xBasis * 0.8,  yBasis * 0.3),
                  (xBasis * 0.5, yBasis * 0.3),
                  (xBasis * 0.5, yBasis * 0.7),
                  (xBasis * 0.2, yBasis * 0.7),
                  ]
        return points

    def _artRecon(self, xBasis, yBasis, *args, **kwargs):
        """ Graphics - APP-6 Recce """
        points = [(xBasis * 0.2,  yBasis * 0.3),
                  (xBasis * 0.8,  yBasis * 0.7),
                  ]
        return points


###################################################################
# APP-6 NATO unit strengths
# Placement at top of frame
###################################################################
    def _artSquad(self, xBasis, yBasis, surface, colour):
        self.font.render_to(surface,
                            dest=(xBasis * 0.48, yBasis * 0.2),
                            text='.',
                            fgcolor=colour,
                            size=xBasis * 0.3)

    def _artSection(self, xBasis, yBasis, surface, colour):
        self.font.render_to(surface,
                            dest=(xBasis * 0.45, yBasis * 0.2),
                            text='..',
                            fgcolor=colour,
                            size=xBasis * 0.3)

    def _artPlatoon(self, xBasis, yBasis, surface, colour):
        self.font.render_to(surface,
                            dest=(xBasis * 0.4, yBasis * 0.2),
                            text='...',
                            fgcolor=colour,
                            size=xBasis * 0.3)

    def _artHQ(self, xBasis, yBasis, surface, colour):
        self.font.render_to(surface,
                            dest=(xBasis * 0.4, yBasis * 0.15),
                            text='HQ',
                            fgcolor=colour,
                            size=xBasis * 0.1)

###################################################################
# APP-6 NATO unit information
# Placement around frame
###################################################################
    def _artName(self, xBasis, yBasis, surface, colour, name=''):
        self.font.render_to(surface,
                            dest=(xBasis * 0.85, yBasis * 0.3),
                            text=name,
                            fgcolor=colour,
                            rotation=270,
                            size=yBasis * 0.15)

    def _artManpower(self, xBasis, yBasis, surface, colour, men,
                     softDefense, softDefenseMax):
        caption = '{0}    {1}/{2}'.format(men, softDefense, softDefenseMax)

        self.font.render_to(surface,
                            dest=(xBasis * 0.2, yBasis * 0.75),
                            text=caption,
                            fgcolor=colour,
                            size=xBasis * 0.1)
