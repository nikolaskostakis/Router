# Class Row
class Row:
    """
    A class used to represent a row of the core

    Methods
    -------
    getName : str
        Returns the name of the row
    getXCoordinate : float
        Returns the x-coordinate of the row's top left corner 
    getYCoordinate : float
        Returns the y-coordinate of the row's top left corner
    getCoordinates : float , float
        Returns the coordinates (x,y) of the row's top left corner
    getWidth : float
        Returns the width of the row 
    getHeight : float
        Returns the height of the row
    getDimentions : float , float
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

    def getName(self):
        """Returns the name of the row"""
        return self.__name

    # Coordinate
    def getXCoordinate(self):
        """Returns the x-coordinate of the row's top left corner"""
        return self.__xPos

    def getYCoordinate(self):
        """Returns the y-coordinate of the row's top left corner"""
        return self.__xPos

    def getCoordinates(self):
        """Returns the coordinates (x,y) of the row's top left corner"""
        return self.__xPos, self.__yPos

    # Dimensions
    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getDimentions(self):
        return self.__width, self.__height


# Class IOPort
class IOPort:
    """
    A class used to represent an I/O port of the core

    Methods
    -------
    getName : str
        Returns the name of the I/O port
    getXCoordinate : float
        Returns the x-coordinate of the I/O port 
    getYCoordinate : float
        Returns the y-coordinate of the I/O port
    getCoordinates : float , float
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
        return "IO: %s Location: %.3f %.3f %s" % (self.__name, self.__xPos, self.__yPos, self.__side)

    def __str__(self):
        return "IO: %s Location: %.3f %.3f %s" % (self.__name, self.__xPos, self.__yPos, self.__side)

    def getName(self):
        """Returns the name of the I/O port"""
        return self.__name

    # Coordinate
    def getXCoordinate(self):
        return self.__xPos

    def getYCoordinate(self):
        return self.__xPos

    def getCoordinates(self):
        return self.__xPos, self.__yPos


# Class Core
class Core:
    """
    A class used to represent the design core
    """

    __coreUtil = None
    __width = None
    __height = None
    __aspectRatio = None
    __xOffset = None
    __yOffset = None

    __rows = []
    __ioPorts = []

    def __init__(self, coreUtil, width, height, aspectRatio, xOffset, yOffset):
        self.__coreUtil = int(coreUtil)
        self.__width = float(width)
        self.__height = float(height)
        self.__aspectRatio = float(aspectRatio)
        self.__xOffset = float(xOffset)
        self.__yOffset = float(yOffset)

    def __repr__(self):
        return " Core Utilisation: %2d\%\n" \
            "Core Width, Height: %.3f, %.3f, Aspect Ratio: %.3f\n" \
            "Core X, Y Offsets: %.3f, %.3f" \
            % (self.__coreUtil, self.__width, self.__height,
               self.__aspectRatio, self.__xOffset, self.__yOffset)

    # Rows
    def addRow(self, newRow):
        # Check if the the new row is object of class Row
        if (not isinstance(newRow, Row)):
            raise TypeError("Object is not a Row")

        self.__rows.append(newRow)

    def noofRows(self):
        return len(self.__rows)

    # I/O ports
    def addIOPort(self, newIOPort):
        # Check if the the new I/O port is object of class IOPort
        if (not isinstance(newIOPort, IOPort)):
            raise TypeError("Object is not an I/O Port")

        self.__ioPorts.append(newIOPort)

    def noofIOPorts(self):
        return len(self.__ioPorts)