import sys
sys.path.append('../')
import globals

# handle button events
def press(button):
    print(button)

def tbFunc(button):

    print(button)
    if (button == "ACTOR"):
        delim=""
        text = globals.app.getTextArea("actor")        
        if (not text.endswith("\n") and text != ""):
            delim="\n"
        globals.app.setTextArea("actor", delim+"actor"+str(globals.acn), True, True)
        globals.acn=globals.acn+1
    if (button == "BEHAVIOR"):
        delim=""
        text = globals.app.getTextArea("behavior")        
        if (not text.endswith("\n") and text != ""):
            delim="\n"
        globals.app.setTextArea("behavior", delim+"condition actor action method effect", True, True)
    pass

def Bentry(button):
    pressed = button
    text = globals.app.getTextArea("behavior")        
    delim = ""
    if (not text.endswith(" ") and not text.endswith("\n") and text != ""):
        delim=" "
    if (button == "wait t"):
        button += str(globals.tcn)
        globals.tcn = globals.tcn + 1
    globals.app.setTextArea("behavior", delim+button, True, True)
    pass

def Centry(button):
    pressed = button
    text = globals.app.getTextArea("constraints")        
    delim = ""
    if (not text.endswith(" ") and not text.endswith("\n") and text != ""):
        delim=" "
    globals.app.setTextArea("constraints", delim+button, True, True)
    pass

def addSuggestions(evtype, pb):
    globals.app.openLabelFrame("Suggestions")
    if evtype == "actors_only":
        for a in globals.actors:
            if a != "":
                print "add actor ",a
                globals.sbuttons[a] = 1
                globals.app.addButton(a, pb)
    elif evtype == "actions_only":
        for a in actions:
            if a != "":
                print "add action ",a
                globals.sbuttons[a] = 1
                globals.app.addButton(a, pb)
    elif evtype == "methods_only":
        for a in globals.methods:
            if a != "":
                globals.sbuttons[a] = 1
                globals.app.addButton(a, pb)
    elif evtype == "events_only":
        for e in globals.events:
            if e != "":
                globals.sbuttons[e] = 1
                globals.app.addButton(e, pb)
    elif evtype == "behaviors_enter" or evtype == "when_enter":
        print "Actors ",len(globals.actors)
        for a in globals.actors:
            if a != "":
                print "add actor ",a
                globals.sbuttons[a] = 1
                globals.app.addButton(a, pb)
        if evtype == "behaviors_enter":
            for e in globals.events:
                eline="when "+e
                globals.sbuttons[eline] = 1
                globals.app.addButton(eline, pb)
        for s in ["wait t"]:
            globals.sbuttons[s] = 1
            globals.app.addButton(s, pb)
    elif evtype == "emit":
        globals.sbuttons["emit"] = 1
        globals.app.addButton("emit", pb)
    else: # it was text to be displayed as label
        globals.app.addLabel("tl",evtype)
        globals.slabels["tl"] = 1
    globals.app.stopLabelFrame()

def processConstraints():
        print "Entered constraints"
        globals.app.openLabelFrame("Suggestions")
        for t in globals.sbuttons:
            globals.app.removeButton(t)
        globals.sbuttons.clear()
        for t in globals.slabels:
            globals.app.removeLabel(t)
        globals.slabels.clear()
        text = globals.app.getTextArea("constraints")
        cs = text.strip().split(" ")
        if cs[-1] in ["num", "os","nodetype", "interfaces", "location", "link","lan"]:
            addSuggestions("actors_only", Centry)
        elif len(cs) >= 2:
            if (cs[-2] == "num" or cs[-2] == "interfaces") and cs[-1] in globals.actors:
                addSuggestions("enter digit", Centry)
            elif cs[-2] == "os" and cs[-1] in globals.actors:
                addSuggestions("enter OS", Centry)
            elif cs[-2] == "link" and cs[-1] in globals.actors:
                addSuggestions("actors_only", Centry)
            elif cs[-2] == "lan" and cs[-1] in globals.actors:
                addSuggestions("actors_only", Centry)
            elif cs[-2] == "location" and cs[-1] in globals.actors:
                addSuggestions("enter testbed", Centry)
            else:
                for l in ["num", "os","link","lan","interfaces","location","topo"]:
                    globals.app.addButton(l,Centry)
                    globals.sbuttons[l]=1
        else:
            for l in ["num", "os","link","lan","interfaces","location","topo"]:
                globals.app.addButton(l,Centry)
                globals.sbuttons[l]=1
        globals.app.stopLabelFrame()

def transitionBstate(ll):

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
        if it in globals.actors:
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

    globals.actors[item] = 1
    if ("actor"+str(globals.acn)) in globals.actors:
        globals.acn = globals.acn+1

    delim=""
    text = globals.app.getTextArea("actor")        
    if (not text.endswith("\n") and text != ""):
        delim="\n"
    globals.app.setTextArea("actor", delim+item, True, True)

def processBehavior():
        print "Entered behavior"
        globals.app.openLabelFrame("Suggestions")
        for t in globals.sbuttons:
            globals.app.removeButton(t)
        globals.sbuttons.clear()
        for t in globals.slabels:
            globals.app.removeLabel(t)
        globals.slabels.clear()
        text = globals.app.getTextArea("behavior")
        bhs = text.split("\n")
        i=0
        # parse out events, globals.actors, actions and methods
        # from every line but the last
        globals.events.clear()
        ll = bhs.pop()
        for b in bhs:
            globals.behaviors[i] = b
            i = i + 1
            items = re.split("[\s,]",b.strip())
            # parse out events
            fa = 0
            fe = 0
            d = 0
            for item in items:
                if item in globals.actors:
                    fa = 1
                    continue
                if (item == "emit"):
                    fe = 1
                    continue
                if (fa == 1):
                    d = d+1
                    if (d == 1):
                        globals.actions[item] = 1
                        continue
                    elif (d == 2):
                        globals.methods[item] = 1
                        continue
                if (fe == 1):
                    globals.events[item] = 1
        # Go through last behavior line to see what is the current state
        # start (waitd, wait) or (whene, when) or actor, actor, action, method, emit, done
        globals.bstate = transitionBstate(ll)
        print "State ",globals.bstate

        if (globals.bstate == "start"):
            addSuggestions("behaviors_enter", Bentry)
        elif(globals.bstate == "whene"):
            addSuggestions("enter event name", Bentry)
            addSuggestions("events_only", Bentry)
        elif(globals.bstate == "when"):
            addSuggestions("when_enter", Bentry)
        elif(globals.bstate == "waitd"):
            addSuggestions("enter variable name or wait time in second", Bentry)
        elif(globals.bstate == "wait"):
            addSuggestions("actors_only", Bentry)
        elif(globals.bstate == "actor" or globals.bstate == "nactor"):
            if (globals.bstate == "nactor"):
                items = ll.strip().split(" ")
                item = items[-1].strip(",")
                addactor(item)
            addSuggestions("enter action", Bentry)
            addSuggestions("actions_only", Bentry)
            addSuggestions("globals.actors_only", Bentry)
        elif(globals.bstate == "action" or globals.bstate == "method" or globals.bstate == "naction" or globals.bstate == "nmethod"):
            items = ll.strip().split(" ")
            if (globals.bstate == "naction"):
                globals.actions[items[-1]] = 1
            addSuggestions("enter method", Bentry)
            addSuggestions("methods_only", Bentry)
            if (globals.bstate == "nmethod"):
                item = items[-1].strip(",")
                globals.methods[item] = 1
            if (globals.bstate == "nmethod" or globals.bstate == "method"):
                addSuggestions("emit", Bentry)
        elif (globals.bstate == "emit"):
            addSuggestions("enter event name", Bentry)
        elif (globals.bstate == "emitted"):
            addSuggestions("enter event name", Bentry)

#            elif chs[-1] in globals.actors:
#                print "Found actor ",chs[-1]
#                addSuggestions("enter action", Bentry)
#                addSuggestions("actions_only", Bentry)
#            elif chs[-1] in events:
#                addSuggestions("globals.actors_only", Bentry)
#            elif chs[-1] == "emit":
#                addSuggestions("enter event name", Bentry)
#            elif len(chs) >= 2:
#                if (chs[-2] == "emit" and chs[-1] in events):
#                    addSuggestions("behaviors_enter", Bentry)
#                elif (chs[-2] in globals.actors and text.endswith(" ")):
#                    actions[chs[-1]] = 1
#                    addSuggestions("enter method", Bentry)
#                elif len(chs) >= 3 and (chs[-3] in globals.actors):
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
        globals.app.stopLabelFrame()

def regenerateSuggestions(evtype):
    print "Event ",evtype
    for t in globals.sbuttons:
        print "Button ",t
    if evtype == "behaviors_enter":
        processBehavior()
    elif evtype == "globals.actors_enter":
        print "Entered actors"
        globals.app.openLabelFrame("Suggestions")
        for t in globals.sbuttons:
            globals.app.removeButton(t)
        globals.sbuttons.clear()
        for t in globals.slabels:
            globals.app.removeLabel(t)
        globals.slabels.clear()
        globals.app.stopLabelFrame()
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
        globals.actors=dict()
        text = globals.app.getTextArea("actor")
        roles = text.split("\n")
        for r in roles:
            if r not in globals.actors and r.strip() != "":
                globals.actors[r] = 1
                print "Added actor ", r
    if (widget == "behavior"):
        text = globals.app.getTextArea("behavior")
        bhs = text.split("\n")
        i=0
        globals.events.clear()
        for b in bhs:
            globals.behaviors[i] = b
            i = i + 1
            items = b.split(" ")
            # parse out events
            prev = ""
            for item in items:
                if (item == "emit"):
                    prev = item
                    continue
                if (prev == "emit"):
                    globals.events[item] = 1
                prev = item

def entered(widget):
    print widget
    if (widget == "actor"):
        regenerateSuggestions("globals.actors_enter")        
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

