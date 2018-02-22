import networkx as nx
import sys
from appJar import gui

try:
    # Python 3
    import tkinter as tk
    import tkinter.messagebox as tkm
    import tkinter.simpledialog as tkd
except ImportError:
    # Python 2
    import Tkinter as tk
    import tkMessageBox as tkm
    import tkSimpleDialog as tkd


sys.path.append("..")

import globals
from netxCanvas.canvas import netxCanvas, GraphCanvas
from netxCanvas.style import NodeClass


class dgStyle(NodeClass):
    def render(self, data, node_name):
        self.config(width=10, height=10)
        marker_options = {'fill': data.get('color','red'), 'outline':    'black'}
        
        if data.get('circle', None):
            self.create_oval(0,0,10,10, **marker_options)
        else:
            self.create_rectangle(0,0,10,10, **marker_options)

class dependencyGraphHandler():
    def __init__(self, canvas, width=0, height=0, **kwargs):
        self.G = nx.Graph()
        self.G.add_node(0)
        self.G.node[0]['label'] = 'start'

        #self.gc = netxCanvas(self.G, master=canvas,  style=dgStyle, width=width, height=height)
        self.gc = GraphCanvas(self.G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)
        #self.gc.grid(row=0, column=0, sticky='NESW')
        self.gc.pack()
        #for item in self.gc.find_all():
        #    print("Item:\t")
        #    print(item)
        #    print("Coords")
        #    print(self.gc.coords(item))
        #self.gc.pack()
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.gc.xoffset = xoffset
        self.gc.yoffset = yoffset

