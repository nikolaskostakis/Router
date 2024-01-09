import readline
import tkinter
from tkinter import Tcl
from parsers import PracticalFormatParser

# Class TclInterpreter
class TclInterpreter:
    """

    Methods
    -------

    """

    __commands = [
        "break", "cd", "exit", " for", "foreach", "if",
        "load_design",
        "puts", "pwd", "quit", "return", "set", "while"
        ]

    __tcl = None

    def __init__(self):
        None
    
    def __completer(self, text, state):
        results = [x for x in self.__commands if x.startswith(text)] + [None]
        return results[state]
    
    def __load_design(self, *args):
        print(args)
        print(len(args))
        #if (len(args) != 1):
        #    return tkinter.TclError
        
        pFP = PracticalFormatParser()
        file = open("benchmarks\counter7.txt", 'r')
        design = pFP.parse_file(file)
        print(design.core)


    def interpreter(self):
        self.__tcl = Tcl()

        self.__tcl.createcommand("load_design", self.__load_design)
        readline.parse_and_bind("tab: complete")

        readline.set_completer(self.__completer)

        while (True):
            line = input('prompt> ')
            print(line)
            if ((line == 'quit') | (line == 'exit')):
                print("Goodbye!")
                quit()
            self.__tcl.eval(line)
