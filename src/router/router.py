"""
Top Module
"""

import logging
import argparse
from argparse import ArgumentParser

import config
from ui.tcl_interpreter import TclInterpreter

class Router:
    """
    Top class
    """

    class HelpFormatter(argparse.HelpFormatter):
        """
        Format helper for the metavars to be shown once in the help description
        """
        def _format_action_invocation(self, action: argparse.Action) -> str:
            formatted = super()._format_action_invocation(action)
            if action.option_strings and action.nargs != 0:
                def_metavar = self._get_default_metavar_for_optional(action)
                formatted = formatted.replace(
                    f" {self._format_args(action, def_metavar)}",
                    "",
                    len(action.option_strings) - 1,
                )

            return formatted

    _interpreter: TclInterpreter = None
    """Tcl Interpreter"""
    _argParser: ArgumentParser = None
    _arguments = []

    def __init__(self):
        self._interpreter = TclInterpreter()

        self._parse_arguments()
    # End of method

    def _parse_arguments(self) -> None:
        """
        Creates an argument parser and helping description for Router's inputs
        """

        self._argParser = ArgumentParser(
            #prog="Router",
            description="A tool used for routing, based on Lee's Maze routing",
            add_help=True,
            formatter_class=self.HelpFormatter
        )

        # Input script
        self._argParser.add_argument(
            "-i", "--input",
            metavar="script",
            type=str,
            help="input script"
            )

        # Debug
        self._argParser.add_argument(
            "-d", "--debug",
            default=False,
            action="store_true",
            help="show debug messages"
        )

        # Version
        self._argParser.add_argument(
            "--version",
            action="version",
            version="%(prog)s 1.0"
        )

        self._arguments = self._argParser.parse_args()

        # Change logging level in case of debug
        if self._arguments.debug:
            config.loggingLevel = logging.DEBUG
            config.consoleHandler.setLevel(config.loggingLevel)
    # End of method

    def run(self) -> None:
        """Start the tool"""

        if self._arguments.input :
            self._interpreter.script_interpreter(self._arguments.input)
        else:
            self._interpreter.interpreter()
    # End of method
# End of class

if (__name__ == "__main__"):
    router = Router()
    router.run()
