import networkx as nx
import sys
from appJar import gui

try:
    # Python 3
    import tkinter as tk
    import tkinter.messagebox as tkm
    import tkinter.simpledialog as tkd
    from tkinter.font import Font
except ImportError:
    # Python 2
    from tkFont import Font
    import Tkinter as tk
    import tkMessageBox as tkm
    import tkSimpleDialog as tkd


sys.path.append("..")

import globals
from netxCanvas.canvas import netxCanvas, GraphCanvas
from netxCanvas.style import NodeClass
from HighLevelBehaviorLanguage.hlb_parser import HLBParser

class dgStyle(NodeClass):
    def render(self, data, node_name):
        # Figure out what size the text we want is.
        label_txt = data.get('label', None)
        if label_txt:
            font = Font(family="Purisa", size=12)
            h = font.metrics("linespace")
            w = font.measure(label_txt)
        else:
            w=20
            h=20
        self.config(width=w, height=h)
        marker_options = {'fill': data.get('color','red'), 'outline':    'black'}
        
        if data.get('circle', None):
            self.create_oval(0,0,w,h, **marker_options)
        else:
            self.create_rectangle(0,0,w,h, **marker_options)
            if label_txt:
                self.create_text(w/2, h/2, text=label_txt)

class dependencyGraphHandler(GraphCanvas, object):
    added_behaviors = []
    
    def __init__(self, canvas, width=0, height=0, **kwargs):
        G = nx.Graph()
        G.add_node(0)
        G.node[0]['label'] = 'start'
        G.node[0]['actors'] = []
        G.node[0]['emits'] = ['startTrigger', 't0']
        G.node[0]['triggeredby'] = []
        G.node[0]['color'] = 'green'
        #G.add_edge(0,1)
        
        try:
            # Python3
            super().__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)
        except TypeError:
            # Python 2
            super(dependencyGraphHandler, self).__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)

        self.pack() 
        
        self.parser = HLBParser()
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.xoffset = xoffset
        self.yoffset = yoffset

    def add_new_behavior(self, statement):
        # XXX TODO Need to handle removals.
        statement = statement.strip()
        if statement not in self.added_behaviors:
            self.added_behaviors.append(statement)
        (t_events, actors, action, e_events, wait_time) = self.parser.parse_stmt(statement)
        if actors != None:	
            # We successfully parsed the statement.
            if t_events != None and wait_time != None:
                print("We have a when/wait statement.")
            else:	
                if t_events != None:
                    print("Triggered by: %s" % t_events)
                elif wait_time != None:	
                    print("Triggered by wait of: %s" % wait_time)
                else:
                    print("Triggered by start.")
                    
        # Add node
        num_nodes = len(self.G)
        self.G.add_node(num_nodes)
        self.G.node[num_nodes]['actors'] = actors
        try:
            self.G.node[num_nodes]['label'] = ''.join(action)
        except TypeError:
            self.G.node[num_nodes]['label'] = action
        if e_events != None:
            self.G.node[num_nodes]['emits'] = e_events
        else:
            self.G.node[num_nodes]['emits'] = []
        if t_events != None:	
            self.G.node[num_nodes]['triggeredby'] = t_events
        else:	
            self.G.node[num_nodes]['triggeredby'] = ['startTrigger']
        self.G.node[num_nodes]['color'] = 'blue'
        
        # Go through emits and make connections.
        for e in self.G.node[num_nodes]['emits']:
            for n in self.G.nodes():
                for t in self.G.nodes[n]['triggeredby']:
                    if t.strip() == e:
                        self.G.add_edge(num_nodes, n)
                
        # Go through triggeredby and make connections.
        for t in self.G.node[num_nodes]['triggeredby']:
            for n in self.G.nodes():
                for e in self.G.nodes[n]['emits']:
                    if e.strip() == t:
                        self.G.add_edge(n, num_nodes)
        
        self._plot_additional(self.G.node[num_nodes])
        self._plot_additional([num_nodes])
        self.refresh()

    def add_dependency(self, name, connections=[]):
        if self.find_label(name) != None:
            return
                
        self.G.add_node(num_nodes)
        self.G.node[num_nodes]['label'] = name
        for name in connections:
            node = self.find_label(name)
            if node != None:
                self.G.add_edge(node, num_nodes)
        
        self._plot_additional(self.G.node[num_nodes])
        self._plot_additional([num_nodes])
        self.refresh()

    def find_label(self, name):
        for n in G.nodes():
            data.get('label', None)
            if label:
                if label == name:
                    return n
        return None
   
   #def add_hlb_line(line):
   #    if line in self.processed
   