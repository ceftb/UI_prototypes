from pyparsing import ParseException, NotAny, Group, Word, Keyword, Literal, alphas, alphanums, nums, White, ZeroOrMore, OneOrMore, Optional

when_keyword = (Keyword("when") | Keyword("When") | Keyword("WHEN")).suppress()
wait_keyword = (Keyword("wait") | Keyword("Wait") | Keyword("WAIT")).suppress()
emit_keyword = (Keyword("emit") | Keyword("Emit") | Keyword("EMIT")).suppress()
not_akeyword = (NotAny(emit_keyword) + NotAny(wait_keyword) + NotAny(when_keyword))
comma = Literal(",").suppress()
newline = Literal("\n")
wsp = White().suppress()
actor = (not_akeyword + Word(alphanums))
actors = actor + ZeroOrMore((comma + wsp + actor | comma + actor))
action = (not_akeyword + Word(alphanums) + Optional(wsp + "start" |wsp + "stop" | wsp + "check"))
event =(not_akeyword + Word(alphanums))
events = event + ZeroOrMore((comma + wsp + event | comma + event))
trigger = (when_keyword + events("t_events") | when_keyword + events("t_events") + wait_keyword + nums | wait_keyword + nums)
hlb_statement = (trigger("trigger") + wsp +  actors("actors") + wsp + action("action") + emit_keyword + events("emit_events") | trigger("trigger") + wsp + actors("actors") + wsp + action("action"))
#hlb = hlb_statement + newline + hlb

while True:
    print("Enter statement.")
    line = input()
    try:
        parsed = hlb_statement.parseString(line)
        print(parsed)
        print("Trigger(s): %s" % parsed.t_events)
        print("Actors: %s" %  ','.join(parsed.actors))        
        print("Action: %s" %  parsed.action)        
        print("Emit events: %s" % parsed.emit_events)
    except ParseException as pe:
        print(pe)
        continue
    

    
    