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

class dependencyGraphHandler(GraphCanvas, object):
    def __init__(self, canvas, width=0, height=0, **kwargs):
        G = nx.Graph()
        G.add_node(0)
        G.node[0]['label'] = 'start'
       
        try:
            # Python3
            super().__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)
        except TypeError:
            # Python 2
            super(dependencyGraphHandler, self).__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)

        self.pack()    
    
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.xoffset = xoffset
        self.yoffset = yoffset

