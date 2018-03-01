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
            font = Font(family="Helvetica", size=12)
            h = font.metrics("linespace") + 1
            w = font.measure(label_txt) + 2
        else:
            w=20
            h=20
        self.config(width=w, height=h)
        marker_options = {'fill': data.get('color','blue'), 'outline': 'white'}
        
        if data.get('circle', None):
            self.create_oval(0,0,w*2,h*2, **marker_options)
        else:
            self.create_rectangle(0,0,w,h, **marker_options)
        if label_txt:
            self.create_text(w/2, h/2, text=label_txt, font=font, fill="white")

class dependencyGraphHandler(GraphCanvas, object):
    added_behaviors = []
    
    def __init__(self, canvas, width=0, height=0, **kwargs):
        G = nx.Graph()
        G.add_node(0)
        G.node[0]['label'] = '*'
        G.node[0]['actors'] = []
        G.node[0]['emits'] = ['startTrigger', 't0']
        G.node[0]['triggeredby'] = []
        G.node[0]['color'] = 'green'
        G.node[0]['circle'] = True
        #G.add_edge(0,1)
        
        try:
            # Python3
            super().__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)
        except TypeError:
            # Python 2
            super(dependencyGraphHandler, self).__init__(G, master=canvas, width=width, height=height, NodeClass=dgStyle, **kwargs)

        #self._draw_node((width, height), 0)
        self.pack()  
        self.parser = HLBParser()
    
    def setoffsets(self, xoffset=0, yoffset=0):
        self.xoffset = xoffset
        self.yoffset = yoffset
        
    def dict_from_behaviors(self):
        # Creates a graph from the current listed behaviors.
        bdict = {}
        for b in globals.behaviors:
            statement = globals.behaviors[b]
            (t_events, actors, action, e_events, wait_time) = self.parser.parse_stmt(statement)
            try:
                action = ''.join(action)
            except TypeError:
                pass
            if actors == None:	
                # We failed to parse the statement, so skip it.
                continue
            if t_events == None:
                t_events = ['startTrigger']
            if e_events == None:
                e_events = []

            # action = [[t_events], [e_events], [actors]]
            if action in bdict:
                i = 0
                for tup in bdict[action]:
                    if set(t_events) == set(tup[0]) and set(e_events) == set(tup[1]):
                        bdict[action][i][2] = list(set(bdict[action][i][2] + actors))
                    i = i + 1
            else:
                # easy add, we know we have no duplicates.
                bdict[action] = []
                bdict[action].append([list(set(t_events)),list(set(e_events)), list(set(actors))])

        return bdict
   
    def add_new_node(self, actors, action, e_events, t_events):     
        # Add node to new graph
        num_nodes = len(self.G)
        self.G.add_node(num_nodes)
        self.G.node[num_nodes]['actors'] = list(set(actors))
        try:
            self.G.node[num_nodes]['label'] = ''.join(action)
        except TypeError:
            self.G.node[num_nodes]['label'] = action
        if e_events != None:
            self.G.node[num_nodes]['emits'] = list(set(e_events))
        else:
            self.G.node[num_nodes]['emits'] = []
        if t_events != None:	
            self.G.node[num_nodes]['triggeredby'] = list(set(t_events))
        else:	
            print("Triggered by start.")
            self.G.node[num_nodes]['triggeredby'] = ['startTrigger']
        self.G.node[num_nodes]['color'] = 'blue'
    
        # self.Go through emits and make connections.
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
                        if n not in self.G.neighbors(num_nodes):
                            self.G.add_edge(num_nodes, n)
        return num_nodes
    

    def plot_changes(self, newdict):
        # First go through and remove nodes that have disappeared.
        remove_nodes = []
        for n in self.G:
            found = False
            Glabel = self.G[n].get('label', 'XXNONEXX')
            if Glabel in newdict:
                i = 0
                for tup in newdict[Glabel]:
                    if set(self.G[n]['triggeredby']) == set(tup[0]) and set(self.G[n]['e_events']) == set(tup[1]):
                        found = True
                        self.G[n]['actors'] = list(set(newdict[Glabel][i][2]))
                        break
                    i = i + 1
            if found:
                # Remove the found info from the newdict since we don't want to add duplicate nodes.
                newdict[action].delete(tup)
                if len (newdict[action]) == 0:
                    newdict.delete(action)
            if not found and n != 0:
                # Remove node if it's not in our new graph and not our start node.
                remove_nodes.append(n)
    
        for n in remove_nodes:
            self.remove_node(n)
        if len(remove_nodes) > 0:
            #XXX TODO this should be a refresh, not a full replot.
            self.plot(0)
            self._plot_additional(self.G.nodes())
        
        new = []
        for label in newdict:
            for tup in newdict[label]:
                # Add this new node to our data graph and plot list.
                new_id = self.add_new_node(set(tup[2]), label, set(tup[1]), set(tup[0]))
                new.append(new_id)

        if len(new) > 0:
            self._plot_additional(new)
    
        #self.refresh()

    def add_new_behavior(self, statement):
        # Create new graph:
        new = self.dict_from_behaviors()
        self.plot_changes(new)
        
        
        #self.plot(0)
        #self._plot_additional(self.G.nodes())
        #self._plot_additional([num_nodes])
        #self.refresh()
    

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
   