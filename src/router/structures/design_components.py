"""
Module housing the design components used for the router
"""

import numpy as np
from numpy import ndarray

from .trees import GenericTreeNode

# Class BaseDesignElement
class BaseDesignElement:
    """Base class used for a design element"""

    _name: str = None
    """Name of design element"""
    _x: float = None
    """X Coordinate"""
    _y: float = None
    """Y Coordinate"""

    def __init__(self, name:str, x:float, y:float) -> None:
        self._name = name
        self._x = x
        self._y = y
    # End of method

    # Name
    @property
    def name(self) -> str:
        """Returns the name"""
        return self._name
    # End of method

    # Coordinates
    @property
    def x(self) -> float:
        """Returns x-coordinate"""
        return self._x
    # End of method

    @x.setter
    def x(self, newX:float) -> None:
        """Assign new x-coordinate"""
        self._x = newX
    # End of method

    @property
    def y(self) -> float:
        """Returns y-coordinate"""
        return self._y
    # End of method
    
    @y.setter
    def y(self, newY):
        self._y = newY
    # End of method

    def get_coordinates(self) -> tuple[float, float]:
        """Returns the coordinates (x,y)"""
        return self._x, self._y
    # End of method
# End of class


# Class RectangleDesignElement
class RectangleDesignElement(BaseDesignElement):
    """Base class used for design elements with rectangular shape"""

    _width: float = None
    """Widht of the design element"""
    _height: float = None
    """ Height of the design element"""

    def __init__(self, name:str, x:float, y:float,
                 width: float, height: float) -> None:
        super().__init__(name, x, y)
        self._width = width
        self._height = height
    # End of method

    # Dimensions
    @property
    def width(self) -> float:
        """Returns width"""
        return self._width
    # End of method

    @property
    def height(self) -> float:
        """Returns heigh"""
        return self._height
    # End of method

    def get_dimentions(self) -> tuple[float, float]:
        """Returns dimentions (width, height)"""
        return self._width, self._height
    # End of method
# End of class


# Class Row
class Row(RectangleDesignElement):
    """A class used to represent a row of the design"""

    # private data
    _type: str = None     
    """ Row type """

    def __init__(self, name:str, type:str, x:float, y:float,
                 width: float, height: float) -> None:
        super().__init__(name, x, y, width, height)
        self._type = type
    # End of method

    def __repr__(self) -> None:
        return f"Row: {self._name} Type: {self._type} " \
               f"Location: {self._x:.3f} {self._y:.3f} " \
               f"Width/Height: {self._width:.3f} {self._height:.3f}" 
    # End of method
# End of class


# Class IOPort
class IOPort(BaseDesignElement):
    """A class used to represent an I/O port of the design"""

    # Private data
    _side: str = None
    """Side of the core where port is"""
    _bin: tuple[int,int] = None
    """Bin where the port is"""

    def __init__(self, name:str, x:float, y:float, side:str) -> None:
        super().__init__(name, x, y)
        self._side = side
    # End of method

    def __repr__(self) -> None:
        repr_str = f"IO: {self._name} Location: {self._x:.3f} {self._y:.3f}" \
                   f" {self._side} SIDE" 
        if self._bin:
            repr_str += f" Bin: {self._bin}"
        return repr_str
    # End of method
    
    @property
    def bin(self) -> tuple[int, int]:
        """"""
        return self._bin
    # End of method
    
    @bin.setter
    def bin(self, newBin) -> None:
        self._bin = newBin
    # End of method
# End of class


# Class Component
class Component(RectangleDesignElement):
    """A class used to represent a component of the design"""

    # Component dimentions based on older Practical Format files
    OLD_PF_COMP_WIDTH = 1.260
    """Component Width from older praactical format inputs"""
    OLD_PF_COMP_HEIGHT = 0.576
    """Component Height from older praactical format inputs"""

    _bin: tuple[int,int] = None
    """Bin where the component is"""

    _type: str = None
    _timingType: str = None

    def __init__(self, name:str, type:str = "n/a", timingType:str = "n/a",
                 width:float = OLD_PF_COMP_WIDTH,
                 heigh:float = OLD_PF_COMP_HEIGHT) -> None:
        super().__init__(name, 0, 0, width, heigh)
        self._type = type
        self._timingType = timingType
    # End of method

    def __repr__(self) -> None:
        rep_str = f"Component: {self.name} Cell_Type: {self._type} " \
                  f"Cell_Timing_Type: {self._timingType} " \
                  f"Location: {self._x:.3f} {self._y:.3f}"
        if self._bin:
            rep_str += f" Bin: {self._bin}"
        return rep_str
    # End of method

    @property
    def bin(self) -> tuple[int, int]:
        """"""
        return self._bin
    # End of method
    
    @bin.setter
    def bin(self, newBin) -> None:
        self._bin = newBin
    # End of method

    def get_center(self) -> tuple[float, float]:
        """Returns the center of the component"""
        return (self.x + self._width/2), (self.y + self._height/2)
    # End of method
# End of class


# Class Netpoint
class NetPoint(BaseDesignElement):
    """A class used to represent a component of the design"""

    _bin: tuple[int,int] = None
    """Bin where the point is"""

    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name, x, y)
    # End of method

    @property
    def bin(self) -> tuple[int, int]:
        """"""
        return self._bin
    # End of method
    
    @bin.setter
    def bin(self, newBin) -> None:
        self._bin = newBin
    # End of method
# End of class


# Class NetTreeNode
class NetTreeNode:
    pass

class NetTreeNode(GenericTreeNode):
    """
    A class used to represent the shape of the net after the routing

    The net is a tree with its source as its root and the leaves been the
    endpoints
    """

    _point:(IOPort|Component|NetPoint)

    def __init__(self, name:str,
                 point:(IOPort|Component|NetPoint),
                 parent:NetTreeNode = None):
        super().__init__(name, parent)
        self._point = point
    # End of method

    def __repr__(self) -> str:
        return f"{self._name}"

    @property
    def point(self) -> (IOPort|Component|NetPoint):
        """"""
        return self._point
    # End of method

    def find_points_on_bin(self, bin:tuple[int,int]):
        def _recursive_search(node:NetTreeNode):
            if bin == node.point.bin:
                result = [node]
            else:
                result = []

            for child in node.children:
                result.extend(_recursive_search(child))
            return result
        # End of inner function

        return _recursive_search(self)
    # End of method

    def find_nearest_tree_node(self, destination:tuple[float,float]):
        def _distance(point:tuple[float,float]):
            distance = (point[0] - destination[0])**2 \
                       + (point[1] - destination[1])**2
            return distance
        # End of function

        def _recursive_nearest_search(node:NetTreeNode) -> NetTreeNode:
            if (len(node.children) == 0):
                return node

            if (node.__class__.__name__ == "Component"):
                shortestDist = _distance(node.point.get_center())
            else:
                shortestDist = _distance(node.point.get_coordinates())
            shortestPoint = node

            for child in node.children:
                childShortestPoint = _recursive_nearest_search(child)
                if (node.__class__.__name__ == "Component"):
                    childShortestDist = _distance(
                        childShortestPoint.point.get_center())
                else:
                    childShortestDist = _distance(
                        childShortestPoint.point.get_coordinates())
                
                if (childShortestDist < shortestDist):
                    shortestPoint = childShortestPoint
                    shortestDist = childShortestDist
            
            return shortestPoint
        # End of function

        return _recursive_nearest_search(self)
    # End of method
# End of class


# Class Net
class Net:
    """
    A Class used to represent a net of the design
    """

    _name: str = None

    _source: (IOPort | Component)= None
    _drain: list[IOPort | Component] = []

    connectionsTree: NetTreeNode = None

    def __init__(self, name:str, source:(IOPort|Component),
                 drain:list[IOPort|Component]):
        self._name = name
        self._source = source
        self._drain = drain
    # End of method

    def __repr__(self):
        drain = " ".join([d.name for d in self._drain])
        rep_str = f"Net: {self._name} Source: {self._source.name} " \
                  f"Drain: {drain}"
        return rep_str
    # End of method

    # Name
    @property
    def name(self) -> str:
        """Returns the name"""
        return self._name
    # End of method

    @property
    def source(self):
        return self._source
    # End of method

    @property
    def drain(self):
        return self._drain
    # End of method
# End of class


# Class Core
class Core(RectangleDesignElement):
    """A class used to represent a core of the design"""

    _coreUtil: int = None
    _aspectRatio: float = None
    _xOffset: float = None
    _yOffset: float = None

    _rows: list[Row] = []
    _ioParts: list[IOPort] = []
    _components: list[Component] = []
    _nets: list[Net] = []

    def __init__(self, coreUtil:int, width:float, height:float,
                 aspectRatio:float, xOffset:float, yOffset:float):
        super().__init__("Core", 0, 0, width, height)
        self._coreUtil = coreUtil
        self._aspectRatio = aspectRatio
        self._xOffset = xOffset
        self._yOffset = yOffset
    # End of method

    def __repr__(self):
        return f"Core Utilisation: {self._coreUtil:2d}%\n" \
               f"Core Width, Height: {self._width:.3f}, {self._height:.3f}, "\
               f"Aspect Ratio: {self._aspectRatio:.3f}\n" \
               f"Core X, Y Offsets: {self._xOffset:.3f}, {self._yOffset:.3f}"
    # End of method

    # Offsets
    @property
    def x_offset(self) -> float:
        return self._xOffset
    # End of method
    
    @property
    def y_offset(self) -> float:
        return self._yOffset
    # End of method

    # Rows
    @property
    def rows(self) -> list[Row]:
        return self._rows
    # End of method

    def add_row(self, newRow: Row) -> None:
        # Check if the the new row is object of class Row
        if (not isinstance(newRow, Row)):
            raise TypeError("Object is not a Row")

        self._rows.append(newRow)
    # End of method

    def noof_rows(self) -> int:
        return len(self._rows)
    # End of method

    # I/O ports
    @property
    def ioPorts(self) -> list[IOPort]:
        return self._ioParts
    # End of method

    def add_IO_port(self, newIOPort: IOPort) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newIOPort, IOPort)):
            raise TypeError("Object is not an I/O Port")

        self._ioParts.append(newIOPort)
    # End of method

    def get_IO_port(self, name:str=None) -> (IOPort|None):
        """Returns IO Port with given name"""
        if not self._ioParts:
            return None

        for port in self._ioParts:
            if (port.name == name):
                return port

        return None
    # End of method

    def noof_IO_ports(self) -> int:
        return len(self._ioParts)
    # End of method
    
    # Components
    @property
    def components(self) -> list[Component]:
        return self._components

    def add_component(self, newComponent: Component) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newComponent, Component)):
            raise TypeError("Object is not a Component")

        self._components.append(newComponent)
    # End of method

    def get_component(self, name:str=None) -> (Component|None):
        """Returns Component with given name"""
        if not self._components:
            return None

        for comp in self._components:
            if (comp.name == name):
                return comp

        return None
    # End of method

    def noof_components(self) -> int:
        return len(self._components)
    # End of method

    # Nets
    @property
    def nets(self) -> list[Net]:
        return self._nets
    # End of method

    def add_net(self, newNet: Net) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newNet, Net)):
            raise TypeError("Object is not a Net")

        self._nets.append(newNet)
    # End of method

    def get_net(self, name: str) -> (Net | None):
        """Returns Net with given name"""
        if not self._nets:
            return None

        for net in self._nets:
            if (net.name == name):
                return net
        
        return None
    # End of method

    def noof_nets(self) -> int:
        return len(self._nets)
    # End of method
# End of class


# Class Bins
class Bins:
    """ A class used to represent the bins used for routing"""

    _bins:ndarray = None
    """The array of bins"""
    
    _size:tuple[int,int] = None
    """The size of the bins array (y,x)"""

    def __init__(self, width:int, height:int) -> None:
        self._size = (height, width)
        self._bins = np.zeros(self._size)
    # End of method

    def __repr__(self) -> str:
        return f"Bins {self.size}:\n{self._bins}"
    # End of method
    
    def __getitem__(self, index: tuple[int, int]) -> ndarray[int, int]:
        return self._bins[index]
    # End of method

    def __setitem__(self, index, newValue):
        self._bins[index] = newValue
    # End of method

    @property
    def size(self) -> tuple[int, int]:
        "Size of bins array"
        return self._size
    # End of method

    @property
    def bins(self) -> ndarray:
        "Bins array"
        return self._bins
    # End of method
# End of class


# Class Design
class Design:
    """
    A class representing the whole design

    Methods
    -------
    create_core(coreUtil, width, height, aspectRatio, xOffset, yOffset)

    create_bins(width, height)

    find_bin(coords)
    """

    _name: str = None
    """Name of the design"""
    _comments: str = None

    _core: Core = None
    """Design Core"""
    _bins: Bins = None
    """Routing Bins"""
    _elementBins: Bins = None

    _isRouted: bool = None

    def __init__(self, name:str, comments:str) -> None:
        self._name = name
        self._comments = comments
        self._isRouted = False
    # End of method

    def __repr__(self) -> str:
        repr = f"Design: {self._name}\n{self._comments}\n{self.core}\n"
        if self._bins:
            repr += f"{self._bins}"
        else:
            repr += f"No bins"
        return repr
    # End of method

    @property
    def name(self):
        """Returns the design name"""
        return self._name
    # End of method
    
    @property
    def core(self) -> Core:
        return self._core
    # End of method
    
    @property
    def bins(self) -> Bins:
        return self._bins
    # End of method
    
    @property
    def elementBins(self) -> Bins:
        return self._elementBins
    # End of method
    
    @property
    def isRouted(self) -> bool:
        return self._isRouted
    # End of method

    @isRouted.setter
    def isRouted(self, isRouted) -> None:
        self._isRouted = isRouted
    # End of method

    def create_core(self, coreUtil: int, width: float, height: float,
                    aspectRatio: float, xOffset: float, yOffset: float) -> None:
        """Creates a core with the given specifications"""
        self._core = Core(coreUtil, width, height,
                          aspectRatio, xOffset, yOffset)
    # End of method

    def create_bins(self, width:int, height:int) -> None:
        """Creates an array of bins with the given dimentions"""
        self._bins = Bins(width, height)
        self._elementBins = Bins(width, height)
        self._update_bins()
        self._isRouted = False
    # End of method

    def remove_bins(self):
        del self.bins
        del self.elementBins
        self.isRouted = False

    def _update_bins(self):
        binsSize = self._bins.size
        binWidth = (self._core.width + 2 *self._core.x_offset) / binsSize[0]
        binHeight = (self._core.height + 2 * self._core.y_offset) / binsSize[1]

        # For the IO Ports
        for port in self._core.ioPorts:
            x,y = port.get_coordinates()
            bin = (int(y/binHeight), int(x/binWidth))
            port.bin = bin
            self._elementBins[bin] += 1
        # For the Components
        for comp in self._core.components:
            x,y = comp.get_coordinates()
            w,h = comp.get_dimentions()
            bin = (int((y + h/2)/binHeight), int((x + w/2)/binWidth))
            comp.bin = bin
            self._elementBins[bin] += 1
    # End of method
    
    def find_bin(self, coords:tuple[float, float]):
        binsSize = self._bins.size
        binWidth = (self._core.width + 2 *self._core.x_offset) / binsSize[0]
        binHeight = (self._core.height + 2 * self._core.y_offset) / binsSize[1]

        return (int(coords[1]/binHeight), int(coords[0]/binWidth))
    # End of method
# End of class


def get_center_coordinates(
        point:(IOPort|Component|NetPoint)) -> tuple[float,float]:
    """
    Gets the coordinates of the point or its center, 
    if the point is a components
    """

    if (point.__class__.__name__ == "Component"):
        px, py = point.get_center()
    else:
        px, py = point.get_coordinates()

    return px, py
# End of function