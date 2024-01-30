"""
Module housing the design components used for the router
"""

import numpy as np
from numpy import ndarray

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

    # Name
    @property
    def name(self) -> str:
        """Returns the name"""
        return self._name

    # Coordinates
    @property
    def x(self) -> float:
        """Returns x-coordinate"""
        return self._x

    @x.setter
    def x(self, newX:float) -> None:
        """Assign new x-coordinate"""
        self._x = newX

    @property
    def y(self) -> float:
        """Returns y-coordinate"""
        return self._y
    
    @y.setter
    def y(self, newY):
        self._y = newY

    def get_coordinates(self) -> tuple[float, float]:
        """Returns the coordinates (x,y)"""
        return self._x, self._y
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

    # Dimensions
    @property
    def width(self) -> float:
        """Returns width"""
        return self._width

    @property
    def height(self) -> float:
        """Returns heigh"""
        return self._height

    def get_dimentions(self) -> tuple[float, float]:
        """Returns dimentions (width, height)"""
        return self._width, self._height
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

    def __repr__(self) -> None:
        return "Row: %s Type: %s Location: %.3f %.3f Width/Height: %.3f %.3f" \
            % (self._name, self._type, self._x, self._y,
               self._width, self._height)
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

    def __repr__(self) -> None:
        repr_str = f"IO: {self._name} Location: {self._x:.3f} {self._y:.3f}" \
                   f" {self._side} SIDE" 
        if self._bin:
            repr_str += f" Bin: {self._bin}"
        return repr_str
    
    @property
    def bin(self) -> tuple[int, int]:
        """"""
        return self._bin
    
    @bin.setter
    def bin(self, newBin) -> None:
        self._bin = newBin
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

    def __repr__(self) -> None:
        rep_str = f"Component: {self.name} Cell_Type: {self._type} " \
                  f"Cell_Timing_Type: {self._timingType} " \
                  f"Location: {self._x:.3f} {self._y:.3f}"
        if self._bin:
            rep_str += f" Bin: {self._bin}"
        return rep_str
    
    @property
    def bin(self) -> tuple[int, int]:
        """"""
        return self._bin
    
    @bin.setter
    def bin(self, newBin) -> None:
        self._bin = newBin
# End of class


# Class Net
class Net:
    """
    A Class used to represent a net of the design
    """

    _name: str = None

    _source: (IOPort | Component)= None
    _drain: list[IOPort | Component] = []

    def __init__(self, name:str, source:(IOPort|Component),
                 drain:list[IOPort|Component]):
        self._name = name
        self._source = source
        self._drain = drain

    def __repr__(self):
        drain = " ".join([d.name for d in self._drain])
        rep_str = f"Net: {self._name} Source: {self._source.name}" \
                  f" Drain: {drain}"
        return rep_str

    # Name
    @property
    def name(self) -> str:
        """Returns the name"""
        return self._name

    @property
    def source(self):
        return self._source

    @property
    def drain(self):
        return self._drain
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

    def __repr__(self):
        return "Core Utilisation: %2d%%\n" \
            "Core Width, Height: %.3f, %.3f, Aspect Ratio: %.3f\n" \
            "Core X, Y Offsets: %.3f, %.3f" \
            % (self._coreUtil, self._width, self._height,
               self._aspectRatio, self._xOffset, self._yOffset)

    # Offsets
    @property
    def x_offset(self) -> float:
        return self._xOffset
    
    @property
    def y_offset(self) -> float:
        return self._yOffset

    # Rows
    @property
    def rows(self) -> list[Row]:
        return self._rows

    def add_row(self, newRow: Row) -> None:
        # Check if the the new row is object of class Row
        if (not isinstance(newRow, Row)):
            raise TypeError("Object is not a Row")

        self._rows.append(newRow)

    def noof_rows(self) -> int:
        return len(self._rows)

    # I/O ports
    @property
    def ioPorts(self) -> list[IOPort]:
        return self._ioParts

    def add_IO_port(self, newIOPort: IOPort) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newIOPort, IOPort)):
            raise TypeError("Object is not an I/O Port")

        self._ioParts.append(newIOPort)

    def get_IO_port(self, name:str=None) -> (IOPort|None):
        """Returns IO Port with given name"""
        if not self._ioParts:
            return None

        for port in self._ioParts:
            if (port.name == name):
                return port

        return None

    def noof_IO_ports(self) -> int:
        return len(self._ioParts)
    
    # Components
    @property
    def components(self) -> list[Component]:
        return self._components

    def add_component(self, newComponent: Component) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newComponent, Component)):
            raise TypeError("Object is not a Component")

        #print(newComponent)
        self._components.append(newComponent)

    def get_component(self, name:str=None) -> (Component|None):
        """Returns Component with given name"""
        if not self._components:
            return None

        for comp in self._components:
            if (comp.name == name):
                return comp

        return None

    def noof_components(self) -> int:
        return len(self._components)

    # Nets
    @property
    def nets(self) -> list[Net]:
        return self._nets

    def add_net(self, newNet: Net) -> None:
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newNet, Net)):
            raise TypeError("Object is not a Net")

        #print(newNet)
        self._nets.append(newNet)

    def get_net(self, name: str) -> (Net | None):
        """Returns Net with given name"""
        if not self._nets:
            return None

        for net in self._nets:
            if (net.name == name):
                return net
        
        return None

    def noof_nets(self) -> int:
        return len(self._nets)
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

    def __repr__(self) -> str:
        return f"Bins {self.size}:\n{self._bins}"
    
    def __getitem__(self, index: tuple[int, int]) -> ndarray[int, int]:
        return self._bins[index]

    def __setitem__(self, index, newValue):
        self._bins[index] = newValue

    @property
    def size(self) -> tuple[int, int]:
        "Size of bins array"
        return self._size

    @property
    def bins(self) -> ndarray:
        "Bins array"
        return self._bins
# End of class


# Class Design
class Design:
    """
    A class representing the whole design

    Methods
    set_name(name)
    get_name()
    create_core(coreUtil, width, height, aspectRatio, xOffset, yOffset)
    """

    _name: str = None
    """Name of the design"""
    _comments: str = None

    _core: Core = None
    """Design Core"""
    _bins: Bins = None
    """Routing Bins"""

    def __init__(self, name:str, comments:str) -> None:
        self._name = name
        self._comments = comments

    @property
    def name(self):
        """Returns the design name"""
        return self._name
    
    @property
    def core(self) -> Core:
        return self._core
    
    @property
    def bins(self) -> Bins:
        return self._bins

    @bins.deleter
    def bins(self) -> None:
        del self._bins

    def create_core(self, coreUtil: int, width: float, height: float,
                    aspectRatio: float, xOffset: float, yOffset: float) -> None:
        """Creates a core with the given specifications"""
        self._core = Core(coreUtil, width, height,
                          aspectRatio, xOffset, yOffset)

    def create_bins(self, width:int, height:int) -> None:
        """Creates an array of bins with the given dimentions"""
        self._bins = Bins(width, height)

    def update_bins(self):
        binsSize = self._bins.size
        binWidth = (self._core.width + 2 *self._core.x_offset) / binsSize[0]
        binHeight = (self._core.height + 2 * self._core.y_offset) / binsSize[1]

        # For the IO Ports
        for port in self._core.ioPorts:
            x,y = port.get_coordinates()
            bin = (int(y/binHeight), int(x/binWidth))
            port.bin = bin
        # For the Components
        for comp in self._core.components:
            x,y = comp.get_coordinates()
            w,h = comp.get_dimentions()
            bin = (int((y + h/2)/binHeight), int((x + w/2)/binWidth))
            comp.bin = bin
# End of class