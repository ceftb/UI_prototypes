# import the library
from appJar import gui

acn=0

actors=dict()
behaviors=dict()
constraints=dict()
events=dict()
actions=dict()

sbuttons=dict()
slabels=dict()

# handle button events
def press(button):
    print(button)

def tbFunc(button):
    global acn

    print(button)
    if (button == "ACTOR"):
        delim=""
        text = app.getTextArea("actor")        
        if (not text.endswith("\n") and text != ""):
            delim="\n"
        app.setTextArea("actor", delim+"actor"+str(acn), True, True)
        acn=acn+1
    if (button == "BEHAVIOR"):
        delim=""
        text = app.getTextArea("behavior")        
        if (not text.endswith("\n") and text != ""):
            delim="\n"
        app.setTextArea("behavior", delim+"condition actor action method effect", True, True)
    pass

def Bentry(button):
    pressed = button
    text = app.getTextArea("behavior")        
    delim = ""
    if (not text.endswith(" ") and text != ""):
        delim=" "
    app.setTextArea("behavior", delim+button, True, True)
    pass

def Centry(button):
    pressed = button
    text = app.getTextArea("constraints")        
    delim = ""
    if (not text.endswith(" ") and not text.endswith("\n") and text != ""):
        delim=" "
    app.setTextArea("constraints", delim+button, True, True)
    pass

def addSuggestions(evtype, pb):
    app.openLabelFrame("Suggestions")
    if evtype == "actors_only":
        for a in actors:
            if a != "":
                print "add actor ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
    elif evtype == "events_only":
        for e in events:
            if e != "":
                sbuttons[e] = 1
                app.addButton(e, pb)
    elif evtype == "behaviors_enter":
        for a in actors:
            if a != "":
                print "add actor ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
        for e in events:
            eline="when "+e
            sbuttons[eline] = 1
            app.addButton(eline, pb)
        for s in ["wait 1","wait 10", "wait 60"]:
            sbuttons[s] = 1
            app.addButton(s, pb)
    else: # it was text to be displayed as label
        app.addLabel("tl",evtype)
        slabels["tl"] = 1
    app.stopLabelFrame()

def processConstraints():
        print "Entered constraints"
        app.openLabelFrame("Suggestions")
        for t in sbuttons:
            app.removeButton(t)
        sbuttons.clear()
        for t in slabels:
            app.removeLabel(t)
        slabels.clear()
        text = app.getTextArea("constraints")
        cs = text.split(" ")
        if cs[-1] in ["num", "os","nodetype", "interfaces", "location", "link","lan"]:
            addSuggestions("actors_only", Centry)
        elif len(cs) >= 2:
            if (cs[-2] == "num" or cs[-2] == "interfaces") and cs[-1] in actors:
                addSuggestions("enter digit", Centry)
            elif cs[-2] == "os" and cs[-1] in actors:
                addSuggestions("enter OS", Centry)
            elif cs[-2] == "link" and cs[-1] in actors:
                addSuggestions("actors_only", Centry)
            elif cs[-2] == "lan" and cs[-1] in actors:
                addSuggestions("actors_only", Centry)
            elif cs[-2] == "location" and cs[-1] in actors:
                addSuggestions("enter testbed", Centry)
            else:
                for l in ["num", "os","link","lan","interfaces","location","topo"]:
                    app.addButton(l,Centry)
                    sbuttons[l]=1
        else:
            for l in ["num", "os","link","lan","interfaces","location","topo"]:
                app.addButton(l,Centry)
                sbuttons[l]=1
        app.stopLabelFrame()

def processBehavior():
        print "Entered behavior"
        app.openLabelFrame("Suggestions")
        for t in sbuttons:
            app.removeButton(t)
        sbuttons.clear()
        for t in slabels:
            app.removeLabel(t)
        slabels.clear()
        text = app.getTextArea("behavior")
        bhs = text.split("\n")
        i=0
        events.clear()
        for b in bhs:
            behaviors[i] = b
            i = i + 1
            items = b.split(" ")
            # parse out events
            prev = ""
            for item in items:
                if (item == "emit"):
                    prev = item
                    continue
                if (prev == "emit"):
                    events[item] = 1
                prev = item
        print "Len ", len(bhs)
        if len(bhs) >= 1:
            if bhs[-1] == "when":
                addSuggestions("events_only", Bentry)
            elif bhs[-1] in actors:
                addSuggestions("enter action", Bentry)
            elif bhs[-1] in events:
                addSuggestions("actors_only", Bentry)
            elif len(bhs) >= 2:
                if (bhs[-2] == "emit" and bhs[-1] in events):
                    addSuggestions("behaviors_enter", Bentry)
                elif (bhs[-1] in actions):
                    addSuggestions("enter method", Bentry)
                else: 
                    addSuggestions("behaviors_enter", Bentry)
            else:
                print "Will add behaviors enter"
                addSuggestions("behaviors_enter", Bentry)
        else:
            print "Will add behaviors enter"
            addSuggestions("behaviors_enter", Bentry)
        app.stopLabelFrame()

def regenerateSuggestions(evtype):
    print "Event ",evtype
    for t in sbuttons:
        print "Button ",t
    if evtype == "behaviors_enter":
        processBehavior()
    elif evtype == "actors_enter":
        print "Entered actors"
        app.openLabelFrame("Suggestions")
        for t in sbuttons:
            app.removeButton(t)
        sbuttons.clear()
        for t in slabels:
            app.removeLabel(t)
        slabels.clear()
        app.stopLabelFrame()
    elif evtype == "constraints_enter":
        processConstraints()

def actorentered(widget):
    entered("actor")

def actorleft(widget):
    left("actor")

def behaviorentered(widget):
    entered("behavior")

def behaviorleft(widget):
    left("behavior")

def constraintsentered(widget):
    entered("constraints")

def constraintsleft(widget):
    left("constraints")

def left(widget):
    print widget
    if (widget == "actor"):
        text = app.getTextArea("actor")
        roles = text.split("\n")
        for r in roles:
            if r not in actors:
                actors[r] = 1
                print "Added actor ", r
    if (widget == "behavior"):
        text = app.getTextArea("behavior")
        bhs = text.split("\n")
        i=0
        events.clear()
        for b in bhs:
            behaviors[i] = b
            i = i + 1
            items = b.split(" ")
            # parse out events
            prev = ""
            for item in items:
                if (item == "emit"):
                    prev = item
                    continue
                if (prev == "emit"):
                    events[item] = 1
                prev = item

def entered(widget):
    print widget
    if (widget == "actor"):
        regenerateSuggestions("actors_enter")        
    elif (widget == "behavior"):
        regenerateSuggestions("behaviors_enter")
    elif (widget == "constraints"):
        regenerateSuggestions("constraints_enter")


def changed(widget):
    if (widget == "actor"):
        pass
    if (widget == "behavior"):
        processBehavior()
    if (widget == "constraints"):
        processConstraints()

# create a GUI variable called app
app = gui("Experiment","600x400")
app.setBg("white")
app.setFont(18)
app.setSticky("news")
app.setStretch("both")
tools = ["ACTOR", "BEHAVIOR", "CONSTRAINT"]


app.addToolbar(tools, tbFunc, findIcon=True)
app.startLabelFrame("Actors", 0,0)
app.setSticky("ew")
app.setStretch("both")
app.addScrolledTextArea("actor")
app.setTextAreaTooltip("actor","actors")
#app.setTextAreaOverFunction("actor",[entered, left])
app.getTextAreaWidget("actor").bind("<FocusOut>", actorleft, add="+")
app.getTextAreaWidget("actor").bind("<FocusIn>", actorentered, add="+")
app.stopLabelFrame()
app.startLabelFrame("Behavior", 1,0)
app.setSticky("ew")
app.setStretch("column")
app.addScrolledTextArea("behavior")
app.setTextAreaTooltip("behavior","behavior")
app.getTextAreaWidget("behavior").bind("<FocusOut>", behaviorleft, add="+")
app.getTextAreaWidget("behavior").bind("<FocusIn>", behaviorentered, add="+")
#app.setTextAreaOverFunction("behavior",[entered, left])
app.setTextAreaChangeFunction("behavior",changed)
app.stopLabelFrame()
app.startLabelFrame("Constraints", 2,0)
app.setSticky("ew")
app.setStretch("column")
app.addScrolledTextArea("constraints")
app.setTextAreaTooltip("constraints","constraints")
#app.setTextAreaOverFunction("constraints",[entered, left])
app.getTextAreaWidget("constraints").bind("<FocusOut>", constraintsleft, add="+")
app.getTextAreaWidget("constraints").bind("<FocusIn>", constraintsentered, add="+")
app.setTextAreaChangeFunction("constraints",changed)
app.stopLabelFrame()
app.startLabelFrame("Suggestions", 0,1,3,3)
app.setSticky("ew")
app.setStretch("column")
app.setLabelFrameOverFunction("Suggestions",[None, left])
app.stopLabelFrame()

# start the GUI
app.go()
