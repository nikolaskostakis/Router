"""
Module
"""
import numpy as np

from structures.design_components import Design

def maze_routing(design: Design) -> None:
    def propagate_wave():
        
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

    def backtrace():
        bt = []

        active = drain
        value = size[0] + size[1]
        while True:
            if (active in netBins):
                break
            print(f"=====> Active {active}, Value {value}")

            #NESW
            # North
            if (active[0] != 0):
                north = ((active[0] - 1), active[1])
                print(f"north {tempBinsArray[north]}")
                if (tempBinsArray[north] < value) & (north != drain):
                    print("Choice")
                    next = north
                    value = tempBinsArray[north]
            # East
            if ((active[1] + 1) != size[1]):
                east = (active[0], (active[1] + 1))
                print(f"east {tempBinsArray[east]}")
                if (tempBinsArray[east] < value) & (east != drain):
                    print("Choice")
                    next = east
                    value = tempBinsArray[east]
            # South
            if ((active[0] +1) != size[0]):
                south = ((active[0] + 1), active[1])
                print(f"south {tempBinsArray[south]}")
                if (tempBinsArray[south] < value) & (south != drain):
                    print("Choice")
                    next = south
                    value = tempBinsArray[south]
            # West
            if (active[1] != 0):
                west = (active[0], (active[1] - 1))
                print(f"west {tempBinsArray[west]}")
                if (tempBinsArray[west] < value) & (west != drain):
                    print("Choice")
                    next = west
                    value = tempBinsArray[west]

            bt.append(active)
            active = next
        netBins.extend(bt)
    # End of function

    def distance(bin):
        dist = (source[0] - bin[0])**2 + (source[1] - bin[1])**2
        print(f"Distance: {dist}")
        return dist
    # End of function

    tempBinsArray = np.zeros(design.bins.size)
    size = design.bins.size


    for net in design.core.nets:
        source = net.source.bin
        netBins = [source]
        print(net.drain)
        net.drain.sort(key=lambda dr: distance(dr.bin))
        print(net.drain)

        print(netBins)
        for endpoint in net.drain:
            drain = endpoint.bin
            print(f"Drain: {drain}")
            propagate_wave()
            backtrace()

            tempBinsArray.fill(0)

            print(netBins)
        
        for change in netBins:
            design.bins[change] += 1

# End of function