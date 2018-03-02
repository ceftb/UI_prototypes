import re
import sys
sys.path.append('../')
import globals
try:
    from tkinter import filedialog
except ImportError:
    import tkFileDialog

try:
    import xir
    from xir import eq, choice, gt, ge, select
    NOXIR=False
except ImportError:
    NOXIR=True

# handle button events
def press(button):
    print(button)


def save_routes():
    routes = dict()

    for a in globals.links:
        for b in globals.links[a]:
            if a not in routes:
                routes[a] = dict()
            routes[a][b] = dict()
            routes[a][b]['n'] = b
            routes[a][b]['h'] = 1
            if b not in routes:
                routes[b] = dict()
            routes[b][a] = dict()
            routes[b][a]['n'] = a
            routes[b][a]['h'] = 1

    for l in globals.lans:
        for a in globals.lans[l]:
            for b in globals.lans[l]:
                if a == b:
                    continue
                if a not in routes:
                    routes[a] = dict()
                routes[a][b] = dict()
                routes[a][b]['n'] = b
                routes[a][b]['h'] = 1

    while True:
        updates = 0
        for a in routes:
            for b in routes[a]:
                for c in routes[a]:
                    if c == b:
                        continue
                    if routes[a][b]['h'] > 1:
                        continue
                    if c not in routes[b] or (c in routes[b] and routes[b][c]['h'] > routes[a][c]['h']+1):
                        if c not in routes[b]:
                            routes[b][c] = dict()
                        routes[b][c]['n'] = a
                        routes[b][c]['h'] = routes[a][c]['h']+1
                        updates += 1
        if updates == 0:
            break

        globals.addresses.clear()

        for a in globals.links:
            for b in globals.links[a]:
                if a not in globals.addresses:
                    globals.addresses[a] = dict()
                globals.addresses[a][globals.links[a][b]] = 1

        for l in globals.lans:
            for i in globals.lans[l]:
                if i not in globals.addresses:
                    globals.addresses[i] = dict()
                globals.addresses[i][globals.lans[l][i]] = 1


        f = open("setup.txt", "w")
        for a in routes:
            for b in routes[a]:
                if routes[a][b]['h'] > 1:
                    c = routes[a][b]['n']
                    for i in addresses[a]:
                        for j in addresses[b]:
                            f.write("route "+globals.addresses[a][i]+" "+globals.addresses[b][j] + " "+routes[a][b]['n'])
        


def save_docker(f):
    # decide on lan IPs
    nets = dict()
    nc = 0
    savelinks = globals.links
    for a in savelinks:
        for b in savelinks[a]:
            globals.links[a][b] = "172.1." + str(nc)
            nets[globals.links[a][b]] = 1            
            if b not in globals.links:
                globals.links[b] = dict()
            globals.links[b][a] = "172.1." + str(nc)
            nets[globals.links[b][a]] = 2
            nc += 1

    for l in globals.lans:
        lc = 1
        for i in globals.lans[l]:
            globals.lans[l][i] = "172.1." + str(nc) + "." + str(lc)
            lc += 1
        nets[l] = "172.1." + str(nc)
        nc += 1

    f.write("version: '3'\nservices:\n");
    for a in globals.nodes:
        f.write("\n "+a+":\n  build:\n   dockerfile: custom.dock\n   context: .\n  command: /bin/setroutes.pl\n  privileged: true\n  networks:\n")
        if a in globals.links:
            for b in globals.links[a]:
                f.write("   link-" + a + "-" + b + ":\n    ipv4_address: " + globals.links[a][b] + "." + str(nets[globals.links[a][b]]) + "\n")
                nets[globals.links[a][b]] += 1

        for l in globals.lans:
            if a in globals.lans[l]:
                f.write("   " + l + ":\n    ipv4_address: " + globals.lans[l][a] + "\n")

        
    f.write("\n\nnetworks:\n")
    for a in globals.links:
        for b in globals.links[a]:
            f.write(" link-" + a + "-" + b + ":\n  driver: bridge\n  ipam:\n   driver: default\n   config:\n   -\n     subnet: "+globals.links[a][b]+".0/24\n\n")

            
    for l in globals.lans:
        f.write(" " + l +  ":\n  driver: bridge\n  ipam:\n   driver: default\n   config:\n   -\n     subnet: "+nets[l]+".0/24\n\n")
        break

    f.close()
    save_routes()

def save(f):
    if NOXIR:
        return

    top = xir.Xir()
    nodes = dict()
    for n in globals.nodes:                                                                                                                        
        node = top.structure.node({'name': n})
        nodes[n] = node

    for a in globals.links:
        for b in globals.links[a]:
            top.structure.connect([nodes[a], nodes[b]], {})

    for l in globals.lans:
        lan = top.structure.node({'name': l, 'capability': select('switch')})
        for i in globals.lans[l]:
            top.structure.connect([nodes[i], lan], {
                    "stack": eq("ip")})
 
    f.write(top.xir())



#            f.write("\tendpoints: [[" + a + "],[" + b +"\n")
#            f.write("\tprops: {}\n");

#    for l in globals.lans:
#        f.write("net:\n")
#        f.write("\tid: " + str(n) + '\n')
#        f.write("\tnodes: [")
#        first = 0
#        for i in globals.lans[l]:
#                if first == 1:
#                    f.write(",")
#                first = 1
#                f.write(str(i));
#        f.write("]\n");
#
#    f.write("}\n\n")
#    f.write("behavior: {\n")
#   text = globals.app.getTextArea("behavior")        
#    f.write(text)
#    f.write("\n}\n\n")





def gather_bindings():
    print("Globals dialogue %s" %globals.dialogue)
    if (globals.dialogue == None):
        globals.app.startSubWindow("Dialogue",modal=True)
        globals.app.setGeometry("400x400")
        globals.app.setSticky("news")
        globals.app.setStretch("both")
        globals.app.startScrollPane("Dialogue")
        globals.dialogue = True
    else:
        globals.app.openSubWindow("Dialogue")
        globals.app.openScrollPane("Dialogue")
        globals.app.removeButton("Submit")
        globals.app.removeLabel("bt1")
        globals.app.removeLabel("bt2")
        globals.app.removeLabel("bt3")

    globals.app.addLabel("bt1", "Please enter paths to executables for all the following actions.",0,0,2)

    for a in globals.dlabels:
        globals.app.removeLabel(a)
    for a in globals.dentries:
        globals.app.removeEntry(a)
    globals.dlabels.clear()
    globals.dentries.clear()

    i = 1
    ce = 0
    for a in globals.actions:
        globals.app.addLabel(a, a, i, 0)
        globals.dlabels[a] = 1
        globals.app.addEntry(a,i,1)
        globals.app.setEntryChangeFunction(a, entryFunc)
        globals.dentries["e"+str(ce)] = 1
        ce += 1
        i += 1

    print("Events %d"% len(globals.events))

    if len(globals.events)>0:
        globals.app.addLabel("bt2", "Please enter paths to executables for all the following events.",i,0,2)
        globals.app.addLabel("bt3", "Event executables should return 1 if the event occured, and 0 otherwise.",i+1,0,2)
        i += 2

    for a in globals.events:
        globals.app.addLabel(a, a, i, 0)
        globals.dlabels[a] = 1
        globals.app.addEntry("e"+str(ce),i,1)
        globals.dentries["e"+str(ce)] = 1
        ce += 1
        i += 1
    globals.app.addButton("Submit", tbFunc, i, 0, 2)
    globals.app.stopScrollPane()
    globals.app.stopSubWindow()
    globals.app.showSubWindow("Dialogue")

def entryFunc(entry):
    print "Changed ",entry

def tbFunc(button):
    print(button)
    if (button == "SAVE"):
        # create another window for setting bindings for actions 
        gather_bindings();

        #save(file_path)
    elif (button == "Submit"):
        # take and save all the input
        globals.app.hideSubWindow("Dialogue")
        file_path = tkFileDialog.asksaveasfile(mode='w', defaultextension=".xir")
        save(file_path)
        f = open("docker-compose.yml", "w")
        save_docker(f)
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
                print("add actor %s" % a)
                globals.sbuttons[a] = 1
                globals.app.addButton(a, pb)
    elif evtype == "actions_only":
        for a in globals.actions:
            if a != "":
                print("add action %s" % a)
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
        print("Actors %d" % len(globals.actors))
        for a in globals.actors:
            if a != "":
                print("add actor %s" % a)
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
    elif evtype == "constraints_enter":
        for l in ["num", "os","link","lan","interfaces","location","nodetype"]:
            globals.app.addButton(l,Centry)
            globals.sbuttons[l]=1
    elif evtype == "emit":
        globals.sbuttons["emit"] = 1
        globals.app.addButton("emit", pb)
    else: # it was text to be displayed as label
        globals.app.addLabel(evtype,evtype)
        globals.slabels[evtype] = 1
    globals.app.stopLabelFrame()

def prefix(mystring):
    p = 0
    for i in str(mystring):
        if i.isdigit():
            return mystring[0:p-1]
        p += 1
    return None

def processConstraints():
        print("Entered constraints")
        globals.app.openLabelFrame("Suggestions")
        for t in globals.sbuttons:
            globals.app.removeButton(t)
        globals.sbuttons.clear()
        for t in globals.slabels:
            globals.app.removeLabel(t)
        globals.slabels.clear()
        text = globals.app.getTextArea("constraints")
        chs = text.split("\n")
        i=0
        lnc=1
        # parse out constraints and remember them
        # from every line including the last
        globals.constraints.clear()
        globals.links.clear()
        globals.lans.clear()
        globals.lans["lan0"] = dict()
        globals.nodes.clear()
        for a in globals.actors:
            globals.nodes[a] = 0
        for c in chs:
            items = re.split("[\s,]",c.strip())
            item = items.pop(0)
            # parse out constraints
            if len(items) >= 2:
                if (item == "num" or item == "os" or item == "location" or item == "interfaces" or item == "nodetype"):
                    if items[0] in globals.nodes:
                        if items[0] not in globals.constraints:
                            globals.constraints[items[0]] = dict()
                        globals.constraints[items[0]][item] = items[1]        
                if (item == "num"):
                    globals.nodes.pop(items[0], None)
                    for i in range(0,int(items[1])):
                        globals.nodes[items[0]+str(i)] = 0
                if (item == "link"):
                    if len(items) >= 2:
                        a = items.pop(0)
                        b = items.pop(0)
                        if a in globals.nodes and b in globals.nodes:
                            if a not in globals.links:
                                globals.links[a] = dict()
                            globals.links[a][b] = ""
                            for i in items:
                                globals.links[a][b] += (i + " ")
                            globals.nodes[a] = 1
                            globals.nodes[b] = 1
                if (item == "lan"):
                    label = "lan" + str(lnc)
                    if label not in globals.lans:
                        globals.lans[label] = dict()
                    for i in items:
                        if i in globals.nodes:
                            globals.lans[label][i] = 1
                            globals.nodes[i] = 1
                    lnc = lnc + 1

        # Now find all nodes that are not part of any link or lan and put them
        # into one lan
        for n in globals.nodes:
            if globals.nodes[n] == 0:
                globals.lans["lan0"][n] = 1
                globals.nodes[n] = 2

        # Then join this lan with a node that is the most similar to nodes in the lan
        if (len(globals.lans["lan0"]) > 0):
            prefs = dict()
            maxc = 0
            maxp = ""
            for n in globals.nodes:
                if globals.nodes[n] == 2:
                    t = prefix(n)
                    if t not in prefs:
                        prefs[t] = 1
                    else:
                        prefs[t] += 1
                    
                    if prefs[t] > maxc:
                        maxc = prefs[t]
                        maxp = t
                            
            for n in globals.nodes:
                if globals.nodes[n] == 1 and prefix(n) == maxp:
                    globals.lans["lan0"][n] = 1
                    break
        else:
            globals.lans.pop("lan0", None)

        # Go through last constraint line to see what we can suggest
        ll = chs.pop()
        items = re.split("[\s,]",ll.strip())
        item = items.pop(0)
        print("Len %d item %s"%(len(items),item))
        if item in ["num", "os","nodetype", "interfaces", "location", "link","lan"] and len(items) == 0:
            addSuggestions("actors_only", Centry)
        elif len(items) >= 1:
            if (item == "num" or item == "interfaces") and items[-1] in globals.actors:
                addSuggestions("enter digit", Centry)
            elif item == "os" and (items[-1] in globals.actors 
                                   or items[-1] in globals.nodes):
                addSuggestions("enter OS", Centry)
            elif item == "nodetype" and (items[-1] in globals.actors 
                                        or items[-1] in globals.nodes):
                addSuggestions("enter node type", Centry)
            elif item == "link" and (items[-1] in globals.actors or 
                                     items[-1] in globals.nodes):
                addSuggestions("actors_only", Centry)
            elif item == "lan" and (items[-1] in globals.actors or
                                    items[-1] in globals.nodes):
                addSuggestions("actors_only", Centry)
            elif item == "location" and (items[-1] in globals.actors or
                                         items[-1] in globals.nodes):
                addSuggestions("enter testbed", Centry)
            else:
               addSuggestions("constraints_enter", Centry)
        else:
            addSuggestions("constraints_enter", Centry)
        globals.app.stopLabelFrame()

        for n in globals.nodes:
            print("Node %s" % n)
        for a in globals.links:
            for b in globals.links[a]:
                print("Link %s-%s"% (a,b))
        for a in globals.lans:
            lanstring = ""
            for b in globals.lans[a]:
                lanstring += (b+ " ")
            print("Lan %s:%s" %( a,lanstring))
            

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
    #print "fwh ",fwh, " fwa ",fwa," fa ",fa, " fe ",fe," fp ",fp, " diff ",diff
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
    globals.nodes[item] = 1
    if "lan0" not in globals.lans:
        globals.lans["lan0"] = dict()
    globals.lans["lan0"][item] = 1

    if ("actor"+str(globals.acn)) in globals.actors:
        globals.acn = globals.acn+1

    delim=""
    text = globals.app.getTextArea("actor")        
    if (not text.endswith("\n") and text != ""):
        delim="\n"
    globals.app.setTextArea("actor", delim+item, True, True)
    
    

def processBehavior():
        #print("Entered behavior")
        globals.app.openLabelFrame("Suggestions")
        for t in globals.sbuttons:
            globals.app.removeButton(t)
        globals.sbuttons.clear()
        for t in globals.slabels:
            globals.app.removeLabel(t)
        globals.slabels.clear()
        text = globals.app.getTextArea("behavior")

        # first capitalize keywords, perhaps remove this
        text = text.replace("when","WHEN")
        text = text.replace("wait","WAIT")
        text = text.replace("emit","EMIT")

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
        print("State %s" % (globals.bstate))

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
            addSuggestions("actors_only", Bentry)
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

        
        
        print text
        globals.app.stopLabelFrame()

def regenerateSuggestions(evtype):
    print("Event %s" % evtype)
    for t in globals.sbuttons:
        print("Button %s" %t)
    if evtype == "behaviors_enter":
        processBehavior()
    elif evtype == "globals.actors_enter":
        print("Entered actors")
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
    print(widget)

    if (widget == "actor"):
        globals.actors=dict()
        text = globals.app.getTextArea("actor")
        roles = text.split("\n")
        for r in roles:
            if r not in globals.actors and r.strip() != "":
                globals.actors[r] = 1
                print("Added actor %s" % r)
                # Update topology 
                print("Updating topology.")
                globals.topo_handler.add_entity(r)

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
            globals.bdg_handler.add_new_behavior(b)

def entered(widget):
    print(widget)
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

