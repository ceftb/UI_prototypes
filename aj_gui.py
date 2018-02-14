# import the library
from appJar import gui
import re

acn=0
tcn=0

actors=dict()
behaviors=dict()
constraints=dict()
events=dict()
actions=dict()
methods=dict()

sbuttons=dict()
slabels=dict()

bstate = "start" # state of current behavior start, (waitd, wait) or (whene, when) or actor, actor, action, method, emit, done

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
    global tcn

    pressed = button
    text = app.getTextArea("behavior")        
    delim = ""
    if (not text.endswith(" ") and not text.endswith("\n") and text != ""):
        delim=" "
    if (button == "wait t"):
        button += str(tcn)
        tcn = tcn + 1
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
    global actors

    app.openLabelFrame("Suggestions")
    if evtype == "actors_only":
        for a in actors:
            if a != "":
                print "add actor ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
    elif evtype == "actions_only":
        for a in actions:
            if a != "":
                print "add action ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
    elif evtype == "methods_only":
        for a in methods:
            if a != "":
                sbuttons[a] = 1
                app.addButton(a, pb)
    elif evtype == "events_only":
        for e in events:
            if e != "":
                sbuttons[e] = 1
                app.addButton(e, pb)
    elif evtype == "behaviors_enter" or evtype == "when_enter":
        print "Actors ",len(actors)
        for a in actors:
            if a != "":
                print "add actor ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
        if evtype == "behaviors_enter":
            for e in events:
                eline="when "+e
                sbuttons[eline] = 1
                app.addButton(eline, pb)
        for s in ["wait t"]:
            sbuttons[s] = 1
            app.addButton(s, pb)
    elif evtype == "emit":
        sbuttons["emit"] = 1
        app.addButton("emit", pb)
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
        cs = text.strip().split(" ")
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

def transitionBstate(ll):
    global acn
    global bstate


    fwh=0
    fwa=0
    fa=0    
    fp=-1
    fe=0

    # first check what is there in the string
    items = ll.strip().split(" ")
    if (len(items) == 0):
        return "start"

    j = 0
    for i in items:
        it = i.strip(",")
        if it == "when":
            fwh = 1
            fp = j
        if it == "wait":
            fwa = 1
            fp = j
        if it in actors:
            fa = 1
            fp = j # position of the last actor
        if it == "emit":
            fe = 1
            fp = j
        j += 1

    diff = len(items) - fp - 1
    print "fwh ",fwh, " fwa ",fwa," fa ",fa, " fe ",fe," fp ",fp, " diff ",diff
    # now check what's the last item
    if (fwh == 1 and fwa == 0 and fa == 0):
        if (items[-1] != "when"):
            if diff == 1 and ll.endswith(" "):
                return "when"
            elif diff == 2 and (ll.endswith(" ") or ll.endswith(",")): # should add new actor
                return "nactor"
            else:
                return "when"
        else:
            return "whene"
    if (fwh == 1 and fwa == 1 and fa == 0) or (fwh == 0 and fwa == 1 and fa == 0):
        if (items[-1] != "wait"):
            if diff == 1 and ll.endswith(" "):
                return "wait"
            elif diff == 2 and (ll.endswith(" ") or ll.endswith(",")): # should add new actor
                return "nactor"
            else:
                return "wait"
        else:
            return "waitd"
    if (fa == 0 and fwh == 0 and fwa == 0):
        if (fp == -1):
            if (ll.endswith(" ") or ll.endswith(",")):
                return "nactor"
            else:
                return "start"
    if (fa == 1 and fe == 0):
        if diff == 0:
            return "actor"
        elif diff == 1:
            if ll.endswith(" "):
                return "naction"
            else:
                return "action"
        elif diff == 2:
            if ll.endswith(" ") or ll.endswith(","):
                return "nmethod"
            else:
                return "method"
        else:
            return "emit"
    if (fa == 1 and fe == 1):
        if (diff == 0):
            return "emite"
        else:
            return "emitted"
    return "wrong"

def addactor(item):
    global actors
    global acn

    actors[item] = 1
    if ("actor"+str(acn)) in actors:
        acn = acn+1

    delim=""
    text = app.getTextArea("actor")        
    if (not text.endswith("\n") and text != ""):
        delim="\n"
    app.setTextArea("actor", delim+item, True, True)

def processBehavior():
        global bstate
        global acn
        global actions
        global actors
        global methods

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
        # parse out events, actors, actions and methods
        # from every line but the last
        events.clear()
        ll = bhs.pop()
        for b in bhs:
            behaviors[i] = b
            i = i + 1
            items = re.split("[\s,]",b.strip())
            # parse out events
            fa = 0
            fe = 0
            d = 0
            for item in items:
                if item in actors:
                    fa = 1
                    continue
                if (item == "emit"):
                    fe = 1
                    continue
                if (fa == 1):
                    d = d+1
                    if (d == 1):
                        actions[item] = 1
                        continue
                    elif (d == 2):
                        methods[item] = 1
                        continue
                if (fe == 1):
                    events[item] = 1
        # Go through last behavior line to see what is the current state
        # start (waitd, wait) or (whene, when) or actor, actor, action, method, emit, done
        bstate = transitionBstate(ll)
        print "State ",bstate

        if (bstate == "start"):
            addSuggestions("behaviors_enter", Bentry)
        elif(bstate == "whene"):
            addSuggestions("enter event name", Bentry)
            addSuggestions("events_only", Bentry)
        elif(bstate == "when"):
            addSuggestions("when_enter", Bentry)
        elif(bstate == "waitd"):
            addSuggestions("enter variable name or wait time in second", Bentry)
        elif(bstate == "wait"):
            addSuggestions("actors_only", Bentry)
        elif(bstate == "actor" or bstate == "nactor"):
            if (bstate == "nactor"):
                items = ll.strip().split(" ")
                item = items[-1].strip(",")
                addactor(item)
            addSuggestions("enter action", Bentry)
            addSuggestions("actions_only", Bentry)
            addSuggestions("actors_only", Bentry)
        elif(bstate == "action" or bstate == "method" or bstate == "naction" or bstate == "nmethod"):
            items = ll.strip().split(" ")
            if (bstate == "naction"):
                actions[items[-1]] = 1
            addSuggestions("enter method", Bentry)
            addSuggestions("methods_only", Bentry)
            if (bstate == "nmethod"):
                item = items[-1].strip(",")
                methods[item] = 1
            if (bstate == "nmethod" or bstate == "method"):
                addSuggestions("emit", Bentry)
        elif (bstate == "emit"):
            addSuggestions("enter event name", Bentry)
        elif (bstate == "emitted"):
            addSuggestions("enter event name", Bentry)

#            elif chs[-1] in actors:
#                print "Found actor ",chs[-1]
#                addSuggestions("enter action", Bentry)
#                addSuggestions("actions_only", Bentry)
#            elif chs[-1] in events:
#                addSuggestions("actors_only", Bentry)
#            elif chs[-1] == "emit":
#                addSuggestions("enter event name", Bentry)
#            elif len(chs) >= 2:
#                if (chs[-2] == "emit" and chs[-1] in events):
#                    addSuggestions("behaviors_enter", Bentry)
#                elif (chs[-2] in actors and text.endswith(" ")):
#                    actions[chs[-1]] = 1
#                    addSuggestions("enter method", Bentry)
#                elif len(chs) >= 3 and (chs[-3] in actors):
#                    addSuggestions("emit", Bentry)
#                    addSuggestions("behaviors_enter", Bentry)
#                else: 
#                    addSuggestions("behaviors_enter", Bentry)
#            else:
#                print "Will add behaviors enter"
#                addSuggestions("behaviors_enter", Bentry)
#        else:
#            print "Will add behaviors enter"
#           addSuggestions("behaviors_enter", Bentry)
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
    global actors
    global events

    if (widget == "actor"):
        actors=dict()
        text = app.getTextArea("actor")
        roles = text.split("\n")
        for r in roles:
            if r not in actors and r.strip() != "":
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
