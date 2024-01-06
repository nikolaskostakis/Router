import re
from design_components import *

class PracticalFormatParser:
    """
    A parser for files written based on the practical format
    """

    __states = ["State1", "State2", "State3", "State4", "State5", "State6"]
    __statesDelimiter = "###############################################################\n"
    __design = None

    def __init__(self):
        None
    
    def __state_one(self, file):
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        splits = line.split(' ')
        self.__design.add_name(splits[2])

    def __state_two(self, file):
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
        line = file.readline()
        line = file.readline()
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break

            splits = re.split(" |\n", line)
            name = splits[1]
            type = splits[3]
            xPos = splits[5]
            yPos = splits[6]
            width = splits[8]
            height = splits[9]
            newRow = Row(name, type, xPos, yPos, width, height)
            self.__design.core.add_row(newRow)
            line = file.readline()
        

    def __state_four(self, file):
        line = file.readline()
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break

            splits = re.split(" |\n", line)
            name = splits[1]
            xPos = splits[3]
            yPos = splits[4]

            line = file.readline()
            splits = re.split(" |\n", line)
            side = splits[1]

            newIOPort = IOPort(name, xPos, yPos, side)
            self.__design.core.add_IO_port(newIOPort)
            line = file.readline()

    def __state_five(self, file):
        line = file.readline()
        while True:
            if (line == self.__statesDelimiter):
                break
            line = file.readline()

    def __state_six(self, file):
        line = file.readline()
        line = file.readline()
        while True:
            if ((line == self.__statesDelimiter) | (not line)):
                break
        
            splits = re.split(" |\n", line)
            name = splits[1]
            newComponent = Component(name)
            self.__design.core.add_component(newComponent)
            line = file.readline()

    def parse_file(self, file):
        self.__design = Design()
        # Simple for loop to test the access to the files
        # for line in file:
        #      print(line)
        for state in self.__states:
            match state:
                case "State1": self.__state_one(file)
                case "State2": self.__state_two(file)
                case "State3": self.__state_three(file)
                case "State4": self.__state_four(file)
                case "State5": self.__state_five(file)
                case "State6": self.__state_six(file)

        # TODO: The actual Parser
            
        return self.__design