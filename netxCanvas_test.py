import networkx as nx
import sys
from appJar import gui

sys.path.append(".")

from netxCanvas.canvas import netxCanvas
from netxCanvas.style import NodeClass


app = gui("Graph Testing")

class CustomNodeStyle(NodeClass):
    def render(self, data, node_name):
        self.config(width=10, height=10)
        marker_options = {'fill': data.get('color','red'), 'outline':    'black'}
        
        if data.get('circle', None):
            self.create_oval(0,0,10,10, **marker_options)
        else:
            self.create_rectangle(0,0,10,10, **marker_options)

G = nx.Graph()
G.add_edge(0,1)
G.add_edge(0,2)
G.add_edge(0,3)

G.node[0]['circle'] = True
G.node[1]['color'] = 'green'

app.setGeometry(600, 300)
app.addCanvas("Graph!")
gc_master = app.getCanvas("Graph!")

gc = netxCanvas(G, master=gc_master, style=CustomNodeStyle, width=300, height=500)

app.go()

