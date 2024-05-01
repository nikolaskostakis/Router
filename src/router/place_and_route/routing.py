"""
Module containing functions for routing
"""

import logging

import numpy as np

import config
from structures.design_components import Design, IOPort, Component, Net
from structures.design_components import NetPoint, NetTreeNode
from structures.design_components import get_center_coordinates

# Logging
routingLogger = logging.getLogger(__name__)
routingLogger.setLevel(logging.DEBUG)
routingLogger.addHandler(config.consoleHandler)
routingLogger.addHandler(config.logfileHandler)

def maze_routing_net(net:Net, design: Design, clockwiseRouting = True) -> None:
    """
    Routing algorithm based on Lee's Maze Routing for a single net
    """

    def _propagate_wave():
        """
        First stage of the maze routing algorithm.

        Propagates wave from the source (existing net)
        """
        
        activeList:list[tuple[int,int]] = []
        visitedList:list[tuple[int,int]] = []

        activeList.extend(netBins)

        while (len(activeList) != 0):
            activeBin = activeList.pop(0)

            if clockwiseRouting:
                #NESW
                # North
                if (activeBin[0] != 0):
                    north = ((activeBin[0] - 1), activeBin[1])
                    if (
                        (north != drain)
                        & (north not in activeList)
                        & (north not in visitedList)
                        & (design.blockages[north] == 0)
                    ):
                        activeList.append(north)
                        tempBinsArray[north] = tempBinsArray[activeBin] + 1
                # End if North
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if (
                        (east != drain)
                        & (east not in activeList)
                        & (east not in visitedList)
                        & (design.blockages[east] == 0)
                    ):
                        activeList.append(east)
                        tempBinsArray[east] = tempBinsArray[activeBin] + 1
                # End if East
                # South
                if ((activeBin[0] +1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if (
                        (south != drain)
                        & (south not in activeList)
                        & (south not in visitedList)
                        & (design.blockages[south] == 0)
                    ):
                        activeList.append(south)
                        tempBinsArray[south] = tempBinsArray[activeBin] + 1
                # End if South
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if (
                        (west != drain)
                        & (west not in activeList)
                        & (west not in visitedList)
                        & (design.blockages[west] == 0)
                    ):
                        activeList.append(west)
                        tempBinsArray[west] = tempBinsArray[activeBin] + 1
                # End if West
            # End if clockwise
            else:
                #NWSE
                # North
                if (activeBin[0] != 0):
                    north = ((activeBin[0] - 1), activeBin[1])
                    if (
                        (north != drain)
                        & (north not in activeList)
                        & (north not in visitedList)
                        & (design.blockages[north] == 0)
                    ):
                        activeList.append(north)
                        tempBinsArray[north] = tempBinsArray[activeBin] + 1
                # End if North
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if (
                        (west != drain)
                        & (west not in activeList)
                        & (west not in visitedList)
                        & (design.blockages[west] == 0)
                    ):
                        activeList.append(west)
                        tempBinsArray[west] = tempBinsArray[activeBin] + 1
                # End if West
                # South
                if ((activeBin[0] +1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if (
                        (south != drain)
                        & (south not in activeList)
                        & (south not in visitedList)
                        & (design.blockages[south] == 0)
                    ):
                        activeList.append(south)
                        tempBinsArray[south] = tempBinsArray[activeBin] + 1
                # End if South
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if (
                        (east != drain)
                        & (east not in activeList)
                        & (east not in visitedList)
                        & (design.blockages[east] == 0)
                    ):
                        activeList.append(east)
                        tempBinsArray[east] = tempBinsArray[activeBin] + 1
                # End if East
            # End else
            visitedList.append(activeBin)
        # End of while
    # End of function

    def _backtrace():
        """
        Second stage of the maze routing algorithm.

        Backtraces from the destination to the source.
        """
        backtraceRoute = []

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
                    if (tempBinsArray[north] < value) & (north != drain) & (design.blockages[north] == 0):
                        nextBin = north
                        newDirection = "NORTH"
                        value = tempBinsArray[north]
                # End if North
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if (tempBinsArray[east] < value) & (east != drain) & (design.blockages[east] == 0):
                        nextBin = east
                        newDirection = "EAST"
                        value = tempBinsArray[east]
                # End if East
                # South
                if ((activeBin[0] +1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if (tempBinsArray[south] < value) & (south != drain) & (design.blockages[south] == 0):
                        nextBin = south
                        newDirection = "SOUTH"
                        value = tempBinsArray[south]
                # End if South
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if (tempBinsArray[west] < value) & (west != drain) & (design.blockages[west] == 0):
                        nextBin = west
                        newDirection = "WEST"
                        value = tempBinsArray[west]
                # End if West
            # End if clockwise
            else:
                #NWSE
                # North
                if (activeBin[0] != 0):
                    north = ((activeBin[0] - 1), activeBin[1])
                    if (tempBinsArray[north] < value) & (north != drain):
                        nextBin = north
                        newDirection = "NORTH"
                        value = tempBinsArray[north]
                # End if North
                # West
                if (activeBin[1] != 0):
                    west = (activeBin[0], (activeBin[1] - 1))
                    if (tempBinsArray[west] < value) & (west != drain):
                        nextBin = west
                        newDirection = "WEST"
                        value = tempBinsArray[west]
                # End if West
                # South
                if ((activeBin[0] +1) != size[0]):
                    south = ((activeBin[0] + 1), activeBin[1])
                    if (tempBinsArray[south] < value) & (south != drain):
                        nextBin = south
                        newDirection = "SOUTH"
                        value = tempBinsArray[south]
                # End if South
                # East
                if ((activeBin[1] + 1) != size[1]):
                    east = (activeBin[0], (activeBin[1] + 1))
                    if (tempBinsArray[east] < value) & (east != drain):
                        nextBin = east
                        newDirection = "EAST"
                        value = tempBinsArray[east]
                # End if East
            # End else

            if ((direction != None) & (direction != newDirection)):
                binsQueue.insert(0, activeBin)

            backtraceRoute.append(activeBin)
            activeBin = nextBin

            direction = newDirection
        netBins.extend(backtraceRoute)
        return activeBin
    # End of function

    def _connect_points():
        def _distance_netNodes_sqrd(point):
            """
            Returns the distance squared between the endpoint an a given point
            """
            dist = (endpoint.x - point.x)**2 + (endpoint.y - point.y)**2
            return dist
        # End of inner function

        def _expand_connections_tree(
                point:NetTreeNode,
                endpoint:(IOPort | Component),
            ):
            nonlocal pointNum
            """Adds new point between endpoint and existing point"""
            px, py = get_center_coordinates(point.point)
            ex, ey = get_center_coordinates(endpoint)

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
            newNode.add_child(NetTreeNode(endpoint.name, endpoint))
            _rearrange_tree(point, newNode)
        # End of inner function

        def _rearrange_tree(node: NetTreeNode, newNode: NetTreeNode):
            """
            Determines if the new node is a child or a new parent to the old
            """
            nx,ny = get_center_coordinates(node.point)
            nnx,nny = get_center_coordinates(newNode.point)
            if ((parentNode := node.parent) is not None):
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

        nonlocal pointNum
        nonlocal connectionsTree
        pointsOnBin = connectionsTree.find_points_on_bin(activeBin)
        routingLogger.debug(f" <> {binsQueue} {pointsOnBin}")
        match len(binsQueue):
            case 0:
                match len(pointsOnBin):
                    case 0:
                        nearestNode = connectionsTree.find_nearest_tree_node(
                            endpoint.get_coordinates())

                        nx, ny = get_center_coordinates(nearestNode.point)
                        ex, ey = get_center_coordinates(endpoint)

                        if (endpoint.bin[0] == activeBin[0]):
                            newPoint= NetPoint(f"{net.name}_{pointNum}", nx, ey)
                        else:
                            newPoint= NetPoint(f"{net.name}_{pointNum}", ex, ny)
                        pointNum += 1

                        newNode = NetTreeNode(newPoint.name,newPoint)
                        newNode.add_child(NetTreeNode(endpoint.name, endpoint))
                        _rearrange_tree(nearestNode, newNode)
                    case 1:
                        parent = pointsOnBin.pop()

                        px, py = get_center_coordinates(parent.point)
                        ex, ey = get_center_coordinates(endpoint)

                        if ((px == ex) | (py == ey)):
                            parent.add_child(
                                NetTreeNode(endpoint.name, endpoint))
                        else:
                            _expand_connections_tree(parent, endpoint)
                            
                    case multiplePoints:
                        pointsOnBin.sort(
                            key=lambda dr: _distance_netNodes_sqrd(dr.point))
                        parent = pointsOnBin.pop(0)

                        px, py = get_center_coordinates(parent.point)
                        ex, ey = get_center_coordinates(endpoint)

                        if ((px == ex) | (py == ey)):
                            parent.add_child(
                                NetTreeNode(endpoint.name, endpoint))
                        else:
                            _expand_connections_tree(parent, endpoint)
            case 1:
                point = binsQueue.pop()
                match len(pointsOnBin):
                    case 0:
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
                        midNode.bin = design.find_bin(midPoint.get_coordinates())
                        _rearrange_tree(nearestNode, midNode)

                        newPoint=NetPoint(f"{net.name}_{pointNum}",cx, cy)
                        newPoint.bin = design.find_bin(newPoint.get_coordinates())
                        routingLogger.info(f"{newPoint}")
                        newNode = NetTreeNode(newPoint.name,newPoint)
                        midNode.add_child(newNode)
                        pointNum += 1

                        ex, ey = get_center_coordinates(endpoint)

                        if (newNode.point.bin[0] == endpoint.bin[0]):
                            newNode.point.y = ey
                        else:
                            newNode.point.x = ex
                        newNode.add_child(NetTreeNode(endpoint.name, endpoint))
                    case 1:
                        parent = pointsOnBin.pop()

                        px, py = get_center_coordinates(parent.point)
                        ex, ey = get_center_coordinates(endpoint)

                        if (parent.point.bin[0] == point[0]):
                            newPoint=NetPoint(f"{net.name}_{pointNum}",ex,py)
                        else:
                            newPoint=NetPoint(f"{net.name}_{pointNum}",px, ey)
                        pointNum += 1
                        newPoint.bin = design.find_bin(newPoint.get_coordinates())
                        newNode = NetTreeNode(newPoint.name,newPoint)
                        parent.add_child(newNode)
                        newNode.add_child(NetTreeNode(endpoint.name, endpoint))
                        #_rearrange_tree(parent,newNode)
                    case multiplePoints:
                        pointsOnBin.sort(
                            key=lambda dr: _distance_netNodes_sqrd(dr.point))
                        parent = pointsOnBin.pop(0)
                        px, py = get_center_coordinates(parent.point)
                        ex, ey = get_center_coordinates(endpoint)

                        if (parent.point.bin[0] == point[0]):
                            newPoint=NetPoint(f"{net.name}_{pointNum}",ex,py)
                        else:
                            newPoint=NetPoint(f"{net.name}_{pointNum}",px, ey)
                        pointNum += 1
                        newPoint.bin = design.find_bin(newPoint.get_coordinates())
                        newNode = NetTreeNode(newPoint.name,newPoint)
                        parent.add_child(newNode)
                        newNode.add_child(NetTreeNode(endpoint.name, endpoint))
            case moreBTPoints:
                routingLogger.info(f"More points from backtrace {moreBTPoints}")
                routingLogger.info(binsQueue)
                match len(pointsOnBin):
                    case 0:
                        routingLogger.info("Zero points of the tree")
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
                        for i in range(moreBTPoints - 1):
                            routingLogger.info(f"Parent: {parent}")
                            pointBin = binsQueue.pop(0)

                            px, py = get_center_coordinates(parent.point)
                            cx, cy = design.find_center_of_bin(pointBin)

                            routingLogger.info(f"== {parent.point.bin} {pointBin}")
                            if (parent.point.bin[0] == pointBin[0]):
                                newPoint=NetPoint(f"{net.name}_{pointNum}",cx, py)
                            else:
                                newPoint=NetPoint(f"{net.name}_{pointNum}",px, cy)
                            pointNum += 1
                            newPoint.bin = design.find_bin(newPoint.get_coordinates())
                            newNode = NetTreeNode(newPoint.name,newPoint)
                            parent.add_child(newNode)
                            parent = newNode
                            #
                        ex, ey = get_center_coordinates(endpoint)

                        if (parent.point.bin[0] == endpoint.bin[0]):
                            parent.point.y = ey
                        else:
                            parent.point.x = ex
                        parent.add_child(NetTreeNode(endpoint.name, endpoint))
                    case 1:
                        routingLogger.info("One point of the tree")
                        parent = pointsOnBin.pop()
                        for i in range(moreBTPoints):
                            routingLogger.info(f"Parent: {parent}")
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
                            #
                        ex, ey = get_center_coordinates(endpoint)

                        if (parent.point.bin[0] == endpoint.bin[0]):
                            parent.point.y = ey
                        else:
                            parent.point.x = ex
                        parent.add_child(NetTreeNode(endpoint.name, endpoint))
                    case multiplePoints:
                        routingLogger.info(f"Multiple points: {multiplePoints}")

                        pointBin = binsQueue.pop(0)
                        cx, cy = design.find_center_of_bin(pointBin)
                        pointsOnBin.sort(
                            key=lambda dr: _distance_netNodes_sqrd(dr.point))
                        parent = pointsOnBin.pop(0)
                        routingLogger.info(f"parent: {parent}")
                        routingLogger.info(f"point: {pointBin}")

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
                        for i in range(moreBTPoints - 1):
                            routingLogger.info(f"Parent: {parent}")
                            pointBin = binsQueue.pop(0)

                            px, py = get_center_coordinates(parent.point)
                            cx, cy = design.find_center_of_bin(pointBin)

                            routingLogger.info(f"== {parent.point.bin} {pointBin}")
                            if (parent.point.bin[0] == pointBin[0]):
                                newPoint=NetPoint(f"{net.name}_{pointNum}",cx, py)
                            else:
                                newPoint=NetPoint(f"{net.name}_{pointNum}",px, cy)
                            pointNum += 1
                            newPoint.bin = design.find_bin(newPoint.get_coordinates())
                            newNode = NetTreeNode(newPoint.name,newPoint)
                            parent.add_child(newNode)
                            parent = newNode
                            #
                        ex, ey = get_center_coordinates(endpoint)

                        if (parent.point.bin[0] == endpoint.bin[0]):
                            parent.point.y = ey
                        else:
                            parent.point.x = ex
                        parent.add_child(NetTreeNode(endpoint.name, endpoint))

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

    sourceBin = net.source.bin
    if (design.blockages[sourceBin] != 0):
        routingLogger.warning(
            f"Net {net.name} cannot be router due to source being into blockage"
        )
        return

    connectionsTree = NetTreeNode(net.source.name, net.source)
    netBins = [sourceBin]

    net.drain.sort(key=lambda dr: _distance_bins(dr.bin))

    for endpoint in net.drain:
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
        _propagate_wave()
        activeBin = _backtrace()

        _connect_points()

        tempBinsArray.fill(0)
    # End of for loop

    for change in netBins:
        design.bins[change] += 1
    
    routingLogger.debug(f"Routing net {net.name} completed")
    net.connectionsTree = connectionsTree
    
# End of function

def maze_routing(design: Design, clockwiseRouting = True) -> None:
    """
    Routing algorithm based on Lee's Maze Routing
    """

    if (design.isRouted):
        routingLogger.info("Design is already routed!")
        return

    for net in design.core.nets:
        maze_routing_net(net, design, clockwiseRouting)

    design.isRouted = True
    routingLogger.debug("Routing completed")
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
