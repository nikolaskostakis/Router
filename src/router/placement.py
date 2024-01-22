"""
Module containing functions for placement
"""

import random
from typing import List

from structures.design_components import Core
from structures.design_components import Component

MAX_RANDOM_TRIES = 100000

def random_placer(core: Core) -> bool:
    """
    Function used to place the components of the design in random positions
    Returns True if successful and False otherwise

    Function does not check for mixed-cell-heights
    """

    placedComponents: List[Component] = []
    """Temporary queue, used for already placed components"""

    def _placement_trial(x:float, y:float, width:float) -> bool:
        """Checks if the new componen's destination is empty"""
        if not placedComponents:
            return True

        for comp in placedComponents:
            # Check if they are in the same row
            if (comp.y != y): continue

            if ((comp.x >= (x + width)) | ((comp.x + comp.width) <= x)):
                continue

            return False
        
        return True

    rows = core.noof_rows()
    for comp in core.components:
        placed = False
        for j in range(MAX_RANDOM_TRIES):
            newRow = random.randrange(0, rows)
            xMin,y = core.rows[newRow].get_coordinates()
            width = comp.width
            xMax = xMin + core.rows[newRow].width - width
            x = random.uniform(xMin, xMax)

            if (_placement_trial(x,y,width)):
                comp.x = x
                comp.y = y
                placedComponents.append(comp)

                placed = True
                break

        if not placed:
            index = core.components.index(comp)
            print(f"Failed at {index + 1}/{core.noof_components()}")
            placedComponents.clear()
            return False
    
    placedComponents.clear()
    return True