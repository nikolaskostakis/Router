from io import TextIOWrapper
from typing import List

from structures.design_components import Component

HASH_LINE = "###############################################################\n"

def write_component_positions(file:TextIOWrapper,
                              designName:str,
                              components:List[Component]
                              ) -> None:
    """Writes components and their coordinates into file"""

    # Write the design
    # Hash line
    file.writelines(HASH_LINE)
    
    # Design name
    line = f"# Design: {designName}\n"
    file.write(line)

    # Hash line
    file.write(HASH_LINE)

    # Components
    file.write("# Components\n")

    # For each component
    for comp in components:
        # Write its coordinates
        line = f"Component: {comp.name} Location: {comp.x:.3f} {comp.y:.3f}\n"
        file.write(line)