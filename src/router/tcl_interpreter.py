import readline
from tkinter import TclError
from tkinter import Tcl

from design_components import Design
from gui import GUI
from parsers import praactical_format_parcer
from placement import random_placer

# Class TclInterpreter
class TclInterpreter:
    """
    Tcl Interpreter

    Methods
    -------
    interpreter()

    """

    __commands = [
        # Tcl Commands
        "break", "cd", " for", "foreach", "if", 
        "puts", "pwd", "return", "set", "while",
        # Readline
        "history",
        # Custom commands
        "list_components", "list_io_ports", "list_rows",
        "load_design", "place_random", "quit", "read_design",
        "remove_design", "save_design", "start_gui"
        ]

    __tcl = None

    __design: Design = None
    __gui: GUI = None

    def __init__(self):
        self.__commands.sort()
        None

    def __print_red(self, msg): print("\x1B[31m" + msg + "\x1B[0m")
    def __print_yellow(self, msg): print("\x1B[33m" + msg + "\x1B[0m")

    # Interpreter initialization
    def __initialize_interpreter(self):
        self.__tcl = Tcl()

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.__completer)

    def __create_Tcl_commands(self):
        self.__tcl.createcommand("list_components", self.__list_components)
        self.__tcl.createcommand("list_io_ports", self.__list_io_ports)
        self.__tcl.createcommand("list_rows", self.__list_rows)
        self.__tcl.createcommand("load_design", self.__load_design)
        self.__tcl.createcommand("place_random", self.__place_random)
        self.__tcl.createcommand("read_design", self.__read_design)
        self.__tcl.createcommand("remove_design", self.__remove_design)
        self.__tcl.createcommand("save_design", self.__save_design)
        self.__tcl.createcommand("start_gui", self.__start_gui)

    # Completer
    def __completer(self, text, state):
        # TODO: Expand completer with files and command flags (optional)
        results = [x for x in self.__commands if x.startswith(text)] + [None]
        return results[state]

    # Tcl Commands
    def __list_components(self, *args):
        if not self.__design:
            print("There is no design")
            return
        
        for comp in self.__design.core.components:
            print(comp)

    def __list_io_ports(self, *args):
        if not self.__design:
            print("There is no design")
            return
        
        for ioPort in self.__design.core.ioPorts:
            print(ioPort)

    def __list_rows(self, *args):
        if not self.__design:
            print("There is no design")
            return
        
        for row in self.__design.core.rows:
            print(row)

    def __load_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for loading design used on previous run")

    def __place_random(self, *args):
        res = random_placer(self.__design.core)
        if res:
            print("Success")
        else:
            print("Failure")

    def __read_design(self, *args):
        commandFormat = "read_design [-h | -f file]"
        commandDescription = "Reads design from given file"
        
        if ((len(args) == 1) & (args[0] == "-h")):
            print(commandFormat + "\n" + commandDescription)
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            if self.__design:
                print("Design is already loaded")
                return

            try:
                with open(args[1], "r") as file:
                    newDesign = praactical_format_parcer(file)
            except IOError:
                print("There is no file: %s" % (args[1]))
            
            if not newDesign:
                print("Failure")
            else:
                self.__design = newDesign
                print("Success")
        else:
            raise TclError

    def __remove_design(self):
        if (self.__design != None):
            del self.__design
            print("Design Removed")
        else:
            print("There is no design to be removed")

    def __save_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for saving design for future runs")

    def __start_gui(self):
        self.__gui = GUI("Router", self.__design)

        self.__gui.mainloop()
        None

    def interpreter(self):
        self.__initialize_interpreter()
        self.__create_Tcl_commands()

        while (True):
            line = input('prompt> ')
            if (line == 'quit'):
                print("Goodbye!")
                break
            # Readline history, not the Tcl Command
            elif (line == "history"):
                readline.add_history(line)
                for i in range(readline.get_current_history_length()):
                    print(readline.get_history_item(i))
            
            # Evaluate the command
            try:
                self.__tcl.eval(line)
            except TclError:
                self.__print_red("Invalid Tcl command or options on one")

            readline.add_history(line)


    # For Design
    def set_design(self, newDesign: Design):
        if (not isinstance(newDesign, Design)):
            raise TypeError("Object is not a Design")
        
        self.__design = newDesign
    
    def get_design(self) -> (Design | None):
        return self.__design