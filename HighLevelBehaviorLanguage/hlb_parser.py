from pyparsing import ParseException, NotAny, Empty, Group, Word, CaselessKeyword, Literal, alphas, alphanums, nums, White, ZeroOrMore, OneOrMore, Optional

class HLBParser():
    when_keyword = CaselessKeyword("when").suppress()
    wait_keyword = CaselessKeyword("wait").suppress() 
    emit_keyword = CaselessKeyword("emit").suppress()
    not_akeyword = (NotAny(emit_keyword) + NotAny(wait_keyword) + NotAny(when_keyword))
    comma = Literal(",").suppress()
    newline = Literal("\n")
    wsp = White().suppress()
    actor = (not_akeyword + Word(alphanums))
    actors = actor + ZeroOrMore((comma + wsp + actor | comma + actor))
    action = (Optional(CaselessKeyword("start") | CaselessKeyword("stop") | CaselessKeyword("restart") | CaselessKeyword("check")) + Word(alphanums))	
    event = (not_akeyword + Word(alphanums))
    events = event + ZeroOrMore((comma + wsp + event | comma + event))
    when_trigger = when_keyword + events("t_events")
    wait_time = (not_akeyword + Word(alphanums))
    wait_trigger = (wait_keyword + wait_time("wait_time"))
    trigger = (when_trigger + wsp + wait_trigger | when_trigger | wait_trigger)
    
    # Full complete statment.
    hlb_statement = (trigger("trigger") + wsp + actors("actors") + wsp + action("action") + emit_keyword + events("emit_events") 
                    | actors("actors") + wsp + action("action") + emit_keyword + events("emit_events")
                    |trigger("trigger") + wsp + actors("actors") + wsp + action("action") 
                    | actors("actors") + wsp + action("action"))
    
    # Partial statements (not incorrect, but not complete either.)
    hlb_missing_when_list = (when_keyword)
    hlb_missing_wait_time = (when_trigger + wsp + wait_keyword | wait_keyword)
    hlb_missing_actors = (trigger("trigger") + not_akeyword)
    hlb_missing_action = (trigger("trigger") + wsp + actors("actors") |  actors("actors"))
    hlb_missing_emit_list = (actors("actors") + wsp + action("action") + emit_keyword | trigger("trigger") + wsp + actors("actors") + wsp + action("action") + emit_keyword)
    
    #hlb = hlb_statement + newline + hlb
        
    def parse_stmt(self, statement):
        """Parses an HLB statement and returns a tuple: (triggers, actors, action, emit_events)
        Values are returned as "None" if they cannot be extracted.
        """
        try:
            parsed = self.hlb_statement.parseString(statement)
        except ParseException as pe:
            #print("WARNING: Could not parse HLB statement:\n\t%s" % (statement))
            return(None, None, None, None, None)
        return_tuple = (parsed.t_events, parsed.actors, parsed.action, parsed.emit_events, parsed.wait_time)
        return(tuple(r if r != [] and r != "" else None for r in return_tuple))

    def extract_partial(self, partial):
        t_events, actors, action, emit_events, wait_time = self.parse_stmt(partial)
        if emit_events == "":
            print("Complete statement. Suggetion: Can add emit events.")
        if actors == None:
            print("Statement is not complete as is.")
            
            ## WARNING: The following is a longest match first:
            ## For the below to work, the order must be kept 
            ## (along with the break out of conditional statements 
            ## via return or some other mechanism).
            
            # Do we have an emit, but missing emit event list?
            try:
                parsed = self.hlb_missing_emit_list.parseString(partial)
                print("Missing emit list.")
                return
            except ParseException as pe:
                pass
            # Are we missing an action?
            try:
                parsed = self.hlb_missing_action.parseString(partial)
                print("Missing action.")
                return
            except ParseException as pe:
                pass
            # Do we have a trigger, but no actors?
            try:
                parsed = self.hlb_missing_actors.parseString(partial)
                print("Missing actors")
                return
            except ParseException as pe:
                pass
            # Do we have a wait? but missing the wait time?
            try:
                parsed = self.hlb_missing_wait_time.parseString(partial)
                print("Missing wait time")
                return
            except ParseException as pe:
                pass
            # Do we have a when? but missing the when event triggers?
            try:
                parsed = self.hlb_missing_when_list.parseString(partial)
                print("Missing when list.")
                return
            except ParseException as pe:
                pass
            print("Unsure what's wrong.")
            return
                
def testParser():
    parser = HLBParser()
    while True:
        line = raw_input("Input statement: ")
        print(line)
        (t_events, actors, action, e_events, wait_time) = parser.parse_stmt(line)
        if actors != None:
            print("Actors: %s" %  actors)        
        if t_events != None:
            print("Trigger(s): %s" % t_events)
        if action != None:
            print("Action: %s" %  action)        
        if e_events != None:
            print("Emit events: %s" % e_events)
        if wait_time != None:
            print("Wait time: %s" % wait_time)
        parser.extract_partial(line)
    
if __name__ == "__main__":
    testParser()
    
    