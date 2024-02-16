"""
Module containing functions for routing
"""

import logging
from time import sleep

import numpy as np

import config
from structures.design_components import Design, NetTreeNode, NetPoint, find_points_on_bin
from structures.trees import print_generic_tree

# Logging
routingLogger = logging.getLogger(__name__)
routingLogger.setLevel(logging.DEBUG)
routingLogger.addHandler(config.consoleHandler)

def maze_routing(design: Design) -> None:
    def _propagate_wave():
        
        activeList = []
        visitedList = []

        activeList.extend(netBins)

        while (len(activeList) != 0):
            active = activeList.pop(0)
            #NESW
            # North
            if (active[0] != 0):
                north = ((active[0] - 1), active[1])
                if (
                    (north != drain) &
                    (north not in activeList) &
                    (north not in visitedList)
                ):
                    activeList.append(north)
                    tempBinsArray[north] = tempBinsArray[active] + 1
                            
            # East
            if ((active[1] + 1) != size[1]):
                east = (active[0], (active[1] + 1))
                if (
                    (east != drain) &
                    (east not in activeList) &
                    (east not in visitedList)
                ):
                    activeList.append(east)
                    tempBinsArray[east] = tempBinsArray[active] + 1
            # South
            if ((active[0] +1) != size[0]):
                south = ((active[0] + 1), active[1])
                if (
                    (south != drain) &
                    (south not in activeList) &
                    (south not in visitedList)
                ):
                    activeList.append(south)
                    tempBinsArray[south] = tempBinsArray[active] + 1
            # West
            if (active[1] != 0):
                west = (active[0], (active[1] - 1))
                if (
                    (west != drain) &
                    (west not in activeList) &
                    (west not in visitedList)
                ):
                    activeList.append(west)
                    tempBinsArray[west] = tempBinsArray[active] + 1
            visitedList.append(active)

        #print(tempBinsArray)
    # End of function

    def _backtrace():
        bt = []

        active = drain
        direction = None
        value = size[0] + size[1]
        while True:
            if (active in netBins):
                break

            #NESW
            # North
            if (active[0] != 0):
                north = ((active[0] - 1), active[1])
                if (tempBinsArray[north] < value) & (north != drain):
                    next = north
                    newDirection = "NORTH"
                    value = tempBinsArray[north]
            # East
            if ((active[1] + 1) != size[1]):
                east = (active[0], (active[1] + 1))
                if (tempBinsArray[east] < value) & (east != drain):
                    next = east
                    newDirection = "EAST"
                    value = tempBinsArray[east]
            # South
            if ((active[0] +1) != size[0]):
                south = ((active[0] + 1), active[1])
                if (tempBinsArray[south] < value) & (south != drain):
                    next = south
                    newDirection = "SOUTH"
                    value = tempBinsArray[south]
            # West
            if (active[1] != 0):
                west = (active[0], (active[1] - 1))
                if (tempBinsArray[west] < value) & (west != drain):
                    next = west
                    newDirection = "WEST"
                    value = tempBinsArray[west]

            if ((direction != None) & (direction != newDirection)):
                print(f"POINT {active}")
                binsQueue.insert(0, active)

            bt.append(active)
            active = next

            direction = newDirection
        netBins.extend(bt)
        return active
    # End of function
    
    def _connect_points():
        print(f"Size {len(binsQueue)}")
        if (len(binsQueue) == 0):
            match len(results := find_points_on_bin(connectionsTree, xa)):
                case 0:
                    print("God Help me!")
                case 1:
                    print(f"One in line  {results}")
                    parent = results.pop()
                    print(parent.children)

                    if ((parent.point.x == endpoint.x)
                        | (parent.point.y == endpoint. y)):
                        parent.add_child(NetTreeNode(endpoint.name, endpoint))
                    else:
                        if (parent.point.__class__.__name__ == "Component"):
                            px = parent.point.x + (parent.point.width / 2)
                            py = parent.point.y + (parent.point.height / 2)
                        else:
                            px, py = parent.point.get_coordinates()
                        
                        if (endpoint.__class__.__name__ == "Component"):
                            ex = endpoint.x + (endpoint.width / 2)
                            ey = endpoint.y + (endpoint.height / 2)
                        else:
                            ex, ey = endpoint.get_coordinates()

                        if (((px < ex) & (py < ey))
                            | ((px > ex) & (py > ey))):
                            newPoint=NetPoint("ha",ex,py)
                        else:
                            newPoint=NetPoint("ha",px,ey)
                        newPoint.bin = design.find_bin(newPoint.get_coordinates())
                        mid = NetTreeNode("Ho",newPoint)
                        parent.add_child(mid)
                        mid.add_child(end:=NetTreeNode(endpoint.name, endpoint))
                case default:
                    print(f"More {default}")

        for point in binsQueue:
            print(f"HAHAHA {point}")

            match len(results := find_points_on_bin(connectionsTree, xa)):
                case 0:
                    print("Empty")
                case 1:
                    print(f"One {results}")
                    parent = results.pop()
                    print(parent.children)

                    if (parent.point.__class__.__name__ == "Component"):
                        px = parent.point.x + (parent.point.width / 2)
                        py = parent.point.y + (parent.point.height / 2)
                    else:
                        px, py = parent.point.get_coordinates()
                    
                    if (endpoint.__class__.__name__ == "Component"):
                        ex = endpoint.x + (endpoint.width / 2)
                        ey = endpoint.y + (endpoint.height / 2)
                    else:
                        ex, ey = endpoint.get_coordinates()

                    if (parent.point.bin[0] == point[0]):
                        newPoint=NetPoint("ho",ex,py)
                    else:
                        newPoint=NetPoint("ho",px, ey)
                    newPoint.bin = design.find_bin(newPoint.get_coordinates())
                    mid = NetTreeNode("Ho",newPoint)
                    parent.add_child(mid)
                    mid.add_child(end:=NetTreeNode(endpoint.name, endpoint))
                case default:
                    print(f"WOW {default}")



    def _distance(bin):
        dist = (source[0] - bin[0])**2 + (source[1] - bin[1])**2
        return dist
    # End of function

    tempBinsArray = np.zeros(design.bins.size)
    size = design.bins.size


    for net in design.core.nets:
        #net = design.core.nets[2]
        source = net.source.bin

        connectionsTree = NetTreeNode(net.source.name, net.source)
        print_generic_tree(connectionsTree)
        netBins = [source]

        net.drain.sort(key=lambda dr: _distance(dr.bin))

        for endpoint in net.drain:
            print(f"ENDPOINT:  {endpoint}")
            drain = endpoint.bin
            binsQueue = []
            _propagate_wave()
            xa = _backtrace()

            _connect_points()
            #print(tempBinsArray)

            tempBinsArray.fill(0)

            #print(netBins)
        
        for change in netBins:
            design.bins[change] += 1
        
        #sleep(5)
        routingLogger.debug("Routing completed")
        routingLogger.info("Routing completed")
        print_generic_tree(connectionsTree)

        net.connectionsTree = connectionsTree
# End of function