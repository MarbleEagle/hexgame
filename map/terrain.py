'''
Created on Jun 2, 2015

@author: Joseph Lim
'''

import math
import random
from numpy import array
from map.hexgrid import HexCell


class RandomMap(object):

    def __init__(self, width, height, config=None):
        self.width = width
        self.height = height
        self.terrainMap = {}
        defaultConfig = {
            'woods': 10,
            'hills': 30,
            'urban': 200,
            'water': 150,
            'jungle': 10000,
            'mountains': 10000, }
        self.config = config or defaultConfig

    def getMap(self):
        # Fill the map with plains. Each hex row is 0.5y offset.
        for z in range(0, self.height):
            for x in range(math.ceil(-z / 2), math.ceil(self.width - z / 2)):
                y = - x - z
                self.terrainMap[x, y, z] = Plains

        # Randomise vegetation
        forestCount = round(len(self.terrainMap) / self.config['woods'])
        jungleCount = round(len(self.terrainMap) / self.config['jungle'])

        for _i in range(0, forestCount):
            if random.random() < 0.5:
                self._seedCluster(2, Woods)
            elif random.random() < 0.75:
                self._seedCluster(3, Woods)
            else:
                self._seedCluster(3, Forest)

        for _i in range(0, jungleCount):
            if random.random() < 0.25:
                self._seedCluster(3, Jungle)
            elif random.random() < 0.5:
                self._seedCluster(2, Marsh)
            else:
                self._seedCluster(5, Jungle)

        # Randomise hills/mountains
        forestCount = round(len(self.terrainMap) / self.config['hills'])
        mountainCount = round(len(self.terrainMap) / self.config['mountains'])

        for _i in range(0, forestCount):
            if random.random() < 0.5:
                self._seedCluster(1, Hills)
            elif random.random() < 0.75:
                self._seedCluster(2, Hills)
            else:
                self._seedCluster(1, Mountains)

        for _i in range(0, mountainCount):
            if random.random() < 0.25:
                self._seedCluster(3, Hills)
            elif random.random() < 0.5:
                self._seedCluster(2, Mountains)
            else:
                self._seedCluster(3, Mountains)

        # Randomise villages/urban sprawl
        cityCount = round(len(self.terrainMap) / self.config['urban'])
        cityNodes = []
        for _i in range(0, cityCount):
            if random.random() < 0.25:
                self._seedCluster(1, Urban, cityNodes)
            elif random.random() < 0.75:
                self._seedCluster(2, Urban, cityNodes)
            elif random.random() < 0.95:
                self._seedCluster(3, Urban, cityNodes)
            else:
                self._seedCluster(4, Urban, cityNodes)

        # Pick random river nodes
        riverCrossingsCount = round(
            len(self.terrainMap) / self.config['water'])
        riverNodes = []
        for _i in range(0, riverCrossingsCount):
            if random.random() < 0.7:
                self._seedCluster(1, River, riverNodes)
            elif random.random() < 0.85:
                self._seedCluster(2, Marsh, riverNodes)
            else:
                self._seedCluster(5, Ocean, riverNodes)

        # Create rivers, roads between cities
        self._joinNodes(riverNodes, Ocean, Ocean)
        self._joinNodes(cityNodes, Road, Urban)

        terrainMap = []
        for k, v in self.terrainMap.items():
            cell = v(k)
            terrainMap.append(cell)

        return terrainMap

    def _seedCluster(self, size, terrainClass, nodeLog=None):
        """ Create a cluster of size """
        z = random.randint(0, self.height)
        x = random.randint(math.ceil(- z / 2), math.ceil(self.width - z / 2))
        y = -x - z

        origin = terrainClass(array([x, y, z]))
        ordinates = [origin.ordinate]

        for i in range(0, size):
            ordinates += origin.getNeighbours(origin.ordinate, i)
        ordinates = set((o[0], o[1], o[2]) for o in ordinates)

        for o in ordinates:
            if random.random() < 0.10 and terrainClass == Urban:
                self.terrainMap[o] = Fortified
            elif random.random() < 0.25 and terrainClass == Woods:
                self.terrainMap[o] = Forest
            elif random.random() < 0.10 and terrainClass == Hills:
                self.terrainMap[o] = Mountains
            else:
                self.terrainMap[o] = terrainClass

        if isinstance(nodeLog, list):
            nodeLog.append(origin.ordinate)

    def _joinNodes(self, nodeLog, terrainClass, doNotReplace=None):
        """ Joins Nodes """
        nodes = [terrainClass(array(node)) for node in nodeLog]

        # Produce a graph with distances on the edges
        pairWiseDistances = {}
        for currentNode in nodes:
            pairWiseDistances[str(currentNode)] = {
                (currentNode.getDistance(currentNode.ordinate, node.ordinate), str(node)): (currentNode, node) for node
                in nodes if currentNode != node}

        # Link every vertex to its nearest unlinked neighbour
        ordinates = []
        linkedNodes = []
        for pairWiseDistance in pairWiseDistances.values():
            for k in sorted(pairWiseDistance):
                if k[1] in linkedNodes:
                    continue
                else:
                    a1, b1 = pairWiseDistance[k]
                    ordinates += a1.getLine(a1.ordinate, b1.ordinate)
                    linkedNodes.append(str(a1))
                    break

        nodesTuples = set(
            (n.ordinate[0], n.ordinate[1], n.ordinate[2]) for n in nodes)
        ordinatesTuples = set((o[0], o[1], o[2]) for o in ordinates)
        ordinates = ordinatesTuples - nodesTuples

        for o in ordinates:
            if self.terrainMap.get(o) != doNotReplace:
                self.terrainMap[o] = terrainClass


def randomTerrain():
    classListWeighted = []
    classListWeighted += [Plains] * 100
    classListWeighted += [Sandy] * 10
    classListWeighted += [Road] * 15
    classListWeighted += [Woods] * 40
    classListWeighted += [Forest] * 20
    classListWeighted += [Jungle] * 10
    classListWeighted += [Hills] * 10
    classListWeighted += [Mountains] * 5
    classListWeighted += [Marsh] * 5
    classListWeighted += [River] * 10
    classListWeighted += [Ocean] * 10
    classListWeighted += [Urban] * 30
    classListWeighted += [Fortified] * 5

    return random.choice(classListWeighted)
    '''return random.choice(
        [Plains, Sandy, Road, Woods, Forest, Jungle, Hills, Mountains, Marsh,
         River, Ocean, Urban, Fortified])'''


class TerrainCell(HexCell):

    """ Represents the terrain. Contains all environmental effects """

    # Meta
    terrain_obstructs = False
    terrain_name = 'Default'
    terrain_icon = None
    hex_colour_border = (0, 0, 0)
    hex_colour_internal = (85, 107, 47)

    # Defense attributes
    defense_cover = 0
    defense_concealment = 0

    # Movement attributes
    passability_foot = 1
    passability_wheel = 1
    passability_track = 1

    def __init__(self, ordinate, **kwargs):
        super(TerrainCell, self).__init__(ordinate)
        for k, v in kwargs.items():
            setattr(self, k, v)


class Plains(TerrainCell):

    terrain_name = 'Plains'
    defense_cover = 0
    defense_concealment = 0
    passability_wheel = 2

    hex_colour_internal = (196, 230, 152)


class Sandy(TerrainCell):

    terrain_name = 'Sand'
    defense_cover = 0
    defense_concealment = 0
    passability_wheel = 2

    hex_colour_internal = (240, 215, 75)


class Road(TerrainCell):

    terrain_name = 'Road'
    defense_cover = -1
    defense_concealment = -1

    hex_colour_internal = (255, 200, 200)


class Woods(TerrainCell):

    terrain_name = 'Woods'
    defense_cover = 1
    defense_concealment = 1
    passability_wheel = 3

    hex_colour_internal = (75, 160, 30)


class Forest(TerrainCell):

    terrain_name = 'Forest'
    defense_cover = 1
    defense_concealment = 2
    passability_wheel = 4
    passability_track = 2

    hex_colour_internal = (50, 90, 24)


class Jungle(TerrainCell):

    terrain_name = 'Jungle'
    defense_cover = 2
    defense_concealment = 2
    passability_wheel = 4
    passability_track = 3
    passability_foot = 2

    hex_colour_internal = (60, 180, 50)


class Hills(TerrainCell):

    terrain_name = 'Hills'
    defense_cover = 1
    defense_concealment = 0
    passability_wheel = 3
    passability_track = 2
    passability_foot = 2

    hex_colour_internal = (100, 100, 100)


class Mountains(TerrainCell):

    terrain_name = 'Mountains'
    defense_cover = 2
    defense_concealment = 0
    passability_wheel = 4
    passability_track = 3
    passability_foot = 1

    hex_colour_internal = (60, 60, 36)


class Marsh(TerrainCell):

    terrain_name = 'Marsh'
    defense_cover = -1
    defense_concealment = 0
    passability_wheel = 3
    passability_track = 2
    passability_foot = 2

    hex_colour_internal = (150, 175, 175)


class River(TerrainCell):

    terrain_name = 'Shallows'
    defense_cover = -2
    defense_concealment = -1
    passability_wheel = 3
    passability_track = 2
    passability_foot = 2

    hex_colour_internal = (34, 154, 240)


class Ocean(TerrainCell):

    terrain_name = 'Deep Water'
    defense_cover = 0
    defense_concealment = 0
    passability_wheel = 10
    passability_track = 10
    passability_foot = 10

    hex_colour_internal = (30, 30, 240)


class Urban(TerrainCell):

    terrain_name = 'Urban'
    defense_cover = 2
    defense_concealment = 2

    hex_colour_internal = (155, 95, 95)


class Fortified(TerrainCell):

    terrain_name = 'Fortified'
    defense_cover = 3
    defense_concealment = 2

    hex_colour_internal = (108, 15, 15)
