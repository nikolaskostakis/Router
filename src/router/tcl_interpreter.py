import readline
from tkinter import TclError
from tkinter import Tcl
from parsers import PracticalFormatParser

# Class TclInterpreter
class TclInterpreter:
    """
    Tcl Interpreter

    Methods
    -------
    interpreter()

    """

    __commands = [
        "break", "cd", " for", "foreach", "history", "if", "load_design",
        "puts", "pwd", "quit", "read_design", "return", "save_design",
        "set", "while"
        ]

    __tcl = None

    def __init__(self):
        None

    def __print_red(self, msg): print("\x1B[31m" + msg + "\x1B[0m")
    def __print_yellow(self, msg): print("\x1B[33m" + msg + "\x1B[0m")

    # Interpreter initialization
    def __initialize_interpreter(self):
        self.__tcl = Tcl()

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.__completer)

    def __create_Tcl_commands(self):
        self.__tcl.createcommand("load_design", self.__load_design)   
        self.__tcl.createcommand("read_design", self.__read_design)   
        self.__tcl.createcommand("save_design", self.__save_design)    

    # Completer
    def __completer(self, text, state):
        # TODO: Expand completer with files and command flags (optional)
        results = [x for x in self.__commands if x.startswith(text)] + [None]
        return results[state]

    # Tcl Commands
    def __load_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for loading design used on previous run")

    def __read_design(self, *args):
        commandFormat = "read_design [-h | -f file]"
        commandDescription = "Reads design from given file"
        
        if ((len(args) == 1) & (args[0] == "-h")):
            print(commandFormat + "\n" + commandDescription)
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            print(args[1])
            pFP = PracticalFormatParser()
            file = open(args[1], "r")
            design = pFP.parse_file(file)
        else:
            raise TclError

    def __save_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for saving design for future runs")

    def interpreter(self):
        self.__initialize_interpreter()
        self.__create_Tcl_commands()

        while (True):
            line = input('prompt> ')
            if (line == 'quit'):
                print("Goodbye!")
                quit()
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
