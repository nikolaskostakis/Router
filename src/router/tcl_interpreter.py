import readline
from tkinter import TclError
from tkinter import Tcl

from structures.design_components import Design
from gui import GUI
from file_io.parsers import practical_format_parcer
from file_io.parsers import components_location_parser
from file_io.writers import write_component_positions
from place_and_route.placement import random_placer
from place_and_route.routing import maze_routing

# Class TclInterpreter
class TclInterpreter:
    """
    Tcl Interpreter

    Methods
    -------
    interpreter()

    """

    _commands = [
        # Tcl Commands
        "break", "cd", " for", "foreach", "if", 
        "puts", "pwd", "return", "set", "while",
        # Readline
        "history",
        # Custom commands
        "quit",
        # Design
        "list_components", "list_io_ports", "list_nets", "list_rows",
        "load_design", "read_design", "remove_design", "save_design",
        "load_components","save_components",
        # Bins
        "bins_info", "create_bins", "remove_bins",
        # Placement
        "place_random",
        # Routing
        "maze_routing"
        # GUI
        "start_gui",
        # Testing
        "test"
        ]

    _tcl = None

    _design: Design = None
    _gui: GUI = None

    def __init__(self):
        self._commands.sort()
        self.__initialize_interpreter()
        self.__create_Tcl_commands()
    # End of method

    def __print_red(self, msg): print(f"\x1B[31m{msg}\x1B[0m")
    def __print_yellow(self, msg): print(f"\x1B[33m{msg}\x1B[0m")

    # Interpreter initialization
    def __initialize_interpreter(self):
        self._tcl = Tcl()

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.__completer)
    # End of method

    # Tcl Command creation
    def __create_Tcl_commands(self):
        self._tcl.createcommand("bins_info", self._bins_info)
        self._tcl.createcommand("create_bins", self._create_bins)
        self._tcl.createcommand("list_components", self._list_components)
        self._tcl.createcommand("list_io_ports", self._list_io_ports)
        self._tcl.createcommand("list_nets", self._list_nets)
        self._tcl.createcommand("list_rows", self._list_rows)
        self._tcl.createcommand("load_design", self.__load_design)
        self._tcl.createcommand("load_components", self.__load_components)
        self._tcl.createcommand("maze_routing", self._maze_routing)
        self._tcl.createcommand("place_random", self.__place_random)
        self._tcl.createcommand("read_design", self.__read_design)
        self._tcl.createcommand("remove_bins", self._remove_bins)
        self._tcl.createcommand("remove_design", self._remove_design)
        self._tcl.createcommand("save_design", self.__save_design)
        self._tcl.createcommand("save_components", self.__save_components)
        self._tcl.createcommand("start_gui", self.__start_gui)
        self._tcl.createcommand("test", self._test)
    # End of method

    # Completer
    def __completer(self, text, state):
        # TODO: Expand completer with files and command flags (optional)
        results = [x for x in self._commands if x.startswith(text)] + [None]
        return results[state]
    # End of method

    # Tcl Commands
    def _bins_info(self):
        if not self._design.bins:
            print("There are no bins created")
        else:
            print(self._design.bins)
    # End of method

    def _create_bins(self, *args):
        commandFormat = "create_bins [-h | -size width height]"
        commandDescription = "Creates aray of bins with given dimentions"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return
        elif ((len(args) == 3) & (args[0] == "-size")):
            if self._design.bins:
                print("There are already bins created")
                return

            try:
                width = int(args[1])
                height = int(args[2])
            except ValueError:
                print("Dimentions for bins are ment to be integers")
                raise TclError
            
            self._design.create_bins(width, height)
            self._design.update_bins()
        else:
            raise TclError
    # End of method

    def _list_components(self, *args):
        if not self._design:
            print("There is no design")
            return
        
        for comp in self._design.core.components:
            print(comp)
    # End of method

    def _list_io_ports(self, *args):
        if not self._design:
            print("There is no design")
            return
        
        for ioPort in self._design.core.ioPorts:
            print(ioPort)
    # End of method

    def _list_nets(self, *args):
        if not self._design:
            print("There is no design")
            return
        
        for net in self._design.core.nets:
            print(net)
    # End of method

    def _list_rows(self, *args):
        if not self._design:
            print("There is no design")
            return
        
        for row in self._design.core.rows:
            print(row)
    # End of method

    def __load_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for loading design used on previous run")
    # End of method

    def __load_components(self, *args):
        commandFormat = "load_components [-h | -f file]"
        commandDescription = "Loads component positions from given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            if not self._design:
                print("There is no design loaded")
                return

            try:
                with open(args[1], "r") as file:
                    success = components_location_parser(file, self._design)
            except IOError:
                print("There is no file: %s" % (args[1]))
            
            if not success: print("Failure")
            else: print("Success")
        else:
            raise TclError
    # End of method

    def _maze_routing(self):
        if not self._design:
            print("There is no design loaded")
            return

        if not self._design.bins:
            print("There are no bins for routing to be done")
            return

        maze_routing(self._design)
    # End of method

    def __place_random(self, *args):
        res = random_placer(self._design.core)
        if res:
            print("Success")
        else:
            print("Failure")
    # End of method

    def __read_design(self, *args):
        commandFormat = "read_design [-h | -f file]"
        commandDescription = "Reads design from given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            if self._design:
                print("Design is already loaded")
                return

            try:
                with open(args[1], "r") as file:
                    newDesign = practical_format_parcer(file)
            except IOError:
                print("There is no file: %s" % (args[1]))
            
            if not newDesign:
                print("Failure")
            else:
                self._design = newDesign
                print("Success")
        else:
            raise TclError
    # End of method

    def _remove_bins(self):
        if (self._design.bins != None):
            del self._design.bins
            print("Bins Removed")
        else:
            print("There are no bins to be removed")

    def _remove_design(self):
        if (self._design != None):
            del self._design
            print("Design Removed")
        else:
            print("There is no design to be removed")
    # End of method

    def __save_design(self, *args):
        self.__print_yellow("Under Construction")
        print("To be used for saving design for future runs")
    # End of method

    def __save_components(self, *args):
        commandFormat = "save_components [-h | -f file]"
        commandDescription = "Saves component positions to given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            if not self._design:
                print("Design is not loaded")
                return

            with open(args[1], "w") as file:
                write_component_positions(file, self._design.name,
                                        self._design.core.components)
        else:
            raise TclError
    # End of method

    def __start_gui(self):
        self._gui = GUI("Router", self._design)

        self._gui.mainloop()
    # End of method

    def _test(self, *args):
        """Tcl command used for testing features"""

        print("Hello")

        #net = self._design.core.get_net(args[0])
        #if not net:
        #    print("Use valid name")
        #    raise TclError
        #for net in self._design.core.nets:
        #    self._bins.maze_routing(net)
        maze_routing(self._design)
    # End of method

    # Interpreter
    def interpreter(self):
        """Interpreter"""

        while (True):
            line = input("\x1B[36mprompt> \x1B[0m")
            if (line == "quit"):
                print("Goodbye!")
                break
            # Readline history, not the Tcl Command
            elif (line == "history"):
                readline.add_history(line)
                for i in range(readline.get_current_history_length()):
                    print(readline.get_history_item(i))
            
            # Evaluate the command
            try:
                self._tcl.eval(line)
            except TclError:
                self.__print_red("Invalid Tcl command or options on one")

            readline.add_history(line)
        self._test()
        self._bins_info()
    # End of method

    # For Design
    def set_design(self, newDesign: Design):
        if (not isinstance(newDesign, Design)):
            raise TypeError("Object is not a Design")
        
        self._design = newDesign
    
    def get_design(self) -> (Design | None):
        return self._design