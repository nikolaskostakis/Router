# Class Row
class Row:
    """
    A class used to represent a row of the design

    Methods
    -------
    get_name()
        Returns the name of the row
    get_x_coordinate()
        Returns the x-coordinate of the row's top left corner 
    get_y_coordinate()
        Returns the y-coordinate of the row's top left corner
    get_coordinates()
        Returns the coordinates (x,y) of the row's top left corner
    get_width()
        Returns the width of the row 
    get_height()
        Returns the height of the row
    get_dimentions()
        Returns the dimentions (width, height) of the row
    """


    # private data
    __name = None   # Row's Name
    __type = None   # Row's type
    __xPos = None   # Row's top left x-coordinate
    __yPos = None   # Row's top left y-coordinate
    __width = None  # Row's width
    __height = None # Row's height

    def __init__(self, name, type, xPos, yPos, width, height):
        self.__name = name
        self.__type = type 
        self.__xPos = float(xPos)
        self.__yPos = float(yPos)
        self.__width = float(width)
        self.__height = float(height)

    def __repr__(self):
        return "Row: %s Type: %s " \
            "Location: %.3f %.3f " \
            "Width/Height: %.3f %.3f" \
            % (self.__name, self.__type, self.__xPos, self.__yPos, self.__width, self.__height)

    def __str__(self):
        return "Row: %s Type: %s " \
            "Location: %.3f %.3f " \
            "Width/Height: %.3f %.3f" \
            % (self.__name, self.__type, self.__xPos, self.__yPos, self.__width, self.__height)

    def get_name(self):
        """Returns the name of the row"""
        return self.__name

    # Coordinate
    def get_x_coordinate(self):
        """Returns the x-coordinate of the row's top left corner"""
        return self.__xPos

    def get_y_coordinate(self):
        """Returns the y-coordinate of the row's top left corner"""
        return self.__xPos

    def get_coordinates(self):
        """Returns the coordinates (x,y) of the row's top left corner"""
        return self.__xPos, self.__yPos

    # Dimensions
    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_dimentions(self):
        return self.__width, self.__height


# Class IOPort
class IOPort:
    """
    A class used to represent an I/O port of the design

    Methods
    -------
    get_name()
        Returns the name of the I/O port
    get_x_Coordinate()
        Returns the x-coordinate of the I/O port 
    get_y_Coordinate()
        Returns the y-coordinate of the I/O port
    get_coordinates()
        Returns the coordinates (x,y) of the I/O port
    """


    # Private data
    __name = None
    __xPos = None
    __yPos = None
    __side = None

    def __init__(self, name, xPos, yPos, side):
        self.__name = name
        self.__xPos = float(xPos)
        self.__yPos = float(yPos)
        self.__side = side

    def __repr__(self):
        return "IO: %s Location: %.3f %.3f %s SIDE" % (self.__name, self.__xPos, self.__yPos, self.__side)

    def __str__(self):
        return "IO: %s Location: %.3f %.3f %s SIDE" % (self.__name, self.__xPos, self.__yPos, self.__side)

    def get_name(self):
        """Returns the name of the I/O port"""
        return self.__name

    # Coordinate
    def get_x_Coordinate(self):
        return self.__xPos

    def get_y_Coordinate(self):
        return self.__xPos

    def get_coordinates(self):
        return self.__xPos, self.__yPos


# Class Component
class Component:
    """
    A class used to represent a component of the design
    """

    __name = None

    def __init__(self, name):
        self.__name = name

    def __repr__(self):
        return "Component: %s " % (self.__name)

    def __str__(self):
        return "Component: %s " % (self.__name)

# Class Core
class Core:
    """
    A class used to represent a core of the design 

    Methods
    -------
    add_row(newRow)
    noof_rows()
    add_IO_port(newIOPort)
    noof_IO_ports()
    """

    __coreUtil = None
    __width = None
    __height = None
    __aspectRatio = None
    __xOffset = None
    __yOffset = None

    __rows = []
    __ioPorts = []
    __components = []

    def __init__(self, coreUtil: int, width: float, height: float, aspectRatio: float, xOffset: float, yOffset: float):
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

    # Rows
    def add_row(self, newRow):
        # Check if the the new row is object of class Row
        if (not isinstance(newRow, Row)):
            raise TypeError("Object is not a Row")

        print(newRow)
        self.__rows.append(newRow)

    def noof_rows(self):
        return len(self.__rows)

    # I/O ports
    def add_IO_port(self, newIOPort):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newIOPort, IOPort)):
            raise TypeError("Object is not an I/O Port")

        print(newIOPort)
        self.__ioPorts.append(newIOPort)

    def noof_IO_ports(self):
        return len(self.__ioPorts)
    
    # Components
    def add_component(self, newComponent):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newComponent, Component)):
            raise TypeError("Object is not a Component")

        print(newComponent)
        self.__components.append(newComponent)

    def noof_components(self):
        return len(self.__components)


# Class Design
class Design:
    """
    A class representing the whole design
    """

    __name = None
    core = None

    def add_name(self, name: str):
        self.__name = name

    def create_core(self, coreUtil: int, width: float, height: float, aspectRatio: float, xOffset: float, yOffset: float):
        self.core = Core(coreUtil, width, height, aspectRatio, xOffset, yOffset)