# -*- coding: utf-8 -*-

"""
Module containing functions for routing
"""

__author__ = "Nikolaos Kostakis"
__copyright__ = "Copyright (c) 2024 Nikolaos Kostakis"
__license__ = "MIT License"
__version__ = "1.0"

import logging

import numpy as np

import config
from structures.design_components import Design, IOPort, Component, Net, Pin
from structures.design_components import NetPoint, NetTreeNode
from structures.design_components import get_center_coordinates

# Logging
routingLogger = logging.getLogger(__name__)
routingLogger.setLevel(logging.DEBUG)
routingLogger.addHandler(config.consoleHandler)
routingLogger.addHandler(config.logfileHandler)

def maze_routing_net(
    net:Net, design: Design,
    startRoutingFromCenter:bool = False,
    clockwiseRouting:bool = True
) -> None:
    """
    Routing algorithm based on Lee's Maze Routing for a single net
    """

    def _propagate_wave_phase() -> None:
        """
        First phase of the maze routing algorithm.

        Propagates wave from the source (existing net)
        """

        def _propagate_to_direction(direction: tuple[int, int]) -> None:
            """
            Propagates (if possible) the wave to the given direction
            """
            if (
                (direction != drain)
                & (direction not in activeList)
                & (direction not in visitedList)
                & (design.blockages[direction] == 0)
            ):
                activeList.append(direction)
                tempBinsArray[direction] = tempBinsArray[activeBin] + 1
        # End of inner function
        
        activeList:list[tuple[int,int]] = []
        visitedList:list[tuple[int,int]] = []

        activeList.extend(netBins)

        while (len(activeList) != 0):
            activeBin = activeList.pop(0)

            #NESW movement is chosen
            # North
            if (activeBin[0] != 0):
                north = ((activeBin[0] - 1), activeBin[1])
                _propagate_to_direction(north)
            # End if North
            # East
            if ((activeBin[1] + 1) != size[1]):
                east = (activeBin[0], (activeBin[1] + 1))
                _propagate_to_direction(east)
            # End if East
            # South
            if ((activeBin[0] +1) != size[0]):
                south = ((activeBin[0] + 1), activeBin[1])
                _propagate_to_direction(south)
            # End if South
            # West
            if (activeBin[1] != 0):
                west = (activeBin[0], (activeBin[1] - 1))
                _propagate_to_direction(west)
            # End if West
           
            visitedList.append(activeBin)
        # End of while
    # End of function

    def _backtracking_phase():
        """
        Second phase of the maze routing algorithm.

        Backtracking from the destination to the source.
        """
        def _check_backtrack_to_direction(direction: tuple[int, int]) -> bool:

            return (tempBinsArray[direction] < value) & (direction != drain) \
                    & (design.blockages[direction] == 0)
        # End of inner function

        backtrackingRoute = []
        nextBin: tuple[int, int] = None
        newDirection: str = None

        activeBin = drain
        direction = None
        value = size[0] + size[1]
        while True:
            if (activeBin in netBins):
                break

            if clockwiseRouting:
                #NESW
                # North
                if (activeBin[0] != 0):
                    north = ((activeBin[0] - 1), activeBin[1])
                    if _check_backtrack_to_direction(north):
                        nextBin = north
                        newDirection = "NORTH"
                        value = tempBinsArray[north]
                # End if North
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if _check_backtrack_to_direction(east):
                        nextBin = east
                        newDirection = "EAST"
                        value = tempBinsArray[east]
                # End if East
                # South
                if ((activeBin[0] + 1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if _check_backtrack_to_direction(south):
                        nextBin = south
                        newDirection = "SOUTH"
                        value = tempBinsArray[south]
                # End if South
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if _check_backtrack_to_direction(west):
                        nextBin = west
                        newDirection = "WEST"
                        value = tempBinsArray[west]
                # End if West
            # End if statement for clockwise
            else:
                #NWSE
                # North
                if (activeBin[0] != 0):
                    north = ((activeBin[0] - 1), activeBin[1])
                    if _check_backtrack_to_direction(north):
                        nextBin = north
                        newDirection = "NORTH"
                        value = tempBinsArray[north]
                # End if North
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if _check_backtrack_to_direction(west):
                        nextBin = west
                        newDirection = "WEST"
                        value = tempBinsArray[west]
                # End if West
                # South
                if ((activeBin[0] + 1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if _check_backtrack_to_direction(south):
                        nextBin = south
                        newDirection = "SOUTH"
                        value = tempBinsArray[south]
                # End if South
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if _check_backtrack_to_direction(east):
                        nextBin = east
                        newDirection = "EAST"
                        value = tempBinsArray[east]
                # End if East
            # End else for counterclockwise
            if ((direction != None) & (direction != newDirection)):
                binsQueue.insert(0, activeBin)

            backtrackingRoute.append(activeBin)
            activeBin = nextBin

            direction = newDirection
        # End of while

        netBins.extend(backtrackingRoute)
        return activeBin
    # End of function

    def _connection_phase() -> None:
        """
        Third phase of maze routing
        """

        def _distance_netNodes_sqrd(point:(IOPort|Component|NetPoint)) -> float:
            """
            Returns the distance squared between the endpoint an a given point
            """
            dist = (ex - point.x)**2 + (ey - point.y)**2
            return dist
        # End of inner function

        def _rearrange_tree(node: NetTreeNode, newNode: NetTreeNode) -> None:
            """
            Determines if the new node is a child or a new parent to the old
            """
            nx,ny = get_center_coordinates(node.point)
            nnx,nny = get_center_coordinates(newNode.point)

            parentNode: NetTreeNode = node.parent
            if (parentNode is not None):
                px,py = get_center_coordinates(parentNode.point)
                if (
                    ((nx == nnx) & (nx == px)
                        & (((py > ny) & (nny > ny)) | ((py < ny) & (nny < ny))))
                    | ((ny == nny) & (ny == py)
                        & (((px > nx) & (nnx > nx)) | ((px < nx) & (nnx < nx))))
                ):
                    parentNode.remove_child(node)
                    parentNode.add_child(newNode)
                    newNode.add_child(node)
                    return
            # End if parent
            for child in node.children:
                cx,cy= get_center_coordinates(child.point)
                if (
                    ((nx == nnx) & (nx == cx)
                        & (((cy > ny) & (nny > ny)) | ((cy < ny) & (nny < ny))))
                    | ((ny == nny) & (ny == cy)
                        & (((cx > nx) & (nnx > nx)) | ((cx < nx) & (nnx < nx))))
                ):
                    node.remove_child(child)
                    node.add_child(newNode)
                    newNode.add_child(child)
                    return
            # End for
            node.add_child(newNode)
        # End of inner function

        def no_corners():
            """
            Connects the drain to the existing tree without any intermediate 
            point/corner from backtracking
            """
            
            def _add_intermediate_node(
                    point:NetTreeNode
                ) -> None:
                """
                Adds if needed a new point between endpoint and existing point
                """

                nonlocal pointNum

                px, py = get_center_coordinates(point.point)

                if ((px == ex) | (py == ey)):
                    parent.add_child(endNode)
                    return

                if clockwiseRouting :
                    if (((px < ex) & (py < ey)) | ((px > ex) & (py > ey))):
                        newPoint=NetPoint(f"{net.name}_{pointNum}",ex,py)
                    else:
                        newPoint=NetPoint(f"{net.name}_{pointNum}",px,ey)
                else:
                    if (((px < ex) & (py < ey)) | ((px > ex) & (py > ey))):
                        newPoint=NetPoint(f"{net.name}_{pointNum}",px,ey)
                    else:
                        newPoint=NetPoint(f"{net.name}_{pointNum}",ex,py)

                newPoint.bin = design.find_bin(newPoint.get_coordinates())
                pointNum += 1
                                
                newNode = NetTreeNode(newPoint.name,newPoint)
                newNode.add_child(endNode)
                _rearrange_tree(point, newNode)
            # End of inner function

            nonlocal pointNum

            if len(pointsOnBin) == 0:
                # If there are no points of the tree in the bin
                nearestNode = connectionsTree.find_nearest_tree_node(
                    endpoint.get_coordinates())

                nx, ny = get_center_coordinates(nearestNode.point)

                if (endpoint.bin[0] == activeBin[0]):
                    newPoint= NetPoint(f"{net.name}_{pointNum}", nx, ey)
                else:
                    newPoint= NetPoint(f"{net.name}_{pointNum}", ex, ny)
                pointNum += 1

                newNode = NetTreeNode(newPoint.name,newPoint)
                newNode.add_child(endNode)
                _rearrange_tree(nearestNode, newNode)
            # End of if
            elif len(pointsOnBin) == 1:
                parent = pointsOnBin.pop()

                px, py = get_center_coordinates(parent.point)

                _add_intermediate_node(parent)
            # End of elif
            else:
                pointsOnBin.sort(
                    key=lambda dr: _distance_netNodes_sqrd(dr.point))
                parent = pointsOnBin.pop(0)

                px, py = get_center_coordinates(parent.point)

                _add_intermediate_node(parent)
            # End of else
        # End of inner function

        def singleCorner():
            """Connects drain to the existing tree with one intermediate 
            point/corner from backtracking
            """
            nonlocal pointNum

            point = binsQueue.pop()
            if len(pointsOnBin) == 0:
                # If there are no points of the tree in the bin
                nearestNode = connectionsTree.find_nearest_tree_node(
                    endpoint.get_coordinates())
                cx, cy = design.find_center_of_bin(point)

                nearestNode = connectionsTree.find_nearest_tree_node((cx, cy))
                nx, ny = get_center_coordinates(nearestNode.point)

                if (activeBin[0] == nearestNode.point.bin[0]):
                    midPoint = NetPoint(f"{net.name}_{pointNum}", cx, ny)
                else:
                    midPoint = NetPoint(f"{net.name}_{pointNum}", nx, cy)
                pointNum += 1

                midNode = NetTreeNode(midPoint.name,midPoint)
                midNode.point.bin = design.find_bin(midPoint.get_coordinates())
                _rearrange_tree(nearestNode, midNode)

                newPoint=NetPoint(f"{net.name}_{pointNum}",cx, cy)
                newPoint.bin = design.find_bin(newPoint.get_coordinates())

                if (newPoint.bin[0] == endpoint.bin[0]):
                    newPoint.y = ey
                else:
                    newPoint.x = ex

                newNode = NetTreeNode(newPoint.name, newPoint)
                midNode.add_child(newNode)
                pointNum += 1
            # End of if
            elif len(pointsOnBin) == 1:
                parent = pointsOnBin.pop()

                px, py = get_center_coordinates(parent.point)

                if (parent.point.bin[0] == point[0]):
                    newPoint = NetPoint(f"{net.name}_{pointNum}", ex, py)
                else:
                    newPoint = NetPoint(f"{net.name}_{pointNum}", px, ey)
                pointNum += 1

                newPoint.bin = design.find_bin(newPoint.get_coordinates())
                newNode = NetTreeNode(newPoint.name, newPoint)
                parent.add_child(newNode)
            # End of elif
            else:
                pointsOnBin.sort(
                    key=lambda dr: _distance_netNodes_sqrd(dr.point))
                parent = pointsOnBin.pop(0)
                px, py = get_center_coordinates(parent.point)

                if (parent.point.bin[0] == point[0]):
                    newPoint=NetPoint(f"{net.name}_{pointNum}",ex,py)
                else:
                    newPoint=NetPoint(f"{net.name}_{pointNum}",px, ey)
                pointNum += 1

                newPoint.bin = design.find_bin(newPoint.get_coordinates())
                newNode = NetTreeNode(newPoint.name,newPoint)
                parent.add_child(newNode)
            # End of else

            newNode.add_child(endNode)
        # End of inner function

        def multipleCorners():
            """Connects drain to the existing tree with multiple intermediate 
            points/corners from backtracking"""
            nonlocal pointNum

            parent:NetTreeNode = None
            corners: int
            if len(pointsOnBin) == 0:
                # If there are no points of the tree in the bin
                pointBin = binsQueue.pop(0)
                cx, cy = design.find_center_of_bin(pointBin)

                nearestNode = connectionsTree.find_nearest_tree_node((cx, cy))
                nx, ny = get_center_coordinates(nearestNode.point)

                if (activeBin[0] == nearestNode.point.bin[0]):
                    midPoint = NetPoint(f"{net.name}_{pointNum}", cx, ny)
                else:
                    midPoint = NetPoint(f"{net.name}_{pointNum}", nx, cy)
                pointNum += 1

                midNode = NetTreeNode(midPoint.name,midPoint)
                midNode.point.bin = design.find_bin(midPoint.get_coordinates())
                _rearrange_tree(nearestNode, midNode)

                newPoint=NetPoint(f"{net.name}_{pointNum}",cx, cy)
                newPoint.bin = design.find_bin(newPoint.get_coordinates())
                newNode = NetTreeNode(newPoint.name,newPoint)
                midNode.add_child(newNode)
                pointNum += 1

                parent = newNode
                corners = noofCorners -1
            # End of if
            elif len(pointsOnBin) == 1:
                parent = pointsOnBin.pop()
                corners = noofCorners
            # End of elif
            else:
                pointBin = binsQueue.pop(0)
                cx, cy = design.find_center_of_bin(pointBin)
                pointsOnBin.sort(
                    key=lambda dr: _distance_netNodes_sqrd(dr.point))
                parent = pointsOnBin.pop(0)

                px, py = get_center_coordinates(parent.point)

                if (activeBin[0] == parent.point.bin[0]):
                    newPoint = NetPoint(f"{net.name}_{pointNum}", cx, py)
                else:
                    newPoint = NetPoint(f"{net.name}_{pointNum}", px, cy)
                pointNum += 1

                newNode = NetTreeNode(newPoint.name,newPoint)
                newNode.point.bin = design.find_bin(newPoint.get_coordinates())
                _rearrange_tree(parent, newNode)

                parent = newNode
                corners = noofCorners -1
            # End of else

            for i in range(corners):
                pointBin = binsQueue.pop(0)

                px, py = get_center_coordinates(parent.point)
                cx, cy = design.find_center_of_bin(pointBin)

                if (parent.point.bin[0] == pointBin[0]):
                    newPoint=NetPoint(f"{net.name}_{pointNum}",cx, py)
                else:
                    newPoint=NetPoint(f"{net.name}_{pointNum}",px, cy)
                pointNum += 1
                newPoint.bin = design.find_bin(newPoint.get_coordinates())
                newNode = NetTreeNode(newPoint.name,newPoint)
                parent.add_child(newNode)
                parent = newNode
            # End of for

            if (parent.point.bin[0] == endpoint.bin[0]):
                parent.point.y = ey
            else:
                parent.point.x = ex
            parent.add_child(endNode)
        # End of inner function

        nonlocal pointNum
        nonlocal connectionsTree

        ex, ey = get_center_coordinates(endpoint)
        endNode = NetTreeNode(endpoint.name, endpoint)

        pointsOnBin = connectionsTree.find_points_on_bin(activeBin)
        routingLogger.debug(f"Corner bins for net: {binsQueue}")
        routingLogger.debug(f"Points of net in bin: {pointsOnBin}")

        match len(binsQueue):
            # Based on the bins where corners are created
            case 0:
                no_corners()
            case 1:
                singleCorner()
            case noofCorners:
                multipleCorners()
        # End of match len(binsQueue)
    # End of function

    def _distance_bins(bin):
        dist = (sourceBin[0] - bin[0])**2 + (sourceBin[1] - bin[1])**2
        return dist
    # End of function


    # Function body
    if (design.isRouted):
        routingLogger.info("Design is already routed!")
        return

    tempBinsArray = np.zeros(design.bins.size)
    size = design.bins.size

    pointNum = 1
    routingLogger.debug(f"Net: {net.name}")

    if startRoutingFromCenter:
        # For the routing on the center of of the bounding
        # box the source is a new point created there

        cX,cY = calculate_bb_center(net)
        cName = f"{net.name}_center"
        sourcePoint = NetPoint(cName, cX, cY)
        sourcePoint.bin = design.find_bin((cX, cY))
        sourceBin = sourcePoint.bin
        connectionsTree = NetTreeNode(sourcePoint.name, sourcePoint)

        # The new drain is the net's drain plus the given source
        netNewDrain = net.drain.copy()
        netNewDrain.append(net.source)
        netNewDrain.sort(key=lambda dr: _distance_bins(dr.bin))
        netDrain = netNewDrain
    # End of if startRoutingFromCenter
    else:
        # For the default routing the source is the one defined
        sourceBin = net.source.bin
        connectionsTree = NetTreeNode(net.source.name, net.source)
        
        net.drain.sort(key=lambda dr: _distance_bins(dr.bin))
        netDrain = net.drain
    # End of else routing from source

    if (design.blockages[sourceBin] != 0):
        routingLogger.warning(
            f"Net {net.name} cannot be router due to source being into blockage"
        )
        return

    
    netBins = [sourceBin]

    for endpoint in netDrain:
        if (endpoint == net.source):
            continue

        routingLogger.debug(f"Endpoint: {endpoint}")
        drain = endpoint.bin
        if (design.blockages[drain] != 0):
            routingLogger.warning(
                f"In net {net.name}: Endpoint {endpoint.name} is into blockage"
            )
            continue

        binsQueue: list[tuple[int,int]] = []
        _propagate_wave_phase()
        activeBin = _backtracking_phase()

        _connection_phase()

        tempBinsArray.fill(0)
    # End of for loop

    for change in netBins:
        design.bins[change] += 1
    
    routingLogger.debug(f"Routing net {net.name} completed")
    net.connectionsTree = connectionsTree
    
# End of function

def maze_routing(
    design: Design, startRoutingFromCenter = False, clockwiseRouting = True
) -> None:
    """
    Routing algorithm based on Lee's Maze Routing
    """

    if (design.isRouted):
        routingLogger.info("Design is already routed!")
        return

    for net in design.core.nets:
        maze_routing_net(net, design, startRoutingFromCenter, clockwiseRouting)

    design.isRouted = True
    routingLogger.debug("Routing completed")
# End of function


def calculate_bb_center(net:Net) -> tuple[float, float]:
    """
    Calculates and returns the center of the bounding box for the given net.
    """
    sx, sy = get_center_coordinates(net.source)
    xMin = sx
    xMax = xMin
    yMin = sy
    yMax = yMin

    for endpoint in net.drain:
        ex, ey = get_center_coordinates(endpoint)
        # X coordinate
        if (ex < xMin):
            xMin = ex
        if (ex > xMax):
            xMax = ex
        # Y coordinate
        if (ey < yMin):
            yMin = ey
        if (ey > yMax):
            yMax = ey
    
    xCenter = xMin + (xMax - xMin)/2
    yCenter = yMin + (yMax - yMin)/2

    return (xCenter, yCenter)
# End of function

def calculate_net_HPWL(net:Net) -> float:
    """
    Calculates the net wirelength based on its bounding box.

    The total wirelength is equal to half the perimeter of the bounding box.
    """
    sx, sy = get_center_coordinates(net.source)
    xMin = sx
    xMax = xMin
    yMin = sy
    yMax = yMin

    for endpoint in net.drain:
        ex, ey = get_center_coordinates(endpoint)
        # X coordinate
        if (ex < xMin):
            xMin = ex
        if (ex > xMax):
            xMax = ex
        # Y coordinate
        if (ey < yMin):
            yMin = ey
        if (ey > yMax):
            yMax = ey

    return (xMax - xMin) + (yMax - yMin)
# End of function

def calculate_HPWL(design:Design) -> float:
    """
    Calculates the total wirelength of the design using the half-perimeter
    wirelength for each net
    """
    result:float = 0

    for net in design.core.nets:
        result += calculate_net_HPWL(net)
    
    return result
# End of function


def calculate_net_tree_wirelength(net:Net) -> float:
    def _recursive_calculate_wirelength(node:NetTreeNode) -> float:
        if (len(node.children) == 0):
            return 0
        
        result = 0
        nx, ny = get_center_coordinates(node.point)
        child:NetTreeNode
        for child in node.children:
            cx, cy = get_center_coordinates(child.point)
            if (cx == nx):
                result += abs(ny - cy)
            else:
                result += abs(nx - cx)
            
            result += _recursive_calculate_wirelength(child)
        
        return result
    # End of inner function

    return _recursive_calculate_wirelength(net.connectionsTree)
# End of function

def calculate_tree_wirelength(design:Design) -> float:
    result = 0

    for net in design.core.nets:
        result += calculate_net_tree_wirelength(net)

    return result
# End of function
