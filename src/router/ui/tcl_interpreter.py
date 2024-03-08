"""
Module containing the TCL Interpreter
"""

import os
import logging

import readline
from tkinter import Tk, Tcl, TclError

import config
from structures.design_components import Design, Net
from structures.trees import print_generic_tree
from .gui import GUI
from file_io.parsers import practical_format_parcer, components_location_parser
from file_io.writers import write_component_positions
from place_and_route.placement import random_placer
from place_and_route.routing import maze_routing, calculate_tree_wirelength
from place_and_route.routing import calculate_HPWL, calculate_net_HPWL
from place_and_route.routing import calculate_net_tree_wirelength

# Logging
interfaceLogger = logging.getLogger(__name__)
interfaceLogger.setLevel(logging.DEBUG)
interfaceLogger.addHandler(config.consoleHandler)

# Colors
CYAN   = "\x1B[36m"
NORMAL = "\x1B[0m"
RED =    "\x1B[31m"
YELLOW = "\x1B[33m"

# Class TclInterpreter
class TclInterpreter:
    """
    Tcl Interpreter

    Methods
    -------
    - interpreter()
    - script_interpreter(script)
    """

    _commands = [
        # Tcl Commands
        "array", "break", "continue", "concat", "cd", "for", "foreach", "if", 
        "list", "lsort", "puts", "pwd", "return", "set", "source", "while",
        # Readline
        "history",
        # Custom commands
        "exit", "quit",
        # Design
        "list_components", "list_io_ports", "list_nets", "list_rows",
        "load_design", "read_design", "remove_design", "save_design",
        "load_components_coords", "save_components_coords", "design_info",
        # Bins
        "bins_info", "create_bins", "remove_bins",
        # Placement
        "place_random",
        # Routing
        "maze_routing",
        # Nets
        "net_info",
        # Wirelength
        "calculate_net_WL", "calculate_WL",
        # GUI
        "start_gui",
        # Testing
        "test"
        ]

    _tcl: Tk = None

    _design: Design = None
    _gui: GUI = None

    def __init__(self):
        self._commands.sort()
        self._initialize_interpreter()
        self._create_Tcl_commands()
    # End of method

    def _print_red(self, msg): print(f"{RED}{msg}{NORMAL}")
    def _print_yellow(self, msg): print(f"{YELLOW}{msg}{NORMAL}")

    # Interpreter initialization
    def _initialize_interpreter(self):
        self._tcl = Tcl()

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._completer)
    # End of method

    # Tcl Command creation
    def _create_Tcl_commands(self):
        self._tcl.createcommand("bins_info", self._bins_info)
        self._tcl.createcommand("calculate_WL", self._calculate_WL)
        self._tcl.createcommand("calculate_net_WL", self._calculate_net_WL)
        self._tcl.createcommand("create_bins", self._create_bins)
        self._tcl.createcommand("design_info", self._design_info)
        self._tcl.createcommand("list_components", self._list_components)
        self._tcl.createcommand("list_io_ports", self._list_io_ports)
        self._tcl.createcommand("list_nets", self._list_nets)
        self._tcl.createcommand("list_rows", self._list_rows)
        self._tcl.createcommand("load_design", self._load_design)
        self._tcl.createcommand(
            "load_components_coords",
            self._load_components_coords
        )
        self._tcl.createcommand("maze_routing", self._maze_routing)
        self._tcl.createcommand("net_info", self._net_info)
        self._tcl.createcommand("place_random", self._place_random)
        self._tcl.createcommand("read_design", self._read_design)
        self._tcl.createcommand("remove_bins", self._remove_bins)
        self._tcl.createcommand("remove_design", self._remove_design)
        self._tcl.createcommand("save_design", self._save_design)
        self._tcl.createcommand(
            "save_components_coords",
            self._save_components_coords
        )
        self._tcl.createcommand("start_gui", self._start_gui)
        self._tcl.createcommand("test", self._test)
    # End of method

    # Completer
    def _completer(self, text, state):
        # TODO: Expand completer with files and command flags (optional)
        results = [x for x in self._commands if x.startswith(text)] + [None]
        return results[state]
    # End of method

    # Tcl Commands
    def _bins_info(self):
        if not self._design.bins:
            interfaceLogger.info("There are no bins created")
        else:
            interfaceLogger.info(self._design.bins)
    # End of method


    def _calculate_net_WL(self, *args):
        commandFormat = "calculate_net_WL [-h | -net net] [-HPWL | -tree]"
        commandDescription = "Calculates the wirelength of the design"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return True
        elif ((len(args) == 3) & (args[0] == "-net")
              & ((args[2] == "-HPWL") | (args[2] == "-tree"))):

            if not self._design:
                interfaceLogger.info("There is no design loaded")
                return

            net:Net = self._design.core.get_net(args[1])
            if (not net):
                interfaceLogger.error(f"There is no net {args[1]}")
                return False
            else:
                if(args[2] == "-HPWL"):
                    wpwl = calculate_net_HPWL(net)
                    interfaceLogger.info(
                        f"Net {net.name} half-perimeter "\
                        f"wirelength is: {wpwl:.3f}")
                else:
                    treeWL = calculate_net_tree_wirelength(net)
                    interfaceLogger.info(
                        f"Net {net.name} routed wirelength is: {treeWL:.3f}")
        else:
            raise TclError
    # End of method
        
    def _calculate_WL(self, *args):
        commandFormat = "calculate_WL [-h | -HPWL | -tree]"
        commandDescription = "Calculates the wirelength of the design"

        if (len(args) == 1):
            if (args[0] == "-h"):
                print(f"{commandFormat}\n{commandDescription}")
                return True
            elif (args[0] == "-HPWL"):
                wpwl = calculate_HPWL(self._design)
                interfaceLogger.info(
                    f"Design half-perimeter wirelength is: {wpwl:.3f}")
            elif (args[0] == "-tree"):
                treeWL = calculate_tree_wirelength(self._design)
                interfaceLogger.info(
                    f"Design routed wirelength is: {treeWL:.3f}")
        else:
            raise TclError
    # End of method

    def _create_bins(self, *args) -> bool:
        commandFormat = "create_bins [-h | -size width height]"
        commandDescription = "Creates array of bins with given dimentions"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return True
        elif ((len(args) == 3) & (args[0] == "-size")):
            if self._design.bins:
                print("There are already bins created")
                return False

            try:
                width = int(args[1])
                height = int(args[2])
            except ValueError:
                interfaceLogger.error(
                    "Dimentions for bins are ment to be integers")
                return False
            
            self._design.create_bins(width, height)
            return True
        else:
            raise TclError
    # End of method
    
    def _design_info(self, * args):
        if not self._design:
            interfaceLogger.info("There is no design")
        else:
            interfaceLogger.info(self._design)
    # End of method

    def _list_components(self, *args) -> int:
        if not self._design:
            interfaceLogger.info("There is no design")
            return 0
        
        for comp in self._design.core.components:
            interfaceLogger.info(comp)
        return self._design.core.noof_components()
    # End of method

    def _list_io_ports(self, *args) -> int:
        if not self._design:
            interfaceLogger.info("There is no design")
            return 0
        
        for ioPort in self._design.core.ioPorts:
            interfaceLogger.info(ioPort)
        return self._design.core.noof_IO_ports()
    # End of method

    def _list_nets(self, *args) -> int:
        if not self._design:
            interfaceLogger.info("There is no design")
            return 0
        
        for net in self._design.core.nets:
            interfaceLogger.info(net)
        return self._design.core.noof_nets()
    # End of method

    def _list_rows(self, *args) -> int:
        if not self._design:
            interfaceLogger.info("There is no design")
            return 0
        
        for row in self._design.core.rows:
            interfaceLogger.info(row)
        return self._design.core.noof_rows()
    # End of method

    def _load_design(self, *args):
        self._print_yellow("Under Construction")
        print("To be used for loading design used on previous run")
    # End of method

    def _load_components_coords(self, *args) -> bool:
        commandFormat = "load_components_coords [-h | -f file]"
        commandDescription = "Loads component positions from given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return True
        elif ((len(args) == 2) & (args[0] == "-f")):
            if not self._design:
                interfaceLogger.info("There is no design loaded")
                return False

            try:
                with open(args[1], "r") as file:
                    if components_location_parser(file, self._design):
                        interfaceLogger.info("Components positions loaded")
                        return True
                    else:
                        interfaceLogger.error(
                            "Could not load components positions")
                        return False
            except IOError:
                interfaceLogger.error(f"There is no file: {args[1]}")
                return False
        else:
            raise TclError
    # End of method

    def _maze_routing(self, *args) -> bool:
        commandFormat = "maze_routing [-h | -counterclockwise]"
        commandDescription = "Displays information about a net"
        if (len(args) == 1):
            if (args[0] == "-h"):
                print(f"{commandFormat}\n{commandDescription}")
                return True
            elif (args[0] == "-counterclockwise"):
                if not self._design:
                    interfaceLogger.info("There is no design loaded")
                    return

                if not self._design.bins:
                    interfaceLogger.info("There are no bins for routing to be done")
                    return

                maze_routing(self._design, clockwiseRouting=False)
                return True
            else:
                raise TclError
        elif (len(args) == 0):
            if not self._design:
                interfaceLogger.info("There is no design loaded")
                return

            if not self._design.bins:
                interfaceLogger.info("There are no bins for routing to be done")
                return

            maze_routing(self._design)
        else:
            raise TclError
    # End of method

    def _net_info(self, *args) -> bool:
        commandFormat = "net_info [-h | net]"
        commandDescription = "Displays information about a net"
        if (len(args) == 1):
            if (args[0] == "-h"):
                print(f"{commandFormat}\n{commandDescription}")
                return True
            else:
                if not self._design:
                    interfaceLogger.info("There is no design loaded")
                    return
                net:Net = self._design.core.get_net(args[0])
                if (not net):
                    interfaceLogger.error(f"There is no net {args[0]}")
                    return False
                else:
                    if (net.connectionsTree is not None):
                        interfaceLogger.info(f"Net: {net.name}")
                        print_generic_tree(net.connectionsTree)
                    else:
                        interfaceLogger.info(net)
                    return True
        else:
            raise TclError
    # End of method

    def _place_random(self, *args) -> bool:
        # TODO: max tries for placement given by the user and show default value
        if random_placer(self._design.core):
            interfaceLogger.info("Random placement was sucessfull")
            return True
        else:
            interfaceLogger.info("Random placement failed")
            return False
    # End of method

    def _read_design(self, *args) -> bool:
        commandFormat = "read_design [-h | -f file]"
        commandDescription = "Reads design from given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return True
        elif ((len(args) == 2) & (args[0] == "-f")):
            if self._design:
                interfaceLogger.info("Design is already loaded")
                return False

            try:
                with open(args[1], "r") as file:
                    newDesign = practical_format_parcer(file)
            except IOError:
                interfaceLogger.error(f"There is no file: {args[1]}")
                return False
            
            self._design = newDesign
            interfaceLogger.info(f"Design loaded: {self._design.name}")
            return True
        else:
            raise TclError
    # End of method

    def _remove_bins(self):
        if (self._design.bins != None):
            self._design.remove_bins()
            interfaceLogger.info("Bins Removed")
        else:
            interfaceLogger.info("There are no bins to be removed")

    def _remove_design(self):
        if (self._design != None):
            del self._design
            interfaceLogger.info("Design Removed")
        else:
            interfaceLogger.info("There is no design to be removed")
    # End of method

    def _save_design(self, *args):
        self._print_yellow("Under Construction")
        print("To be used for saving design for future runs")
    # End of method

    def _save_components_coords(self, *args):
        commandFormat = "save_components_coords [-h | -f file]"
        commandDescription = "Saves component positions to given file"

        if ((len(args) == 1) & (args[0] == "-h")):
            print(f"{commandFormat}\n{commandDescription}")
            return
        elif ((len(args) == 2) & (args[0] == "-f")):
            if not self._design:
                interfaceLogger.info("Design is not loaded")
                return

            with open(args[1], "w") as file:
                write_component_positions(
                    file, self._design.name,self._design.core.components
                )
        else:
            raise TclError
    # End of method

    def _start_gui(self):
        self._gui = GUI("Router", self._design)

        self._gui.mainloop()
    # End of method

    def _test(self, *args):
        """Tcl command used for testing features"""

        print("Test command used during development")

        #Code for testing below:

    # End of method

    def _evaluate_command(self, command: str):
        """Evaluates given tcl command"""

        if ((command == "quit") | (command == "exit")):
            return "Finish"
        # Readline history, not the Tcl Command
        elif (command == "history"):
            readline.add_history(command)
            for i in range(readline.get_current_history_length()):
                print(readline.get_history_item(i))
        
        # Evaluate the command
        try:
            self._tcl.eval(command)
        except TclError:
        #    self._print_red("Invalid Tcl command or options on one")
            interfaceLogger.error("Invalid Tcl command or options on one")

        readline.add_history(command)
    # End of method

    # Interpreter
    def interpreter(self) -> None:
        """TCL Shell"""

        while (True):
            line = input(f"{CYAN}Router {os.getcwd()}> {NORMAL}")
            if self._evaluate_command(line) == "Finish":
                print("Goodbye!")
                break
    # End of method

    def script_interpreter(self, script: str) -> None:
        """
        Execution of TCL input script.

        In case the script does not contain a termination command 
        (exit or quit), the user can continue using the tool with the
        TCL Shell.
        """

        try:
            with open(script, "r") as file:
                while line := file.readline().rstrip():
                    result = self._evaluate_command(line)
        except IOError:
            interfaceLogger.error(f"There is no file: {script}")
            return

        if result == "Finish":
            print("Goodbye!")
        else:
            self.interpreter()
    # End of method
# End of class