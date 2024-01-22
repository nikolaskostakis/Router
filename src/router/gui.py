from tkinter import Tk
from tkinter import Canvas
from tkinter import Frame
from tkinter import Label
from tkinter import Button
import time

from structures.design_components import Design
from structures.bins import Bins

class GUI(Tk):

    _canvas: Canvas = None
    _infoFrame: Frame = None
    _binsFrame: Frame = None
    _buttonsFrame: Frame = None

    _design: Design = None
    _bins: Bins = None

    _width = 1010
    _height = 860
    _CanvasWidth = 850
    _CanvasHeight = 850
    _offset = 25

    _ratio: float = None

    show_components = True
    show_nets = False
    show_bins = False

    def __init__(self, screenName:(str|None) = None, design: Design = None,
                 bins:Bins = None):
        super().__init__(screenName)

        self.title(screenName)
        self.minsize(self._width,self._height)

        self._design = design
        self._bins = bins
    # End of method

    def __draw_rows(self):
        for i in range(self._design.core.noof_rows()):
            x, y = self._design.core.rows[i].get_coordinates()
            width, height = self._design.core.rows[i].get_dimentions()
            
            x = x * self._ratio + self._offset
            y = y * self._ratio + self._offset
            width *= self._ratio
            height *= self._ratio

            self._canvas.create_rectangle(x, y, (width+x), (height+y))
    # End of method

    def __draw_IO_ports(self):
        for i in range(self._design.core.noof_IO_ports()):
            x, y = self._design.core.ioPorts[i].get_coordinates()

            x = x * self._ratio + self._offset
            y = y * self._ratio + self._offset
            radius = 0.02 * self._ratio 
            self._canvas.create_oval((x-radius), (y-radius),
                                      (x+radius), (y+radius), fill="yellow")
    # End of method

    def __draw_components(self):
        if self.show_components:

            for i in range(self._design.core.noof_components()):
                x, y = self._design.core.components[i].get_coordinates()
                width, height = self._design.core.components[i].get_dimentions()
                
                x = x * self._ratio + self._offset
                y = y * self._ratio + self._offset
                width *= self._ratio
                height *= self._ratio

                self._canvas.create_rectangle(x, y, (width+x), (height+y),
                                              outline="blue", tags="comp")
                #self._canvas.create_text((x + (width / 2)), (y + (height / 2)),
                #                         text=self._design.core.components[i].name,
                #                         fill="blue", width=width)
        else:
            self._canvas.delete("comp")
            self._canvas.delete("nets")

        self.show_components = not self.show_components
        self.update()
        self.update_idletasks()
        time.sleep(1)
    # End of method

    def _draw_nets(self):
        if self.show_nets:
            for net in self._design.core.nets:
                x1, y1 = net.source.get_coordinates()
                if (net.source.__class__.__name__ == "IOPort"):
                    w1 = 0
                    h1 = 0
                else:
                    w1, h1 = net.source.get_dimentions()

                x1 = x1 * self._ratio + self._offset
                y1 = y1 * self._ratio + self._offset
                w1 *= self._ratio
                h1 *= self._ratio

                x1 += w1/2
                y1 += h1/2

                for dr in net.drain:
                    x2, y2 = dr.get_coordinates()
                    w2, h2 = dr.get_dimentions()

                    x2 = x2 * self._ratio + self._offset
                    y2 = y2 * self._ratio + self._offset
                    w2 *= self._ratio
                    h2 *= self._ratio

                    x2 += w2/2
                    y2 += h2/2

                    self._canvas.create_line(x1,y1,x2,y2,
                                             fill="red", tags="nets")
        else:
            self._canvas.delete("nets")
        
        self.show_nets = not self.show_nets
        time.sleep(1)
    # End of method

    def _draw_bins(self):
        if (not self._bins): return

        if self.show_bins:
            binsX, binsY = self._bins.size

            coreWidth, coreHeight = self._design.core.get_dimentions()
            coreWidth += 2 * self._design.core.x_offset
            coreHeight += 2 * self._design.core.y_offset

            bw = coreWidth * self._ratio / binsX
            bh = coreHeight * self._ratio / binsY
            for i in range(binsX):
                for j in range(binsY):
                    x1 = (i * bw) + self._offset
                    y1 = (j * bh) + self._offset
                    x2 = ((i+1) * bw) + self._offset
                    y2 = ((j+1) * bh) + self._offset
                    self._canvas.create_rectangle(x1, y1, x2, y2,
                                              outline="orange", tags="bins")
        else:
            self._canvas.delete("bins")

        self.show_bins = not self.show_bins
    # End of method

    def _draw_core(self):
        if (self._design == None):
            self._canvas.create_text((self._width / 2), (self._height / 2),
                                      text = "There is no design loaded",
                                      fill = "black")
            self._canvas.pack()
            return
        

        coreWidth, coreHeight = self._design.core.get_dimentions()
        coreWidth += 2 * self._design.core.x_offset
        coreHeight += 2 * self._design.core.y_offset
        xRatio = (self._width - 2 * self._offset) / coreWidth
        yRatio = (self._height - 2 * self._offset) / coreHeight
        self._ratio = xRatio if (xRatio <= yRatio) else yRatio

        # Core
        self._canvas.create_rectangle(self._offset,  self._offset,
                                       ((coreWidth * self._ratio) + self._offset),
                                       ((coreHeight * self._ratio) + self._offset))

        # Rows
        self.__draw_rows()

        # IO Ports
        self.__draw_IO_ports()

        # Componenta
        self.__draw_components()

        # Nets
        self._draw_nets()

        # Bins
        self._draw_bins()
    # End of method

    def _draw_core_info(self):
        Label(self._infoFrame, text="Design: ").grid(row=0, column=0, 
                                                    sticky="NW")
        Label(self._infoFrame, text=f"{self._design.name}").grid(row=0, column=1,
                                                                sticky="NE")

        Label(self._infoFrame, text="--------------").grid(row=1, column=0,
                                                          sticky="NW")
        Label(self._infoFrame, text="--------------").grid(row=1, column=1,
                                                          sticky="NE")

        Label(self._infoFrame, text="Rows: ").grid(row=2, column=0, sticky="NW")
        Label(self._infoFrame, text=f"{self._design.core.noof_rows()}"
              ).grid(row=2, column=1, sticky="NE")

        Label(self._infoFrame, text="IO Ports: ").grid(row=3, column=0,
                                                      sticky="NW")
        Label(self._infoFrame, text=f"{self._design.core.noof_IO_ports()}"
              ).grid(row=3, column=1, sticky="NE")

        Label(self._infoFrame, text="Components: ").grid(row=4, column=0, 
                                                        sticky="NW")
        Label(self._infoFrame, text=f"{self._design.core.noof_components()}"
              ).grid(row=4, column=1, sticky="NE")

        Label(self._infoFrame, text="Nets: ").grid(row=5, column=0, sticky="NW")
        Label(self._infoFrame, text=f"{self._design.core.noof_nets()}"
              ).grid(row=5, column=1, sticky="NE")
    # End of method

    def _draw_bins_info(self):
        if (not self._bins):
            Label(self._binsFrame,text="There are no bins").grid(
                row=0, column=0,sticky="N")
            return

        Label(self._binsFrame, text="Bins").grid(
            row=0, column=0, columnspan=2, sticky="N")
        Label(self._binsFrame, text="Size").grid(row=1,column=0)
        Label(self._binsFrame, text=f"{self._bins.size}").grid(row=1,column=1)
    # End of method

    def _draw_buttons(self):
        Button(self._buttonsFrame,text="Toggle Components", 
               command= lambda:self.__draw_components()).grid(row=0, column=0,
                                                              sticky="N")
        Button(self._buttonsFrame,text="Toggle Nets", 
               command= lambda:self._draw_nets()).grid(row=1, column=0,
                                                              sticky="N")
        Button(self._buttonsFrame,text="Toggle Bins", 
               command= lambda:self._draw_bins()).grid(row=2, column=0,
                                                              sticky="N")
    # End of method

    def _draw_gui(self):
        if (self._design == None):
            Label(self, text="There is no design loaded",
                  font=("Arial", 40)).pack(padx=(self._width/2),
                                           pady=(self._height/2))
            return

        self._canvas = Canvas(self,width = self._CanvasWidth,
                               height = self._CanvasHeight)
        self._canvas.grid(row=0, column=1, rowspan=20, sticky="nswe", 
                          padx=5, pady=5)
        self._draw_core()

        # Core Information
        self._infoFrame = Frame(self, width=150, height=150)
        self._infoFrame.grid(row=0, column=0,sticky="N", padx=5, pady=5)
        self._draw_core_info()

        # Bins Information
        self._binsFrame = Frame(self, width=150, height=150)
        self._binsFrame.grid(row=1, column=0, sticky="N", padx=5, pady=5)
        self._draw_bins_info()

        # Buttons
        self._buttonsFrame = Frame(self, width=150, height= 300)
        self._buttonsFrame.grid(row=2, column=0, sticky="N", padx=5, pady=5)
        self._draw_buttons()
        
    # End of method

    def mainloop(self, n: int = 0):
        self._draw_gui()
        super().mainloop(n)
    # End of method