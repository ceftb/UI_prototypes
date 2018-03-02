app = None
dialogue = None
bdg_canvas = None
topo_canvas = None
bdg_handler = None
topo_handler = None
nlp_handler = None
nlp_help_str = "Type Natural English Language Here. E.g.:\n\"After the bad host begins the attack, the good host will deploy defences.\""

acn=0
tcn=0
al=0

actors=dict()
behaviors=dict()
constraints=dict()
events=dict()
actions=dict()
methods=dict()

nodes=dict()
links=dict()
lans=dict()
addresses=dict()

sbuttons=dict()
slabels=dict()
dlabels=dict()
dentries=dict()

bstate = "start" # state of current behavior start, (waitd, wait) or (whene, when) or actor, actor, action, method, emit, done

