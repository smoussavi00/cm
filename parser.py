import lexer
import sys

class Node:
    def __init__(self, type):
        self.type = type
        self.c = []
    def __repr__(self):
        return repr(lexer.translator(self.type))


def pm(ts,pr):
# Pattern matching function 

# pr - production rules of the form: [T1,T2,...,TN]
# ts - token set of the form [TT1,TT2,...,TTM] where TT is a terminal token
# Returns all tokens, and combines the terminal into non-terminal tokens 
# Returns exception if the pattern matching fails

    nts = []
    mode = -1
    start = -1
    i = 0
    li = -1

    for ct in ts:
        if len(pr) == 0 and mode == -1:
        #RAISE EXCEPTION - THERE ARE TOKENS IN THE SET THAT ARE NOT ACCOUNTED FOR
            print("Syntax Failure")
            break
        if mode == -1:
            cpr = pr.pop(0)
        if cpr < 100: 
        #IF WE ARE LOOKING FOR A T TOKEN - ATTEMPT TO MATCH THEM
            if mode == 1:
                if cpr == lexer.categorizer(ct):
                    nts[-1].c = ts[start:i]
                    nts.append(ct)
                    mode = -1
            elif mode == 2:
                if cpr == lexer.categorizer(ct):
                    li = i
            else:

                if lexer.categorizer(ct) == cpr:
                    nts.append(ct)
                else:
                #RAISE EXCEPTION - FAILED TO MATCH CURRENT TOKEN 
                    print("Syntax Failure")
                    break
        else: 
            nts.append(Node(cpr))
        #IF WE ARE LOOKING FOR A NT TOKEN - SKIP TO THE NEXT T TOKEN
            start = i
            cpr = pr.pop(0)
            if cpr in [2,4,6]:
                mode = 1
            else:
            # NOW WE NEED TO FIND 'LAST-INSTANCE' NT TOKEN 
                mode = 2
        i += 1
    if mode == 2:
        if li == -1:
            print("Syntax Failure")
            return
        else:
            nts[-1].c = ts[start:li]
            nts.append(ct)
    if len(pr) != 0:
        #RAISE EXCEPTION - FAILED TO FIND EACH TOKEN ASKED BY PRODUCTION RULE
        print("Syntax Failure")
        

    return nts

'''
Production Rules:
    <main function>
'''
def pprog(ts): 
# Parses the program token 

    prog_node = Node("prog")

    prog_node.c.append(pfunc(ts))
    return prog_node

'''
Production Rules:
    "int" -name- <parameters> "{" <statement> "}"
'''
def pfunc(ts):
# Parses the function token
    pr = [12,11,102,2,101,3]
    print(pm(ts,pr))


    pass

def main():
    if len(sys.argv) != 2:
        print("Unspecified File Failure")
        return
    
    f = open(sys.argv[1], 'r')
    #pprog(lexer.get_tokens(f))
    ts = lexer.get_tokens(f)
    pr = [12,11,102,2,101,3]
    print(ts)
    pfunc(ts)

if __name__ == "__main__":
    main()