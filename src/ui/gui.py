# -*- coding: utf-8 -*-

"""
Module housing the graphical user interface (GUI)
"""

__author__ = "Nikolaos Kostakis"
__copyright__ = "Copyright (c) 2024 Nikolaos Kostakis"
__license__ = "MIT License"
__version__ = "1.0"

from tkinter import Tk, Canvas, Frame, Label, Button, Entry, messagebox
from tkinter.ttk import Separator

from matplotlib import pyplot

from structures.design_components import Design, NetTreeNode, Bins

class GUI(Tk):

    _canvas: Canvas = None
    _infoFrame: Frame = None
    _binsFrame: Frame = None
    _buttonsFrame: Frame = None

    _design: Design = None

    _width = 1030
    _height = 860
    _CanvasWidth = 850
    _CanvasHeight = 850
    _offset = 25

    _ratio: float = None

    show_components = True
    show_components_names = True
    show_nets = False
    show_blockages = False
    show_bins = False
    netSearch = None

    def __init__(self, screenName:(str|None) = None, design: Design = None):
        super().__init__(screenName)

        self.title(screenName)
        self.minsize(self._width,self._height)

        self._design = design
    # End of method

    def _calc_ratio(self) -> None:
        """Method used for calculating the drawing ratio"""

        coreWidth, coreHeight = self._design.core.get_dimensions()
        coreWidth += 2 * self._design.core.x_offset
        coreHeight += 2 * self._design.core.y_offset
        xRatio = (self._CanvasWidth - 2 * self._offset) / coreWidth
        yRatio = (self._CanvasHeight - 2 * self._offset) / coreHeight
        self._ratio = xRatio if (xRatio <= yRatio) else yRatio
    # End of method

    def _draw_rows(self) -> None:
        """Method used for drawing the rows of the core"""

        for i in range(self._design.core.noof_rows()):
            x, y = self._design.core.rows[i].get_coordinates()
            width, height = self._design.core.rows[i].get_dimensions()
            
            x = x * self._ratio + self._offset
            y = y * self._ratio + self._offset
            width *= self._ratio
            height *= self._ratio

            self._canvas.create_rectangle(x, y, (width+x), (height+y))
    # End of method

    def _draw_IO_ports(self) -> None:
        """Method used for drawing the IO ports of the core"""

        for i in range(self._design.core.noof_IO_ports()):
            x, y = self._design.core.ioPorts[i].get_coordinates()

            x = x * self._ratio + self._offset
            y = y * self._ratio + self._offset
            radius = 0.02 * self._ratio 
            self._canvas.create_oval((x-radius), (y-radius),
                                      (x+radius), (y+radius), fill="yellow")
    # End of method

    def _draw_components(self) -> None:
        """
        Method used for drawing the components of the core.
        
        The names of the components are drawn depending the state of toggle
        button.
        """

        if self.show_components:

            for i in range(self._design.core.noof_components()):
                x, y = self._design.core.components[i].get_coordinates()
                width, height = self._design.core.components[i].get_dimensions()
                
                x = x * self._ratio + self._offset
                y = y * self._ratio + self._offset
                width *= self._ratio
                height *= self._ratio

                self._canvas.create_rectangle(x, y, (width+x), (height+y),
                                              outline="blue", tags="comp")

                if self.show_components_names:
                    self._canvas.create_text(
                        (x + (width / 2)), (y + (height / 2)),
                        text=self._design.core.components[i].name,
                        fill="blue", width=width, tags=["comp","compNames"]
                    )
            # End for loop
        else:
            self._canvas.delete("comp")
            self._canvas.delete("nets")
            self.show_nets = True

        self.show_components = not self.show_components
        self.update()
        self.update_idletasks()
    # End of method

    def _draw_component_names(self):
        """Method used for drawing the names of the components in the canvas"""
        if not self.show_components:
            if self.show_components_names:
                self._canvas.delete("compNames")
            else:
                for i in range(self._design.core.noof_components()):
                    x, y = self._design.core.components[i].get_coordinates()
                    width, height = self._design.core.components[i].get_dimensions()
                    
                    x = x * self._ratio + self._offset
                    y = y * self._ratio + self._offset
                    width *= self._ratio
                    height *= self._ratio

                    self._canvas.create_text(
                        (x + (width / 2)), (y + (height / 2)),
                        text=self._design.core.components[i].name,
                        fill="blue", width=width, tags=["comp","compNames"]
                    )
                # End for loop
            # End else
        # End if
        
        self.show_components_names = not self.show_components_names
    # End of method

    def _recursive_net_drawing(self, node:NetTreeNode, color="orange", tags=""):
        """
        Recursive method used for drawing the tree representatio of a net
        """
        lineTags = ["nets","treeView"]
        lineTags.append(tags)
        if node.children == []:
            return
        x1, y1 = node.point.get_coordinates()
        if (node.point.__class__.__name__ == "Component"):
            w1, h1 = node.point.get_dimensions()
        else:
            w1 = 0
            h1 = 0
        x1 = x1 * self._ratio + self._offset
        y1 = y1 * self._ratio + self._offset
        w1 *= self._ratio
        h1 *= self._ratio

        x1 += w1/2
        y1 += h1/2

        child:NetTreeNode
        for child in node.children:
            x2, y2 = child.point.get_coordinates()
            if (child.point.__class__.__name__ == "Component"):
                w2, h2 = child.point.get_dimensions()
            else:
                w2 = 0
                h2 = 0
            x2 = x2 * self._ratio + self._offset
            y2 = y2 * self._ratio + self._offset
            w2 *= self._ratio
            h2 *= self._ratio

            x2 += w2/2
            y2 += h2/2

            self._canvas.create_line(x1, y1, x2, y2, fill=color, tags=lineTags)
            self._recursive_net_drawing(child, color, tags)
    # End of method

    def _draw_nets(self, drawP2P:bool = True):
        """
        Method used for drawing the nets on the canvas
        """
        if ((not self._design.isRouted) & (not drawP2P)):
            messagebox.showinfo("Tree view", 
                "There is no tree view. Run routing first!")
            return

        if self.show_nets:
            if drawP2P:
                for net in self._design.core.nets:
                    x1, y1 = net.source.get_coordinates()
                    if (net.source.__class__.__name__ == "IOPort"):
                        w1 = 0
                        h1 = 0
                    else:
                        w1, h1 = net.source.get_dimensions()

                    x1 = x1 * self._ratio + self._offset
                    y1 = y1 * self._ratio + self._offset
                    w1 *= self._ratio
                    h1 *= self._ratio

                    x1 += w1/2
                    y1 += h1/2

                    for dr in net.drain:
                        x2, y2 = dr.get_coordinates()
                        w2, h2 = dr.get_dimensions()

                        x2 = x2 * self._ratio + self._offset
                        y2 = y2 * self._ratio + self._offset
                        w2 *= self._ratio
                        h2 *= self._ratio

                        x2 += w2/2
                        y2 += h2/2

                        self._canvas.create_line(x1, y1, x2, y2,
                            fill="black", tags=["nets","P2P"])
                # End for loop
            # End if p2p
            else:
                for net in self._design.core.nets:
                    if (net.connectionsTree is None):
                        messagebox.showinfo("Tree view", 
                            f"There is no tree connection for net {net.name}")
                        continue
                    self._recursive_net_drawing(net.connectionsTree)
                # End for loop
            # End else tree view
        # End if show nets
        else:
            if (drawP2P):
                self._canvas.delete("P2P")
            else:
                self._canvas.delete("treeView")
        
        self.show_nets = not self.show_nets
    # End of method
    
    def _highlight_net(self, drawP2P = True) -> None:
        """
        Method used for drawing a highlighted net. The net can
        either be P2P orof a tree connection.
        """

        netName = self.netSearch.get()
        net = self._design.core.get_net(netName)
        if (not net):
            messagebox.showinfo("Net searching", f"There is no net {netName}")
            return

        if drawP2P:
            x1, y1 = net.source.get_coordinates()
            if (net.source.__class__.__name__ == "IOPort"):
                w1 = 0
                h1 = 0
            else:
                w1, h1 = net.source.get_dimensions()

            x1 = x1 * self._ratio + self._offset
            y1 = y1 * self._ratio + self._offset
            w1 *= self._ratio
            h1 *= self._ratio

            x1 += w1/2
            y1 += h1/2

            for dr in net.drain:
                x2, y2 = dr.get_coordinates()
                w2, h2 = dr.get_dimensions()

                x2 = x2 * self._ratio + self._offset
                y2 = y2 * self._ratio + self._offset
                w2 *= self._ratio
                h2 *= self._ratio

                x2 += w2/2
                y2 += h2/2

                self._canvas.create_line(x1,y1,x2,y2,
                                        fill="purple",
                                        tags=["nets","P2P", "highlight"])
            # End for loop
        # End if
        else:
            if not net.connectionsTree:
                messagebox.showinfo("Tree view", 
                                "There is no tree view. Run routing first!")
                return
            self._recursive_net_drawing(net.connectionsTree,
                                            color="red",tags="highlight")
        # End else
    # End of method
    
    def _clear_highlight(self):
        """Method used for removing highlighted nets"""

        self._canvas.delete("highlight")
    # End of method


    def _draw_bins(self):
        """Method used for drawing the bins of the design"""

        if (not self._design.bins): return

        if self.show_bins:
            binsY, binsX = self._design.bins.size

            coreWidth, coreHeight = self._design.core.get_dimensions()
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
                                              outline="green", tags="bins")
        else:
            self._canvas.delete("bins")

        self.show_bins = not self.show_bins
    # End of method

    def _draw_blockages(self):
        """Method used for drawing the bins of the design"""

        if (not self._design.blockages): return

        if self.show_blockages:
            binsY, binsX = self._design._blockages.size

            coreWidth, coreHeight = self._design.core.get_dimensions()
            coreWidth += 2 * self._design.core.x_offset
            coreHeight += 2 * self._design.core.y_offset

            bw = coreWidth * self._ratio / binsX
            bh = coreHeight * self._ratio / binsY
            for i in range(binsX):
                for j in range(binsY):
                    if (self._design.blockages[(j,i)]):
                        x1 = (i * bw) + self._offset
                        y1 = (j * bh) + self._offset
                        x2 = ((i+1) * bw) + self._offset
                        y2 = ((j+1) * bh) + self._offset
                        self._canvas.create_rectangle(x1, y1, x2, y2,
                                                outline="brown", stipple="gray12",fill="brown", tags="blockages")
        else:
            self._canvas.delete("blockages")

        self.show_blockages = not self.show_blockages
    # End of method

    @staticmethod
    def heatmap(bins:(Bins|None), binsName:str) -> None:
        """Method used for showing the heatmap of given bins"""

        if bins == None:
            messagebox.showinfo(
                binsName,
                "There are no bins. You need to create them first!"
            )
            return

        xAxis = list(range(bins.size[1]))
        yAxis = list(range(bins.size[0]))

        fig = pyplot.figure()
        plt = fig.add_subplot(111)
        plt.set_title(f"Heatmap of {binsName}")
        plt.set_xticks(xAxis)
        plt.set_yticks(yAxis)

        #for i in range(bins.size[0]):
        #    for j in range(bins.size[1]):
        #        text = plt.text(j, i, bins.bins[i,j],ha="center", va="center", color="r")

        hmap = plt.imshow(bins.bins, cmap='viridis')
        fig.colorbar(hmap)
        fig.show()
    # End of method

    def _draw_core(self) -> None:
        """Method used for drawing the core of the design"""

        if (self._design == None):
            self._canvas.create_text(
                (self._width / 2), (self._height / 2),
                text = "There is no design loaded", fill = "black"
            )
            self._canvas.pack()
            return
        

        self._calc_ratio()
        coreWidth, coreHeight = self._design.core.get_dimensions()
        coreWidth += 2 * self._design.core.x_offset
        coreHeight += 2 * self._design.core.y_offset

        # Core
        self._canvas.create_rectangle(
            self._offset,  self._offset,
            ((coreWidth * self._ratio) + self._offset),
            ((coreHeight * self._ratio) + self._offset)
        )

        # Rows
        self._draw_rows()

        # IO Ports
        self._draw_IO_ports()

        # Components
        self._draw_components()

        # Nets
        self._draw_nets()

        # Bins
        self._draw_bins()

        # Blockages
        self._draw_blockages()
    # End of method

    def _draw_core_info(self):
        """Information about the design shown in the info Frame"""

        
        self._infoFrame.columnconfigure(0,weight=1)
        self._infoFrame.columnconfigure(1,weight=1)
        self._infoFrame.columnconfigure(2,weight=1)

        designLabel = Label(self._infoFrame, text="Design:")
        designLabel.grid(row=0, column=0, sticky="NW")

        designName = Label(self._infoFrame, text=f"{self._design.name}")
        designName.grid(row=0, column=2, sticky="NE")

        seperator = Separator(self._infoFrame, orient='horizontal')
        seperator.grid(row=1, column=0, columnspan=3, sticky="EW", pady=5)

        verticalSeperator = Separator(self._infoFrame, orient='vertical')
        verticalSeperator.grid(row=0, column=1, rowspan=6, sticky="NS", pady=5)

        rowsLabel = Label(self._infoFrame, text="Rows:")
        rowsLabel.grid(row=2, column=0, sticky="NW")

        rowsNum = Label(
            self._infoFrame, text=f"{self._design.core.noof_rows()}"
        )
        rowsNum.grid(row=2, column=2, sticky="NE")

        ioLabel = Label(self._infoFrame, text="IO Ports: ")
        ioLabel.grid(row=3, column=0, sticky="NW")

        ioNum = Label(
            self._infoFrame, text=f"{self._design.core.noof_IO_ports()}"
        )
        ioNum.grid(row=3, column=2, sticky="NE")

        componentsLabel = Label(self._infoFrame, text="Components: ")
        componentsLabel.grid(row=4, column=0, sticky="NW")

        componentsNum = Label(
            self._infoFrame, text=f"{self._design.core.noof_components()}"
        )
        componentsNum.grid(row=4, column=2, sticky="NE")

        netsLabel = Label(self._infoFrame, text="Nets: ")
        netsLabel.grid(row=5, column=0, sticky="NW")

        netsNum = Label(
            self._infoFrame, text=f"{self._design.core.noof_nets()}"
        )
        netsNum.grid(row=5, column=2, sticky="NE")
    # End of method

    def _draw_bins_info(self):
        """Information about the bins in the bins Frame"""
        if (not self._design.bins):
            Label(self._binsFrame,text="There are no bins").place(x=75, y=25, anchor="center")
            return
        
        self._binsFrame.columnconfigure(0,weight=1)
        self._binsFrame.columnconfigure(1,weight=1)

        binsHeaderLabel = Label(self._binsFrame, text="Bins")
        binsHeaderLabel.grid(row=0, column=0, columnspan=2, sticky="ESW",pady=5)

        sizeHeaderLabel = Label(self._binsFrame, text="Size")
        sizeHeaderLabel.grid(row=1,column=0,sticky="E")

        sizeLabel = Label(self._binsFrame, text=f"{self._design.bins.size}")
        sizeLabel.grid(row=1,column=1,sticky="W")
    # End of method

    def _draw_buttons(self):
        """Buttons used for understanding the implementation of the algorithm"""

        rowNumber = 0

        toggleComponentsButton = Button(
            self._buttonsFrame,text="Toggle Components", width=20,
            command= lambda:self._draw_components()
        )
        toggleComponentsButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1
        
        toggleComponentsButton = Button(
            self._buttonsFrame,text="Toggle Comp. Names", width=20,
            command= lambda:self._draw_component_names()
        )
        toggleComponentsButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        toggleNetsP2PButton = Button(
            self._buttonsFrame,text="Toggle Nets (P2P)", width=20,
            command= lambda:self._draw_nets()
        )
        toggleNetsP2PButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        toggleNetsTreeButton = Button(
            self._buttonsFrame,text="Toggle Nets (Tree)", width=20,
            command= lambda:self._draw_nets(drawP2P=False)
        )
        toggleNetsTreeButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        toggleBinsButton = Button(
            self._buttonsFrame,text="Toggle Bins", width=20,
            command= lambda:self._draw_bins()
        )
        toggleBinsButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        toggleBinsButton = Button(
            self._buttonsFrame,text="Toggle Blockages", width=20,
            command= lambda:self._draw_blockages()
        )
        toggleBinsButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        binsHeatmapButton = Button(
            self._buttonsFrame,text="Routing Bins Heatmap", width=20,
            command= lambda:self.heatmap(self._design.bins, "Routing Bins")
        )
        binsHeatmapButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        elementBinsHeatmapButton = Button(
            self._buttonsFrame,text="Component Bins Heatmap", width=20,
            command= lambda:self.heatmap(self._design.componentBins, "Component Bins")
        )
        elementBinsHeatmapButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1
    
        blockagesHeatmapButton = Button(
            self._buttonsFrame,text="Blockages Heatmap", width=20,
            command= lambda:self.heatmap(self._design.blockages, "Blockages")
        )
        blockagesHeatmapButton.grid(row=rowNumber, column=0, columnspan=2, sticky="N")
        rowNumber += 1

        seperator = Separator(self._buttonsFrame, orient='horizontal')
        seperator.grid(row=rowNumber, column=0, columnspan=2, sticky="EW", pady=5)
        rowNumber += 1

        higlightTreeButton = Button(
            self._buttonsFrame, text="Highlight Tree", height=1,
            command= lambda:self._highlight_net(drawP2P=False),width= 10
        )
        higlightTreeButton.grid(row=rowNumber, column=0, sticky="N")

        self.netSearch = Entry(self._buttonsFrame, width=10)
        self.netSearch.grid(row=rowNumber, column=1, sticky="N")
        rowNumber += 1

        highlightP2PButton = Button(
            self._buttonsFrame, text="Highlight P2P", height=1,
            command= lambda:self._highlight_net(),width= 10
        )
        highlightP2PButton.grid(row=rowNumber, column=0, sticky="N")

        clearHighlightButton = Button(
            self._buttonsFrame, text="Clear", height=1,
            command=lambda:self._clear_highlight(),width= 10
        )
        clearHighlightButton.grid(row=rowNumber, column=1, sticky="N")
        rowNumber += 1
    # End of method

    def _draw_gui(self):
        """Method used for drawning the GUI"""

        if (self._design == None):
            Label(self, text="There is no design loaded",font=("Arial", 40)
                  ).place(x=(self._width/2),y=(self._height/2), anchor="center")
            return

        self._canvas = Canvas(self,width = self._CanvasWidth,
                               height = self._CanvasHeight)
        self._canvas.grid(row=0, column=1, rowspan=20, sticky="nswe", 
                          padx=5, pady=5)
        self._draw_core()

        # Core Information
        self._infoFrame = Frame(self, width=150, height=150)
        self._infoFrame.grid(row=0, column=0,sticky="NSEW", padx=10, pady=15)
        self._draw_core_info()

        # Bins Information
        self._binsFrame = Frame(self, width=150, height=50)
        self._binsFrame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=5)
        self._draw_bins_info()

        # Buttons
        self._buttonsFrame = Frame(self, width=150, height= 350)
        self._buttonsFrame.grid(row=2, column=0, sticky="NSEW", padx=10, pady=5)
        self._draw_buttons()
        
    # End of method

    def mainloop(self, n: int = 0):
        self._draw_gui()
        super().mainloop(n)
    # End of method
# End of class