import re

class inputHelper():
    def __init__(self):
        self.ok_check = {'':self.ok, 'N':self.rename, 'n':self.rename, 'f':self.forget, 'F':self.forget}    
        
    def ok(self,str):
        print("ok")
        return(str)
    
    def rename(self,str):
        print("rename")
        return(input("Input new name: "))
    
    def forget(self,str):
        print("forget")
        return None
        
    def get_list(self, qtext):
        initial_list = input("%s (Use commas to separate) " % qtext)
        parsed_list = initial_list.split(',')
        oked_list = []
        for item in parsed_list:
            new_item = None
            func = input("\'%s\': Does this entity look ok? (Enter for ok, N to rename, F to forget this entity.) "%item)        
            try:	
                new_item = self.ok_check[func](item)
            except KeyError:
                print("Sorry, type-os here not handled yet. Moving on.")
                new_item = item
                pass
            oked_list.append(new_item)
        return(oked_list)
    
    def q_with_options(self, qtext, options):
        counted_list = zip([str(i) for i in range(1, len(options)+1)], options)
        option_list = []
        for item in counted_list:
            option_list.append('. '.join(item))
        option_text=' , '.join(option_list)
        option = input("%s: \n\tOptions are:\n\t%s\n\tor press 'o' for other to enter your own. To pick multiple, put a comma separated list in.\n" %(qtext, option_text))
        choices = []
        if option == 'o' or option == 'O':
            return([input("Enter your value: ")])
        try:
            for o in option.split(','):
                int_option = int(o)
                if int_option in range(1, len(options)+1):
                    option = options[int_option-1]
                    choices.append(option)
        except ValueError:
            pass
        return(choices)

def hlb_friendly_name(str):
    return(re.sub(r"\s+", '_', str.strip()))

def questions():
    tcount = 1
    unknown_triggers = []
    # XXX total hack - we should have a proper grammar and 
    # collapse statements into more compact lines (e.g. grouping all actors which start the same process into one line)
    hlb = []
    qh = inputHelper()
    
    # Get list of entities
    entities = qh.get_list("Please list the actors in your scenario.")
    processes = qh.get_list("Please list the activities (processes) that will run in your scenario.")
    triggers = [ '@start4' + s for s in processes ] + [ '@stop4' + s for s in processes ] + ['At the scenario <<start>>', 'After a <<wait time>>.'] 
    for p in processes:
        runs_on = qh.q_with_options('Which actors run %s?' %(p), entities)
        print(runs_on)
        for actor in runs_on:
            triggered_by = qh.q_with_options('What triggers %s to start on %s?'%(p, actor), [t for t in triggers if p not in t])
            for t in triggered_by:
                if t not in triggers:
                    unknown_triggers.append(t)
            # If we start this at the beginning or at a specific time, we ignore all other triggers.
            if 'At the scenario <<start>>' in triggered_by:
                hlb.append('%s start %s emit %s' % (hlb_friendly_name(actor), hlb_friendly_name(p), hlb_friendly_name(p)+'_'+hlb_friendly_name(actor)+'_start'))
            elif 'After a <<wait time>>.' in triggered_by:
                hlb.append('wait %s %s start %s emit %s' % ('t'+str(tcount), hlb_friendly_name(actor), hlb_friendly_name(p), hlb_friendly_name(p)+'_'+hlb_friendly_name(actor)+'_start'))
                tcount = tcount+1
            else:
                hlb.append('when %s %s start %s emit %s' % (','.join([hlb_friendly_name(s) for s in triggered_by]), hlb_friendly_name(actor), hlb_friendly_name(p), hlb_friendly_name(p)+'_'+hlb_friendly_name(actor)+'_start'))
            
    for line in hlb:
        print(line)  
        

if __name__ == '__main__':
    questions()                
    

