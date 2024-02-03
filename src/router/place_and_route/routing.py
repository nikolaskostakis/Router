"""
Module
"""
import logging

import numpy as np

import config
from structures.design_components import Design

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

        print(tempBinsArray)
    # End of function

    def _backtrace():
        bt = []

        active = drain
        value = size[0] + size[1]
        while True:
            if (active in netBins):
                break

            #NESW
            # North
            if (active[0] != 0):
                north = ((active[0] - 1), active[1])
                print(f"north {tempBinsArray[north]}")
                if (tempBinsArray[north] < value) & (north != drain):
                    next = north
                    value = tempBinsArray[north]
            # East
            if ((active[1] + 1) != size[1]):
                east = (active[0], (active[1] + 1))
                print(f"east {tempBinsArray[east]}")
                if (tempBinsArray[east] < value) & (east != drain):
                    next = east
                    value = tempBinsArray[east]
            # South
            if ((active[0] +1) != size[0]):
                south = ((active[0] + 1), active[1])
                print(f"south {tempBinsArray[south]}")
                if (tempBinsArray[south] < value) & (south != drain):
                    next = south
                    value = tempBinsArray[south]
            # West
            if (active[1] != 0):
                west = (active[0], (active[1] - 1))
                print(f"west {tempBinsArray[west]}")
                if (tempBinsArray[west] < value) & (west != drain):
                    next = west
                    value = tempBinsArray[west]

            bt.append(active)
            active = next
        netBins.extend(bt)
    # End of function

    def _distance(bin):
        dist = (source[0] - bin[0])**2 + (source[1] - bin[1])**2
        return dist
    # End of function

    tempBinsArray = np.zeros(design.bins.size)
    size = design.bins.size


    for net in design.core.nets:
        source = net.source.bin
        netBins = [source]
        print(net.drain)
        net.drain.sort(key=lambda dr: _distance(dr.bin))
        print(net.drain)

        for endpoint in net.drain:
            drain = endpoint.bin
            _propagate_wave()
            _backtrace()

            tempBinsArray.fill(0)

            print(netBins)
        
        for change in netBins:
            design.bins[change] += 1
    
    routingLogger.debug("Routing completed")
# End of function