"""
Module containing file writers
"""

import logging
from io import TextIOWrapper

import config
from . import HASH_LINE
from structures.design_components import Component

# Logging
writersLogger = logging.getLogger(__name__)
writersLogger.setLevel(logging.DEBUG)
writersLogger.addHandler(config.consoleHandler)

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