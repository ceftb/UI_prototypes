app = None
bdg_canvas = None
topo_canvas = None
bdg_handler = None
topo_handler = None

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

