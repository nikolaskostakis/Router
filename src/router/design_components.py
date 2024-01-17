from typing import List

class BaseDesignElement:
    """Base class used for a design element"""

    _name: str = None
    """Name of design element"""
    _x: float = None
    """X Coordinate"""
    _y: float = None
    """Y Coordinate"""

    def __init__(self, name: str, x: float, y: float) -> None:
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

class RectangleDesignElement(BaseDesignElement):
    """Base class used for design elements with rectangular shape"""

    _width: float = None
    """Widht of the design element"""
    _height: float = None
    """ Height of the design element"""

    def __init__(self, name: str, x: float, y: float,
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

# Class Row
class Row(RectangleDesignElement):
    """A class used to represent a row of the design"""

    # private data
    _type: str = None     
    """ Row type """

    def __init__(self, name: str, type: str, x: float, y: float,
                 width: float, height: float) -> None:
        super().__init__(name, x, y, width, height)
        self._type = type 

    def __repr__(self) -> None:
        return "Row: %s Type: %s Location: %.3f %.3f Width/Height: %.3f %.3f" \
            % (self._name, self._type, self._x, self._y,
               self._width, self._height)

    def __str__(self) -> None:
        return "Row: %s Type: %s Location: %.3f %.3f Width/Height: %.3f %.3f" \
            % (self._name, self._type, self._x, self._y,
               self._width, self._height)

# Class IOPort
class IOPort(BaseDesignElement):
    """A class used to represent an I/O port of the design"""

    # Private data
    _side: str = None
    """Side of the core where port is"""

    def __init__(self, name: str, x: float, y: float, side: str) -> None:
        super().__init__(name, x, y)
        self._side = side

    def __repr__(self) -> None:
        return "IO: %s Location: %.3f %.3f %s SIDE" \
                % (self._name, self._x, self._y, self._side)

    def __str__(self) -> None:
        return "IO: %s Location: %.3f %.3f %s SIDE" \
                % (self._name, self._x, self._y, self._side)


# Class Component
class Component(RectangleDesignElement):
    """A class used to represent a component of the design"""

    def __init__(self, name: str) -> None:
        super().__init__(name, 0, 0, 1.26, 0.575)

    def __repr__(self) -> None:
        return "Component: %s " % (self._name)

    def __str__(self) -> None:
        return "Component: %s " % (self._name)


# Class Net
class Net:
    """
    A Class used to represent a net of the design
    """

    __name: str = None

    __source: (IOPort | Component)= None
    __drain: (IOPort | Component) = []

    def __init__(self, name: str, source: (IOPort | Component), drain):
        self.__name = name
        self.__source = source
        self.__drain = drain

    def __str__(self):
        pstr = "Net: %s Source: %s Drain: " % (self.__name, self.__source)
        pstr += ' '.join(map(str, self.__drain))
        return pstr

    def get_name(self):
        """Returns the name of the Net"""
        return self.__name

# Class Core
class Core:
    """
    A class used to represent a core of the design 

    Methods
    -------
    add_row(newRow)
    noof_rows()
    add_IO_port(newIOPort)
    get_IO_port(name)
    noof_IO_ports()
    add_component(newComponent)
    get_component(name)
    noof_IO_components()
    """

    __coreUtil: int = None
    __width: float = None
    __height: float = None
    __aspectRatio: float = None
    __xOffset: float = None
    __yOffset: float = None

    __rows: List[Row] = []
    __ioPorts: List[IOPort] = []
    __components: List[Component] = []
    __nets: List[Net] = []

    def __init__(self, coreUtil: int, width: float, height: float,
                 aspectRatio: float, xOffset: float, yOffset: float):
        self.__coreUtil = coreUtil
        self.__width = width
        self.__height = height
        self.__aspectRatio = aspectRatio
        self.__xOffset = xOffset
        self.__yOffset = yOffset

    def __repr__(self):
        return "Core Utilisation: %2d%%\n" \
            "Core Width, Height: %.3f, %.3f, Aspect Ratio: %.3f\n" \
            "Core X, Y Offsets: %.3f, %.3f" \
            % (self.__coreUtil, self.__width, self.__height,
               self.__aspectRatio, self.__xOffset, self.__yOffset)

    def __str__(self):
        return "Core Utilisation: %2d%%\n" \
            "Core Width, Height: %.3f, %.3f, Aspect Ratio: %.3f\n" \
            "Core X, Y Offsets: %.3f, %.3f" \
            % (self.__coreUtil, self.__width, self.__height,
               self.__aspectRatio, self.__xOffset, self.__yOffset)

    # Offsets
    def get_x_offset(self):
        return self.__xOffset
    
    def get_y_offset(self):
        return self.__yOffset

    # Dimensions
    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_dimentions(self):
        return self.__width, self.__height

    # Rows
    def add_row(self, newRow: Row):
        # Check if the the new row is object of class Row
        if (not isinstance(newRow, Row)):
            raise TypeError("Object is not a Row")

        self.__rows.append(newRow)

    def get_row(self, index: int):
        if (index < len(self.__rows)):
            return self.__rows[index]
        else:
            return None

    def noof_rows(self):
        return len(self.__rows)

    # I/O ports
    def add_IO_port(self, newIOPort: IOPort):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newIOPort, IOPort)):
            raise TypeError("Object is not an I/O Port")

        self.__ioPorts.append(newIOPort)

    def get_IO_port(self, name:str=None, index:int=None) -> (IOPort|None):
        if (index == None):
            for port in self.__ioPorts:
                if (port.name == name):
                    return port
        else:
            if (index < len(self.__ioPorts)):
                return self.__ioPorts[index]

        return None

    def noof_IO_ports(self):
        return len(self.__ioPorts)
    
    # Components
    def add_component(self, newComponent: Component):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newComponent, Component)):
            raise TypeError("Object is not a Component")

        #print(newComponent)
        self.__components.append(newComponent)

    def get_component(self, name:str=None, index:int=None) -> (Component|None):
        if (index == None):
            for comp in self.__components:
                if (comp.name == name):
                    return comp
        else:
            if (index < len(self.__components)):
                return self.__components[index]
        
        return None

    def noof_components(self):
        return len(self.__components)

    # Nets
    def add_net(self, newNet: Net):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newNet, Net)):
            raise TypeError("Object is not a Net")

        #print(newNet)
        self.__nets.append(newNet)

    def get_net(self, name: str) -> (Net | None):
        for net in self.__components:
            if (net.get_name() == name):
                return net
        
        return None

    def noof_nets(self):
        return len(self.__nets)

# Class Design
class Design:
    """
    A class representing the whole design

    Methods
    set_name(name)
    get_name()
    create_core(coreUtil, width, height, aspectRatio, xOffset, yOffset)
    """

    __name: str = None
    __core: Core = None

    def set_name(self, name: str):
        """
        Sets the name of the design
        """
        self.__name = name

    def get_name(self):
        """
        Returns the design name
        """
        return self.__name
    
    @property
    def core(self):
        return self.__core

    def create_core(self, coreUtil: int, width: float, height: float,
                    aspectRatio: float, xOffset: float, yOffset: float):
        """
        Creates a core with the given specifications
        """
        self.__core = Core(coreUtil, width, height, aspectRatio, xOffset, yOffset)