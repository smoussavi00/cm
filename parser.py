import lexer
import sys

class Node:
    def __init__(self, type):
        self.type = type
        self.c = []
    def __repr__(self):
        return repr(lexer.translator(self.type))

def pm(ts,pr):
# Pattern matching function - Standard

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
            return 'f'
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
                    return 'f'
        else: 
            nts.append(Node(cpr))
        #IF WE ARE LOOKING FOR A NT TOKEN - SKIP TO THE NEXT T TOKEN
            start = i
            cpr = pr.pop(0)
            if cpr in [2,4,6]:
                mode = 1
            else:
            #NOW WE NEED TO FIND 'LAST-INSTANCE' NT TOKEN 
                mode = 2
        i += 1
    if mode == 2:
        if li == -1:
            print("Syntax Failure")
            return 'f'
        else:
            nts[-1].c = ts[start:li]
            nts.append(ct)
    if len(pr) != 0:
        #RAISE EXCEPTION - FAILED TO FIND EACH TOKEN ASKED BY PRODUCTION RULE
        print("Syntax Failure")
        return 'f'

        
    return nts

'''
Production Rules:
    <main function>
'''
def pprog(ts): 
# Parses the program token 

    prog_node = Node(-1)
    prog_node.c.append(Node(100))
    pfunc(ts,prog_node.c[0])
    
'''
Production Rules:
    "int" -name- <parameters> "{" <body> "}"
'''
def pfunc(ts,n):
# Parses the function token

    pr = [12,11,102,2,101,3]
    cc = pm(ts,pr)
    if cc != 'f':
        n.c = cc
    pparamdef(cc[2].c,cc[2])
    pblock(cc[4].c,cc[4])

def pparamdef(ts,n):
#Parses the parameter token
    nts = []
    if not(ts[0] == '(' and ts[-1] == ')'):
        print("Syntax Failure")

    else:
        nts.append('(')
        start = 1
        for i in range(1,len(ts),1):
            if ts[i] == ',' and i != len(ts)-1:
            #EVERYTHING UP TO THIS COMMA IS <SINGLE DEF PARAMETER> CANDIDATE
                nts.append(Node(103))
                nts[-1].c = ts[start:i]
                nts.append(',')
                start = i+1
            elif i == len(ts)-1:
                nts.append(Node(103))
                nts[-1].c = ts[start:i]
                nts.append(')')

def pblock(ts,n):
#Parses the block token
    nts = []
    start = 0
    wait = -1
    for i in range(len(ts)):

        if ts[i] == ';' and wait == -1:
            nts.append(Node(104))
            nts[-1].c = ts[start:i]
            nts.append(';')
            start = i+1

        if ts[i] == '{':    
            wait += 1
            if wait == 0:
                    nts.append(Node(105))
                    nts[-1].c = ts[start:i]
                    start = i+1

        if ts[i] == '}' and wait != -1:
            wait -= 1
            if wait  == -1:
                nts.append('{')
                nts.append(Node(101))
                nts[-1].c = ts[start:i]
                nts.append('}')
                wait = -1
                start = i + 1

    print(nts)

        
def main():
    if len(sys.argv) != 2:
        print("Unspecified File Failure")
        return
    
    f = open(sys.argv[1], 'r')
    ts = lexer.get_tokens(f)
    pprog(ts)

if __name__ == "__main__":
    main()