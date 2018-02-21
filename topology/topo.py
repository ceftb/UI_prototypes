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


class topoStyle(NodeClass):
    def render(self, data, node_name):
        self.config(width=10, height=10)
        marker_options = {'fill': data.get('color','red'), 'outline':    'black'}
        
        if data.get('circle', None):
            self.create_oval(0,0,10,10, **marker_options)
        else:
            self.create_rectangle(0,0,10,10, **marker_options)

class topoHandler():
    def __init__(self, canvas, width=0, height=0, **kwargs):
        self.G = nx.Graph()
        self.G.add_edge(0,1)
        self.G.add_edge(0,2)
        self.G.add_edge(0,3)

        self.G.node[0]['circle'] = True
        self.G.node[0]['color'] = 'green'
        self.G.node[1]['color'] = 'blue'

        #self.gc = netxCanvas(self.G, master=canvas,  style=dgStyle, width=width, height=height)
        self.gc = GraphCanvas(self.G, master=canvas, width=width, height=height, NodeClass=topoStyle, **kwargs)
        #self.gc.grid(row=0, column=0, sticky='NESW')
        self.gc.pack()
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.gc.xoffset = xoffset
        self.gc.yoffset = yoffset

    def add_entity(self, name):
        num_nodes = len(self.G)
        print("Topology adding %s (have %d nodes currently)" % (name,num_nodes))
        print("Now have %d nodes." % (len(self.G)))
        print("Refreshing")
        self.G.add_node(num_nodes, label=name)
        self.G.add_edge(0, num_nodes)

        self.gc._plot_additional(self.G.node[num_nodes])
        self.gc._plot_additional([num_nodes])
        self.gc.refresh()
        
