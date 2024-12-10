# -*- coding: utf-8 -*-

"""
Module containing file writers
"""

__author__ = "Nikolaos Kostakis"
__copyright__ = "Copyright (c) 2024 Nikolaos Kostakis"
__license__ = "MIT License"
__version__ = "1.0"

import logging
import pickle
from io import TextIOWrapper

import config
from . import HASH_LINE
from structures.design_components import Design, Component

# Logging
writersLogger = logging.getLogger(__name__)
writersLogger.setLevel(logging.DEBUG)
writersLogger.addHandler(config.consoleHandler)
writersLogger.addHandler(config.logfileHandler)

def write_component_positions(file:TextIOWrapper,
                              designName:str,
                              components:list[Component]
                              ) -> None:
    """Writes components and their coordinates into file"""

    # Write the design
    # Hash line
    file.writelines(f"{HASH_LINE}\n")
    
    # Design name
    line = f"# Design: {designName}\n"
    file.write(line)

    # Hash line
    file.write(f"{HASH_LINE}\n")

    # Components
    file.write("# Components\n")

    # For each component
    for comp in components:
        # Write its coordinates
        line = f"Component: {comp.name} Location: {comp.x:.3f} {comp.y:.3f}\n"
        file.write(line)
    
    writersLogger.debug(f"Components stored: {len(components)}")
# End of function

def pickle_design_to_file(file:TextIOWrapper, design: Design) -> None:
    """Writes the deign and all its elements into a file using pickle"""

    # Write the design to the file
    # The bins are stored as well
    pickle.dump(design, file)

    # Write the lists of the various elements
    pickle.dump(design.core.rows, file)
    pickle.dump(design.core.ioPorts, file)
    pickle.dump(design.core.components, file)
    pickle.dump(design.core.nets, file)
    return
# End of function