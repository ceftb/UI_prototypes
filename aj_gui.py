# import the library
from appJar import gui
import re
from HighLevelBehaviorLanguage.hlb import *
import globals

# create a GUI variable and assign our app var
globals.app = gui("Experiment","800x660")
globals.app.setBg("white")
globals.app.setFont(18)
globals.app.setSticky("news")
globals.app.setStretch("both")

# The tool bar is cool, but will be present across all tabs (not sure we want that)
# To have these buttons on *just* one tab, we should create a row of individual buttons.
tools = ["ACTOR", "BEHAVIOR", "CONSTRAINT"]
#globals.app.addToolbar(tools, tbFunc, findIcon=True)

# XXX TODO: Clean up and add more structure here.

globals.app.startTabbedFrame("TabbedArea")
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
globals.app.stopTab()

## TAB 4
globals.app.startTab("Topology")
globals.app.stopTab()

globals.app.stopTabbedFrame()

# start the GUI
globals.app.go()
