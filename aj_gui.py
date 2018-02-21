import inspect as ins
import pprint
# import the library
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


from appJar import gui
import re
from HighLevelBehaviorLanguage.hlb import *
from dependencyGraph.dg import dependencyGraphHandler
from topology.topo import topoHandler
import globals

# create a GUI variable and assign our app var
globals.app = gui("Experiment","800x600")
globals.app.setResizable(canResize=True)
globals.app.setBg("white")
globals.app.setFont(18)
globals.app.setSticky("news")
globals.app.setStretch("both")

# The tool bar is cool, but will be present across all tabs (not sure we want that)
# To have these buttons on *just* one tab, we should create a row of individual buttons.
tools = ["ACTOR", "BEHAVIOR", "CONSTRAINT"]
#globals.app.addToolbar(tools, tbFunc, findIcon=True)

# XXX TODO: Clean up and add more structure here.

tabbed_frame = globals.app.startTabbedFrame("TabbedArea")


## Tab1
globals.app.startTab("HLB")
globals.app.startLabelFrame("Actors", 0,0)
globals.app.setSticky("ew")
globals.app.setStretch("both")
globals.app.addScrolledTextArea("actor")
globals.app.setTextAreaTooltip("actor","actors")
#globals.app.setTextAreaOverFunction("actor",[entered, left])
globals.app.getTextAreaWidget("actor").bind("<FocusOut>", actorleft, add="+")
globals.app.getTextAreaWidget("actor").bind("<FocusIn>", actorentered, add="+")
globals.app.stopLabelFrame()
globals.app.startLabelFrame("Behavior", 1,0)
globals.app.setSticky("ew")
globals.app.setStretch("column")
globals.app.addScrolledTextArea("behavior")
globals.app.setTextAreaTooltip("behavior","behavior")
globals.app.getTextAreaWidget("behavior").bind("<FocusOut>", behaviorleft, add="+")
globals.app.getTextAreaWidget("behavior").bind("<FocusIn>", behaviorentered, add="+")
#globals.app.setTextAreaOverFunction("behavior",[entered, left])
globals.app.setTextAreaChangeFunction("behavior",changed)
globals.app.stopLabelFrame()
globals.app.startLabelFrame("Constraints", 2,0)
globals.app.setSticky("ew")
globals.app.setStretch("column")
globals.app.addScrolledTextArea("constraints")
globals.app.setTextAreaTooltip("constraints","constraints")
#globals.app.setTextAreaOverFunction("constraints",[entered, left])
globals.app.getTextAreaWidget("constraints").bind("<FocusOut>", constraintsleft, add="+")
globals.app.getTextAreaWidget("constraints").bind("<FocusIn>", constraintsentered, add="+")
globals.app.setTextAreaChangeFunction("constraints",changed)
globals.app.stopLabelFrame()
globals.app.startLabelFrame("Suggestions", 0,1,3,3)
globals.app.setSticky("ew")
globals.app.setStretch("column")
globals.app.setLabelFrameOverFunction("Suggestions",[None, left])
globals.app.stopLabelFrame()
globals.app.stopTab()

## TAB 2
globals.app.startTab("NLP")
globals.app.stopTab()

## TAB 3
globals.app.startTab("Behavior Dependency Graph")
globals.bdg_canvas = globals.app.addCanvas("Behavior Dependency Graph")
init_width = int(globals.app.appWindow.winfo_screenwidth()*.75)
init_height = int(globals.app.appWindow.winfo_screenheight()*.75)
globals.bdg_canvas.config(width=init_width,height=init_height)
print("Width of GUI: %d" % globals.app.appWindow.winfo_screenwidth())
print("Requesting canvas width of %d" % init_width)
globals.bdg_handler = dependencyGraphHandler(globals.bdg_canvas, width=init_width, height=init_height)
print("Width of new canvas: %d" % globals.bdg_canvas.winfo_reqwidth())
globals.app.stopTab()

## TAB 4
globals.app.startTab("Topology")
globals.app.topo_canvas = globals.app.addCanvas("Topology")
init_width = int(globals.app.appWindow.winfo_screenwidth()*.75)
init_height = int(globals.app.appWindow.winfo_screenheight()*.75)
globals.app.topo_canvas.config(width=init_width,height=init_height)
globals.topo_handler = topoHandler(globals.app.topo_canvas, width=init_width, height=init_height)
globals.app.stopTab()

globals.app.stopTabbedFrame()

# XXX TODO: Not sure why working with appjar 
# doesn't give us correct event or winfo or canvasx/y coordinates.
# Appears to offset us by the height of the tab frame? 
# Which we need to get after creating full frame area.
ta = gknlobals.app.widgetManager.get(globals.app.Widgets.TabbedFrame, "TabbedArea")
tabbedHeight = ta.tabContainer.winfo_height()
globals.bdg_handler.setoffsets(yoffset=tabbedHeight)
globals.topo_handler.setoffsets(yoffset=tabbedHeight)

# start the GUI
globals.app.go()
