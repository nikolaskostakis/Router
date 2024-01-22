"""
"""

import numpy as np
from numpy import ndarray

from structures.design_components import Core

class Bins:

    _bins:ndarray = None
    """The array of bins"""
    _temp:ndarray = None
    """Temporary array, used to fill the bins"""
    
    _size:tuple[int,int] = None

    def __init__(self, width:int, height:int) -> None:
        self._size = (width, height)

        self._bins = np.zeros(self._size)
        self._temp = np.zeros(self._size)

    def __repr__(self) -> str:
        return f"Bins {self.size}:\n{self._bins}"

    @property
    def size(self) -> tuple[int, int]:
        "Size of bins array"
        return self._size

    @property
    def bins(self) -> ndarray:
        "Bins array"
        return self._bins

    def determine_bins(self, core: Core):
        binWidth = (core.width + 2 *core.x_offset) / self._size[0]
        binHeight = (core.height + 2 * core.y_offset) / self.size[1]

        # For the IO Ports
        for port in core.ioPorts:
            x,y = port.get_coordinates()
            bin = (int(x/binWidth), int(y/binHeight))
            port.bin = bin
        # For the Components
        for comp in core.components:
            x,y = comp.get_coordinates()
            w,h = comp.get_dimentions()
            bin = (int((x + w/2)/binWidth), int((y + h/2)/binHeight))
            comp.bin = bin


# End of class