'''
Created on Jun 2, 2015

@author: Joseph Lim
'''

from copy import copy
from numpy import array
import pygame
import pygame.freetype
from map.hexgrid import HexCell


class HexMap(object):

    """ HexMap the view controller """

    def __init__(self, context, cells, renderWholeMap=False):
        self.context = context
        self.cells = cells
        self.calculationCell = HexCell()
        self.selectedCell = None
        self.font = pygame.freetype.Font(None)
        self.renderWholeMap = renderWholeMap
        self.images = {}

        if self.renderWholeMap:
            cx, cy = context.display_camera_bounds
            self.canvas = pygame.Surface((
                cx * context.hex_width + context.display_map_width,
                cy * context.hex_height + context.display_map_height),
                pygame.HWSURFACE,
                32)
        else:
            self.canvas = pygame.Surface((
                self.context.display_map_width,
                self.context.display_map_height),
                pygame.HWSURFACE,
                32)

    def _isCellVisible(self, cell):
        """ If rendering only visible area - use this to determine cells """
        x, y = cell.cartesianOrdinate
        xBasis, yBasis = self.context.hex_width, self.context.hex_height
        cx, cy = self.context.display_camera
        px = (x - cx) * xBasis
        py = (y - cy) * yBasis

        return (px > 0 - xBasis and
                py > 0 - yBasis and
                px < self.context.display_map_width + xBasis and
                py < self.context.display_map_height + yBasis
                )

    def renderMap(self, updateCellsTo=None):
        """ Renders the hexes into a viewable map """
        if updateCellsTo:
            self.cells = updateCellsTo
            self.images['map'] = None

        if self.renderWholeMap:
            self._renderMapStatic()
        else:
            self._renderMapDynamic()

        self.renderHighlightedHex(self.selectedCell, border=3)

    def _renderMapStatic(self):
        """ Render entire map, cache it - blit only visible area """
        if not self.images.get('map'):
            self.canvas.fill((0, 0, 0))
            _renderedCells = [
                self.renderTerrainHex(cell) for cell in self.cells]
            self.images['map'] = self.canvas

        cx, cy = self.context.display_camera
        xBasis, yBasis = self.context.hex_width, self.context.hex_height
        visibleRect = pygame.Rect((cx * xBasis, cy * yBasis),
                                  (self.context.display_map_width,
                                   self.context.display_map_height))
        self.context.view_main.blit(
            self.images['map'],
            self.context.display_map_rect,
            area=visibleRect)

    def _renderMapDynamic(self):
        """ Render only cells in visible area - blit area into view """
        self.canvas.fill((0, 0, 0))
        _renderedCells = [self.renderTerrainHex(
            cell) for cell in self.cells if self._isCellVisible(cell)]
        self.context.view_main.blit(
            self.canvas,
            self.context.display_map_rect)

    def getCursorPosition(self, cursorPosition):
        """ Returns the cube coordinates of the hex object under the cursor """
        # Convert from pixels -> Map's cartesian x,y -> Map's hex vector -> Hex
        # centre
        xPixels = cursorPosition[0]
        yPixels = cursorPosition[1]
        x = (xPixels - self.context.display_border) / self.context.hex_width
        y = (yPixels - self.context.display_border) / self.context.hex_height

        self.calculationCell.cartesianOrdinate = array([x, y])
        hexagonalCoords = copy(self.calculationCell.ordinate)

        self.calculationCell.cartesianOrdinate = self.context.display_camera
        cameraHexagonalCoords = copy(self.calculationCell.ordinate)

        return self.calculationCell.round(
            hexagonalCoords, cameraHexagonalCoords)

    def getSelectedHex(self, cursorPosition):
        """ Returns the hex object under the cursor """
        # Can only select objects within the map screen area
        x, y = cursorPosition
        rect = pygame.Rect(
            (self.context.display_border, self.context.display_border),
            (self.context.display_map_width, self.context.display_map_height))
        if not rect.collidepoint(x, y):
            return

        # Retrieve the selected cell
        cells = self.cells
        ordinate = self.getCursorPosition(cursorPosition)
        selected = [
            cell for cell in cells if (cell.ordinate == ordinate)]
        assert len(selected) < 2, 'Algo Error: multiple cells selected'
        self.selectedCell = selected[0] if selected else None
        return self.selectedCell

    def _getHexVertices(self, cartesianOrdinate, cartesianOffset=(0, 0)):
        xBasis = self.context.hex_width
        yBasis = self.context.hex_height
        x = (cartesianOrdinate[0] - cartesianOffset[0]) * xBasis
        y = (cartesianOrdinate[1] - cartesianOffset[1]) * yBasis

        # Calculate the 6 points of the hex polygon. List indexing is slower
        # than local ref
        top = (x, y + yBasis / 2)
        bottom = (x, y - yBasis / 2)
        leftTop = (x - xBasis / 2, y + yBasis / 4)
        leftBottom = (x - xBasis / 2, y - yBasis / 4)
        rightTop = (x + xBasis / 2, y + yBasis / 4)
        rightBottom = (x + xBasis / 2, y - yBasis / 4)

        return (top, rightTop, rightBottom, bottom, leftBottom, leftTop)

    def renderTerrainHex(self, cell):
        """ Draws a terrain hex onto the map """
        if self.renderWholeMap:
            points = self._getHexVertices(
                cell.cartesianOrdinate,
            )
        else:  # Positioned dynamically
            points = self._getHexVertices(
                cell.cartesianOrdinate,
                cartesianOffset=self.context.display_camera
            )

        # Render fill - about 10fps
        pygame.draw.polygon(
            self.canvas,
            cell.hex_colour_internal or self.context.hex_colour_internal,
            points
        )

        pygame.draw.lines(self.canvas,
                          (196, 196, 196),
                          True,
                          points,
                          2
                          )

    def renderHighlightedHex(self, cell, border=1, colour=None, freq=2):
        """ Highlights the currently selected hex """
        if not cell:
            return
        if not self._isCellVisible(cell):
            return

        # Animation:
        animationCycle = 1000
        currentCycle = self.context.clock_elapsed % animationCycle
        if currentCycle < animationCycle / freq:
            return
        else:
            self._renderHighlightedHex(cell, border, colour)

    def _renderHighlightedHex(self, cell, border, colour):
        # Cache highlight image
        if not self.images.get('highlight'):
            highlight = pygame.Surface(
                (self.context.hex_height + border * 2,
                 self.context.hex_width + border * 2),
                flags=pygame.HWSURFACE | pygame.SRCALPHA)

            pygame.draw.lines(highlight,
                              colour or self.context.hex_colour_selection_border,
                              True,
                              self._getHexVertices(array([0.5, 0.5])),
                              border
                              )
            self.images['highlight'] = highlight

        # Add image to canvas
        x, y = cell.cartesianOrdinate
        cx, cy = self.context.display_camera
        bx, by = self.context.hex_width, self.context.hex_height

        xdest = bx * (x - cx - 0.5) + self.context.display_border
        ydest = by * (y - cy - 0.5) + self.context.display_border

        self.context.view_main.blit(self.images['highlight'],
                                    dest=(xdest, ydest),
                                    )
