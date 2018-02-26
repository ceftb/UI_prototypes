from pyparsing import ParseException, NotAny, Group, Word, CaselessKeyword, Literal, alphas, alphanums, nums, White, ZeroOrMore, OneOrMore, Optional

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
    event =(not_akeyword + Word(alphanums))
    events = event + ZeroOrMore((comma + wsp + event | comma + event))
    when_trigger = when_keyword + events("t_events")
    wait_time = Word(alphanums)
    wait_trigger = wait_keyword + wait_time("wait_time")
    trigger = (when_trigger + wsp + wait_trigger | when_trigger | wait_trigger)
    hlb_statement = (trigger("trigger") + wsp +  actors("actors") + wsp + action("action") + emit_keyword + events("emit_events") | trigger("trigger") + wsp + actors("actors") + wsp + action("action"))
    #hlb = hlb_statement + newline + hlb
    
    
    def parse_stmt(self, statement):
        """Parses an HLB statement and returns a tuple: (triggers, actors, action, emit_events)
        """
        try:
            parsed = self.hlb_statement.parseString(statement)
        except ParseException as pe:
            print("WARNING: Could not parse HLB statement:\n\t%s" % (statement))
            return(None, None, None, None, None)

        return(parsed.t_events, parsed.actors, parsed.action, parsed.emit_events, parsed.wait_time)

def testParser():
    parser = HLBParser()
    while True:
        line = raw_input("Input statement: ")
        print(line)
        (t_events, actors, action, e_events, wait_time) = parser.parse_stmt(line)
        if actors != None:
            print("Trigger(s): %s" % t_events)
            print("Actors: %s" %  actors)        
            print("Action: %s" %  action)        
            print("Emit events: %s" % e_events)
            print("Wait time: %s" % wait_time)
    
if __name__ == "__main__":
    testParser()
    
    