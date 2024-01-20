#from design_components import Design
from tcl_interpreter import TclInterpreter

class Router:
    """
    Top class
    """

    interp: TclInterpreter = None

    def __init__(self):
        None

    def start_interpreter(self):
        self.interp = TclInterpreter()
        self.interp.interpreter()

    def main(self):
        """
        """
        if (__name__ != "__main__"):
            print("This method is to be used as main function " \
                  "for standalone execution of Router\n" \
                  "Cannot be used otherwise")

        self.start_interpreter()

router = Router()
router.main()
