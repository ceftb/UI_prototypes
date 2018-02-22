import spacy
import sys
sys.path.append('../')
import globals
from HighLevelBehaviorLanguage.hlb import *
from NLP.nlplib import findEntities, findCondClauses, actionRelation

class nlpHandler():
    sentences = []
    dict = spacy.load('en')

    def nlpChanged(self, widget):
        current_text = globals.app.getTextArea("NLP Input")
        if len(current_text.split('.')) != len(self.sentences) and len(current_text.split('.')) > 1:
            if len(current_text.split('.')) > len(self.sentences):
                # We have a new sentence.
                for sentence in current_text.split('.'):
                    if sentence.strip() not in  self.sentences and sentence.strip() != "":
                        print("New to process: %s" % sentence)
                        
                        tokens = self.dict(sentence)
                        
                        cond_clauses = findCondClauses(tokens)
                        main_sen = sentence
                        i = 1
                        for cond in cond_clauses:
                            main_sen = main_sen.replace(str(cond), '', 1)
                            i = i+1
                        main_action_relation = actionRelation(main_sen)
                        clause_action_relation = []
                        if len(cond_clauses) > 0:
                            clause_action_relation = actionRelation(cond_clauses[0])
                        if len(cond_clauses) > 1:
                            print("Warning: Mutiple conditional statements in a sentence is not handled.")
                        print("Main action relation:")
                        print(main_action_relation)
                        if len(cond_clauses) > 0:
                            print("Conditional action relation")
                            print(clause_action_relation)
                                        
                        # Entities.
                        entities = findEntities(tokens)
                        for ent in entities:
                            globals.app.setTextArea("actor",''.join(x for x in str(ent).title() if not x.isspace()) +'\n', callFunction=actorentered)
                        
            elif len(current_text.split('.')) < len(self.sentences):
                print("Do not handle erasures yet.")
                # We have lost a sentence.
            self.sentences = [s.strip() for s in current_text.split('.')]