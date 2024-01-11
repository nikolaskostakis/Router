import re
from io import TextIOWrapper
from design_components import *

class PracticalFormatParser:
    """
    A parser for files written based on the practical format
    """

    # The states of the parser
    __states = ["State1", "State2", "State3", "State4", "State5", "State6"]
    __statesDelimiter = "###############################################################\n"
    __design = None

    def __init__(self):
        None
    
    def __state_one(self, file):
        """
        First state of the parser
        """
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        splits = line.split(' ')
        self.__design.set_name(splits[2])

    def __state_two(self, file):
        """
        Second state of the parser
        """
        line = file.readline()

        line = file.readline()
        splits = re.split(" |\n", line)
        util = int(splits[3].replace('%',''))

        line = file.readline()
        splits = re.split(" |, |\n", line)
        width = float(splits[4])
        height = float(splits[5])
        ratio = float(splits[8])
        
        line = file.readline()
        splits = re.split(" |, |\n", line)
        xOffset = float(splits[5])
        yOffset = float(splits[6])

        self.__design.create_core(util, width, height, ratio, xOffset, yOffset)

    def __state_three(self, file):
        """
        Third state of the parser
        """
        line = file.readline()
        line = file.readline()
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break

            splits = re.split(" |\n", line)
            name = splits[1]
            type = splits[3]
            xPos = float(splits[5])
            yPos = float(splits[6])
            width = float(splits[8])
            height = float(splits[9])
            newRow = Row(name, type, xPos, yPos, width, height)
            self.__design.core.add_row(newRow)
            line = file.readline()

    def __state_four(self, file):
        """
        Fourth state of the parser
        """
        line = file.readline()
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break

            splits = re.split(" |\n", line)
            name = splits[1]
            xPos = float(splits[3])
            yPos = float(splits[4])

            line = file.readline()
            splits = re.split(" |\n", line)
            side = splits[1]

            newIOPort = IOPort(name, xPos, yPos, side)
            self.__design.core.add_IO_port(newIOPort)
            line = file.readline()

    def __create_component(self, name: str):
        # Check  if component exists
        newComponent: Component = self.__design.core.get_component(name)
        if (not newComponent):
            # If component does not exist
            # Crate new component
            newComponent = Component(name)

            # Add new component to the design
            self.__design.core.add_component(newComponent)

        return newComponent

    def __create_net(self, source, components):
        name = "N%d" % (self.__design.core.noof_nets() + 1)
        newDrain = []
        for comp in components:
            # Add component to the list of endpoints of the net
            newComp = self.__create_component(comp)
            newDrain.append(newComp)
        
        # Add new net to the design
        return Net(name, source, newDrain)

    def __state_five(self, file):
        """
        Fifth state of the parser
        """
        line = file.readline()
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break

            splits = re.split(" ", line)

            source = self.__design.core.get_IO_port(splits[1])
            newNet = self.__create_net(source, splits[3:(len(splits) - 1)])
            self.__design.core.add_net(newNet)

            line = file.readline()

    def __state_six(self, file):
        """
        Sixth state of the parser
        """
        line = file.readline()
        line = file.readline()
        while True:
            if (not line):
                break
        
            splits = re.split(" ", line)
            name = splits[1]
            
            source = self.__create_component(name)
            newNet = self.__create_net(source, splits[3:(len(splits) - 1)])
            self.__design.core.add_net(newNet)

            line = file.readline()

    def parse_file(self, file: TextIOWrapper):
        """
        Parses the file and returns the design
        """

        # Create new design
        self.__design = Design()

        # Parse file 
        for state in self.__states:
            match state:
                case "State1": self.__state_one(file)
                case "State2": self.__state_two(file)
                case "State3": self.__state_three(file)
                case "State4": self.__state_four(file)
                case "State5": self.__state_five(file)
                case "State6": self.__state_six(file)
            
        return self.__design