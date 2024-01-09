from design_components import Design
from parsers import PracticalFormatParser
from tcl_interpreter import TclInterpreter

pFP = PracticalFormatParser()

file = open("benchmarks\counter7.txt", 'r')

#design = pFP.parse_file(file)
#print(design.core)
inter = TclInterpreter()

inter.interpreter()