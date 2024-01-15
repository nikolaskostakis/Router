from tkinter import Tk
from tkinter import Canvas
from design_components import Design

class GUI(Tk):

    __canvas: Canvas = None
    __design: Design = None

    __width = 550
    __height = 650
    __offset = 25

    def __init__(self, screenName: (str | None) = None, design: Design = None):
        super().__init__(screenName)

        self.title(screenName)
        self.minsize(self.__width,self.__height)

        self.__design = design

    def __draw_rows(self, ratio: float):
        for i in range(self.__design.core.noof_rows()):
            x, y = self.__design.core.get_row(i).get_coordinates()
            width, height = self.__design.core.get_row(i).get_dimentions()
            
            x = x * ratio + self.__offset
            y = y * ratio + self.__offset
            width *= ratio
            height *= ratio

            self.__canvas.create_rectangle(x, y, (width+x), (height+y))

    def __draw_IO_ports(self, ratio: float):
        for i in range(self.__design.core.noof_IO_ports()):
            x, y = self.__design.core.get_IO_port(index = i).get_coordinates()

            x = x * ratio + self.__offset
            y = y * ratio + self.__offset
            radius = 0.02 * ratio 
            self.__canvas.create_oval((x-radius), (y-radius),
                                      (x+radius), (y+radius), fill="yellow")


    def __draw_core(self):
        self.__canvas = Canvas(self,width = self.__width,
                               height = self.__height)

        if (self.__design == None):
            self.__canvas.create_text(300, 250,
                                      text = "There is no design loaded",
                                      fill = "black")
            self.__canvas.pack()
            return
        

        coreWidth, coreHeight = self.__design.core.get_dimentions()
        coreWidth += 2 * self.__design.core.get_x_offset()
        coreHeight += 2 * self.__design.core.get_y_offset()
        xRatio = (self.__width - 2 * self.__offset) / coreWidth
        yRatio = (self.__height - 2 * self.__offset) / coreHeight
        ratio = xRatio if (xRatio <= yRatio) else yRatio

        # Core
        self.__canvas.create_rectangle(self.__offset,  self.__offset,
                                       ((coreWidth * ratio) + self.__offset),
                                       ((coreHeight * ratio) + self.__offset))

        # Rows
        self.__draw_rows(ratio)

        # IO Ports
        self.__draw_IO_ports(ratio)

        self.__canvas.pack()
    
    def mainloop(self, n: int = 0):
        self.__draw_core()
        super().mainloop(n)