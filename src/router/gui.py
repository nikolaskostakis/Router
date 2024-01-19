from tkinter import Tk
from tkinter import Canvas
from design_components import Design

class GUI(Tk):

    _canvas: Canvas = None
    _design: Design = None

    _width = 550
    _height = 650
    _offset = 25

    def __init__(self, screenName: (str | None) = None, design: Design = None):
        super().__init__(screenName)

        self.title(screenName)
        self.minsize(self._width,self._height)

        self._design = design

    def __draw_rows(self, ratio: float):
        for i in range(self._design.core.noof_rows()):
            x, y = self._design.core.rows[i].get_coordinates()
            width, height = self._design.core.rows[i].get_dimentions()
            
            x = x * ratio + self._offset
            y = y * ratio + self._offset
            width *= ratio
            height *= ratio

            self._canvas.create_rectangle(x, y, (width+x), (height+y))

    def __draw_IO_ports(self, ratio: float):
        for i in range(self._design.core.noof_IO_ports()):
            x, y = self._design.core.ioPorts[i].get_coordinates()

            x = x * ratio + self._offset
            y = y * ratio + self._offset
            radius = 0.02 * ratio 
            self._canvas.create_oval((x-radius), (y-radius),
                                      (x+radius), (y+radius), fill="yellow")

    def __draw_components(self, ratio):
        for i in range(self._design.core.noof_components()):
            x, y = self._design.core.components[i].get_coordinates()
            width, height = self._design.core.components[i].get_dimentions()
            
            x = x * ratio + self._offset
            y = y * ratio + self._offset
            width *= ratio
            height *= ratio

            self._canvas.create_rectangle(x, y, (width+x), (height+y),
                                          outline="blue")

    def __draw_core(self):
        self._canvas = Canvas(self,width = self._width,
                               height = self._height)

        if (self._design == None):
            self._canvas.create_text(300, 250,
                                      text = "There is no design loaded",
                                      fill = "black")
            self._canvas.pack()
            return
        

        coreWidth, coreHeight = self._design.core.get_dimentions()
        coreWidth += 2 * self._design.core.x_offset
        coreHeight += 2 * self._design.core.y_offset
        xRatio = (self._width - 2 * self._offset) / coreWidth
        yRatio = (self._height - 2 * self._offset) / coreHeight
        ratio = xRatio if (xRatio <= yRatio) else yRatio

        # Core
        self._canvas.create_rectangle(self._offset,  self._offset,
                                       ((coreWidth * ratio) + self._offset),
                                       ((coreHeight * ratio) + self._offset))

        # Rows
        self.__draw_rows(ratio)

        # IO Ports
        self.__draw_IO_ports(ratio)

        # Components
        self.__draw_components(ratio)

        self._canvas.pack()
    
    def mainloop(self, n: int = 0):
        self.__draw_core()
        super().mainloop(n)