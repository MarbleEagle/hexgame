'''
Created on Jul 4, 2015

@author: Joseph Lim
'''
from map.hexgrid import HexCell


def getMovementRange(origin, movementRange, costDict=None, target=None):
    """ Starting from the origin, find all hexes within the movement range,
    for an infinite plane of cost 1 per hex, and with non-standard costs
    determined by the terrain Dict.

    :origin: 3-tuple:
        Origin in terms of hexagonal ordinates

    :costDict: dict:
        Key, hexagonal ordinate. Value, movement cost (default=1)

    :target: 3-tuple:
        If specified, returns the path and cost to that target  """

    def _recurseDijkstra(origin, nodes, unvisitedNodes, target):
        unvisitedNodes.remove(origin)
        path = []

        # If at the edge of the movement range, return
        if nodes[origin] >= movementRange:
            if origin == target:
                path.append(origin)
            return path

        # Visit all neighbours and update only if nearer
        for neighbour in HexCell.getNeighbours(origin, 1):
            neighbour = tuple(neighbour.tolist())
            if neighbour in unvisitedNodes:
                movementCost = costDict.get(neighbour, 1) + nodes[origin]
                nodes[neighbour] = movementCost if movementCost < nodes[
                    neighbour] else nodes[neighbour]
                path += _recurseDijkstra(neighbour,
                                         nodes, unvisitedNodes, target)
        if path:
            path.append(origin)
        return path

    costDict = costDict or {}
    unvisitedNodes = set()
    for i in range(movementRange + 1):
        unvisitedNodes.update((i, j, k)
                              for i, j, k in HexCell.getNeighbours(origin, i))

    nodes = {node: 1000 for node in unvisitedNodes}  # Should be infinite
    nodes[origin] = 0
    path = _recurseDijkstra(origin, nodes, unvisitedNodes, target)
    path = path[::-1]

    if target:
        return {nodes[target]: path}
    else:
        return {k: v for k, v in nodes.items() if v <= movementRange}


def getVisionRange(origin, linearRange, costDict=None):
    """ Starting from the origin, find all hexes within the line of sight,
    for an infinite plane of cost 1 per hex, and with non-standard costs
    determined by the dict.

    :origin: 3-tuple:
        Origin in terms of hexagonal ordinates

    :costDict: dict:
        Key, hexagonal ordinate. Value, movement cost (default=1) """

    costDict = costDict or {}
    nodes = {}
    unvisitedNodes = set()
    for i in range(1, linearRange + 1):
        unvisitedNodes.update((i, j, k)
                              for i, j, k in HexCell.getNeighbours(origin, i))

    for node in unvisitedNodes:
        if HexCell.getDistance(origin, node) > linearRange:
            continue

        visionPathCells = HexCell.getLine(origin, node)
        visionCost = sum(costDict.get((i, j, k), 1)
                         for i, j, k in visionPathCells) - 1
        if visionCost > linearRange:
            continue

        nodes[node] = visionCost

    return {k: v for k, v in nodes.items()}
