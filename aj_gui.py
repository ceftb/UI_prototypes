# import the library
from appJar import gui

acn=0
tcn=0

actors=dict()
behaviors=dict()
constraints=dict()
events=dict()
actions=dict()

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
    elif evtype == "events_only":
        for e in events:
            if e != "":
                sbuttons[e] = 1
                app.addButton(e, pb)
    elif evtype == "behaviors_enter":
        print "Actors ",len(actors)
        for a in actors:
            if a != "":
                print "add actor ",a
                sbuttons[a] = 1
                app.addButton(a, pb)
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

    #print "Entering w state ",bstate, "line ",ll
    if (bstate == "start" or bstate == "done"):
        if (ll.strip() == ""):
            bstate = "start"
        elif (ll.strip() == "wait"):
            bstate = "waitd"
        elif (ll.strip() == "when"):
            bstate = "whene"
        elif (ll.strip() in actors):
            bstate = "actor"
        elif (ll.endswith(" ")): # new actor that someone added
            actors[ll.strip()] = 1 
            bstate = "actor"
            text = app.getTextArea("actor")        
            delim = ""
            if (not text.endswith("\n") and text != ""):
                    delim="\n"
            app.setTextArea("actor", delim+ll.strip(), True, True)
            if ("actor"+str(acn)) in actors:
                acn=acn+1
    elif (bstate == "waitd"):
        if(ll.endswith(" ")):
            items = ll.split(" ")
            print "came here len",len(items)
            if (len(items) >= 2):
                bstate = "wait"
    elif (bstate == "whene"):
        if ll.endswith(" "):
            items = ll.split(" ")
            if (len(items) == 2):
                bstate = "when"
    elif (bstate == "wait" or bstate == "when"):
        items = ll.split(" ")
        iteme = ll.strip().split(" ")
        leni = len(iteme)
        if (bstate == "wait" and ll.startswith("when")):
            adjust = 4
        elif (bstate == "wait" or bstate == "when"):
            adjust = 2
        if leni - adjust == 1:
            print " last item ",iteme[adjust]
            if (iteme[adjust] in actors):
                bstate = "actor"
            elif (iteme[adjust] == "wait"):
                bstate = "waitd"
            elif ll.endswith(" "): # new actor that someone added
                actors[iteme[-1]] = 1 
                bstate = "actor"
                text = app.getTextArea("actor")        
                delim = ""
                if (not text.endswith("\n") and text != ""):
                    delim="\n"
                app.setTextArea("actor", delim+iteme[-1], True, True)
                if ("actor"+str(acn)) in actors:
                    acn=acn+1
    return bstate

def processBehavior():
        global bstate
        global acn

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
        # Go through last behavior line to see what is the current state
        # start (waitd, wait) or (whene, when) or actor, actor, action, method, emit, done
        ll = bhs[-1]
        bstate = transitionBstate(ll)
        print "Bstate ",bstate
            
        chs = bhs[-1].strip().split(" ")
        print "Len ", len(chs)
        if len(chs) >= 1:
            if chs[-1] == "when":
                addSuggestions("events_only", Bentry)
            elif chs[-1] in actors:
                print "Found actor ",chs[-1]
                addSuggestions("enter action", Bentry)
                addSuggestions("actions_only", Bentry)
            elif chs[-1] in events:
                addSuggestions("actors_only", Bentry)
            elif chs[-1] == "emit":
                addSuggestions("enter event name", Bentry)
            elif len(chs) >= 2:
                if (chs[-2] == "emit" and chs[-1] in events):
                    addSuggestions("behaviors_enter", Bentry)
                elif (chs[-2] in actors and text.endswith(" ")):
                    actions[chs[-1]] = 1
                    addSuggestions("enter method", Bentry)
                elif len(chs) >= 3 and (chs[-3] in actors):
                    addSuggestions("emit", Bentry)
                    addSuggestions("behaviors_enter", Bentry)
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
