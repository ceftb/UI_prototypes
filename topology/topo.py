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

class topoHandler(GraphCanvas, object):
    def __init__(self, canvas, width=0, height=0, **kwargs):
        G = nx.Graph()
   
        G.add_node(0, label='lan')
        G.add_edge(0,1)
        G.add_edge(0,2)
        G.add_edge(0,3)

        G.node[0]['circle'] = True
        G.node[0]['color'] = 'green'
        G.node[1]['color'] = 'blue'
        try:
            # Python 3
            super().__init__(G, master=canvas, width=width, height=height, NodeClass=topoStyle, **kwargs)
        except TypeError:
            # Python 2
            super(topoHandler, self).__init__(G, master=canvas, width=width, height=height, NodeClass=topoStyle, **kwargs)
        self.pack()
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.xoffset = xoffset
        self.yoffset = yoffset

    def add_entity(self, name, connections=['lan0']):
        num_nodes = len(self.G)
        print("Topology adding %s (have %d nodes currently)" % (name,num_nodes))
        print("Now have %d nodes." % (len(self.G)))
        print("Refreshing")
        self.G.add_node(num_nodes, label=name)
        #for name in connections:
        #    node = self.find_label(name)
        #    self.G.add_edge(node, num_nodes)

        self._plot_additional(self.G.node[num_nodes])
        self._plot_additional([num_nodes])
        self.refresh()
    
    def save(self, f):
        l=0
        lans=dict()
        num_nodes = len(self.G)
        print("Have %d nodes ", (num_nodes))
        nodes = nx.get_node_attributes(self.G, 'label')
        for n in nodes:
            f.write("node:\n")
            f.write("\tid: " + str(n) + '\n')
            f.write("\tendpoints: [" + nodes[n] + ']\n')
            f.write("\tprops: {}\n")
        edges = nx.edges(self.G);
        for e in edges:
            if nodes[e[0]].startswith("lan"):
                if e[0] not in lans:
                    lans[e[0]] = []
                lans[e[0]].append(e[1])
                print lans[e[0]]
            else:
                f.write("link:\n")
                f.write("\tid: link" + str(l) + '\n')
                l=l+1
                f.write("\tendpoints: [[" + nodes[e[0]] + "],[" + nodes[e[1]]+"\n")
                f.write("\tprops: {}\n");
        for n in lans:
            f.write("net:\n")
            f.write("\tid: " + str(n) + '\n')
            f.write("\tnodes: [")
            first = 0
            for i in lans[n]:
                if first == 1:
                    f.write(",")
                first = 1
                f.write(str(i));
            f.write("]\n");
            
