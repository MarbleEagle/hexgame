'''
Created on Jun 1, 2015

@author: Joseph Lim
'''
from numpy import array


class HexCell(object):

    '''
    This is the basis of a hexagonal grid cell
    '''

    def __init__(self, ordinate=None):
        """ A hexagonal cell centred around the ordinate

        :param 3-vector: from origin to hex centre """
        self.ordinate = ordinate if ordinate is not None else (0, 0, 0)
        self.cache = {}
        self.refreshCache = False

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.ordinate == other.ordinate)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def ordinate(self):
        """ Hexagonal ordinates """
        return tuple(list(self._ordinate))

    @ordinate.setter
    def ordinate(self, ordinate):
        """ Hexagonal ordinates - compute x,y when setting as CPU intensive """
        self._ordinate = array(list(ordinate))

        # Note: |a|cos(theta) = a.x/|x| get distance as a multiple of x,y unit
        xUnitVector = array([1, -1, 0]) / 2  # right by 0.5 hex widths
        yUnitVector = array([-1, -1, 2]) / 4  # down by 0.5 hex heights
        x = self._ordinate.dot(xUnitVector)
        y = self._ordinate.dot(yUnitVector)

        self._ordinateCartesian = (x, y)

    @property
    def cartesianOrdinate(self):
        """ X, Y ordinates from top left """
        return self._ordinateCartesian

    @cartesianOrdinate.setter
    def cartesianOrdinate(self, coordinates):
        """ X, Y ordinates - compute hexagonal ordinates when setting """
        x = coordinates[0]
        y = coordinates[1]
        self._ordinate = (
            x * array([1, -1, 0])) + (y * array([-1, -1, 2]) * 2 / 3)
        self._ordinateCartesian = coordinates

    @classmethod
    def round(cls, vector, offset):
        """ For a given hexagonal ordinate, find the nearest hex
        offset allows for a camera displacement vector """
        x = round(vector[0] + offset[0])
        y = round(vector[1] + offset[1])
        z = round(vector[2] + offset[2])

        x_diff = abs(vector[0] + offset[0] - x)
        y_diff = abs(vector[1] + offset[1] - y)
        z_diff = abs(vector[2] + offset[2] - z)

        if x_diff > y_diff and x_diff > z_diff:
            x = -y - z
        elif y_diff > z_diff:
            y = -x - z
        else:
            z = -x - y

        return (x, y, z)

    @classmethod
    def getDirection(cls, direction):
        """ Vectors for the 6 hexagonal directions. 3=Right. Clockwise """
        basisVectors = {
            0: (-1, 1, 0),
            1: (0, 1, -1),
            2: (1, 0, -1),
            3: (1, -1, 0),
            4: (0, -1, 1),
            5: (-1, 0, 1),
        }
        return basisVectors[direction]

    @classmethod
    def getNeighbours(cls, ordinate, radius):
        """ Returns a ring of all cells at radius from the ordinate """
        ordinate = array(list(ordinate))
        ringPosition = ordinate + array(list(cls.getDirection(4))) * radius
        results = []

        # Clockwise rotation through 6-arcs to from a hexagon
        for arc in range(6):
            for _i in range(radius):
                ringPosition += array(list(cls.getDirection(arc)))
                results.append(ringPosition.copy())

        return results or [tuple(ordinate.tolist())]

    @classmethod
    def getDistance(cls, ordinate1, ordinate2):
        """ Returns the # of hexes away a target cell is. Not abs distance """
        ax, ay, az = ordinate1
        bx, by, bz = ordinate2
        return max(abs(ax - bx), abs(ay - by), abs(az - bz))

    @classmethod
    def getLine(cls, ordinate1, ordinate2):
        """ Returns all cells between cell1 and cell2 """
        ordinate1 = array(list(ordinate1))
        ordinate2 = array(list(ordinate2))
        distance = cls.getDistance(ordinate1, ordinate2)

        if not distance:
            return []

        results = []
        lineVector = (ordinate2 - ordinate1) / distance
        for i in range(0, distance + 1):
            samplingPoint = ordinate1 + lineVector * i
            results.append(cls.round(samplingPoint, (0, 0, 0)))
        return results
