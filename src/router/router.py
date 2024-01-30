"""
"""

import argparse

from tcl_interpreter import TclInterpreter

class Router:
    """
    Top class
    """

    _interp: TclInterpreter = None

    def __init__(self):
        self._interp = TclInterpreter()
    # End of method

    def run(self):
        """
        """
        self._interp.interpreter()
    # End of method
# End of class

if (__name__ == "__main__"):
    router = Router()
    router.run()
