import random
from typing import List
from design_components import Core
from design_components import Component

MAX_RANDOM_TRIES = 100

class RandomPlacer:

    _placedComponents: List[Component] = []

    def __init__(self):
        None

    def _placement_trial(self,x,y, width):
        if not self._placedComponents:
            return True

        for comp in self._placedComponents:
            # Check if they are in the same row
            if (comp.y != y): continue

            if ((comp.x >= (x + width)) | ((comp.x + comp.width) <= x)):
                continue

            return False
        
        return True


    def run(self, core: Core) -> bool:
        rows = core.noof_rows()
        for i in range(core.noof_components()):
            placed = False
            for j in range(MAX_RANDOM_TRIES):
                newRow = random.randrange(0, rows)
                xMin,y = core.get_row(newRow).get_coordinates()
                width = core.get_component(index=i).width
                xMax = xMin + core.get_row(newRow).width - width
                x = random.uniform(xMin, xMax)

                if (self._placement_trial(x,y,width)):
                    core.get_component(index=i).x = x
                    core.get_component(index=i).y = y
                    self._placedComponents.append(core.get_component(index=i))
                    placed = True
                    break

            if not placed:
                return False
        
        return True