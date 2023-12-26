import lexer
import sys

class Node:
    def __init__(self, type):
        self.type = type
        self.c = []
    def __repr__(self):
        return repr(lexer.translator(self.type))

'''
Production Rules:
    <main function>
'''
def pprog(ts): 
# Parses the program token 

    prog_node = Node(-1)
    prog_node.c.append(Node(100))
    pfunc(ts,prog_node.c[0],1)
    
'''
Production Rules:
    <data type> -name- <function def parameters> "{" <block> "}"
    int main <main parameters> "{" <block> "}"
'''
def pfunc(ts,n,is_main=0):
# Parses the function token
    
    nts = []
    start = 0 
    mode = 1
    wait = -1
    pwait = -1
    s = 0

    for i in range(len(ts)):

        if (lexer.categorizer(ts[i]) == 0 and is_main == 0) and mode == 1:
            nts.append(Node(107))
            nts[-1].c = ts[start:i]
            nts.append(ts[i])
            start = i+1
            mode = 2
        elif (ts[i] == 'main' and is_main == 1 and i != 0 and ts[i-1] == 'int') and mode == 1:
            nts.append(Node(107))
            nts[-1].c = ts[start:i]
            nts.append(ts[i])
            start = i+1
            mode = 2        
        elif ts[i] == '(' and mode > 1 and mode < 4:
            pwait += 1
            if pwait == 0:
                nts.append('(')
                nts.append(Node(102))
                start = i+1
                mode = 3
        elif ts[i] == ')' and mode == 3:
            pwait -= 1
            if pwait == -1:
                nts.append(')')
                nts[-2].c = ts[start:i]
                start = i+1
                mode = 4
        elif mode == 4 and ts[i] != '{':
            break
        elif ts[i] == '{' and mode > 3:
            wait += 1
            if wait == 0:
                nts.append('{')
                nts.append(Node(101))
                start = i+1
                mode = 5
        elif ts[i] == '}' and mode == 5:
            wait -= 1
            if wait == -1:
                nts[-1].c = ts[start:i]
                nts.append('}')
                if i == len(ts)-1:
                    s = 1
    if s == 1:
        n.c = nts
        if is_main == 0: return pdtype(nts[0].c,nts) and pparamdef(nts[3].c,nts[3]) and pblock(nts[6].c,nts[6])
        else: return pparamdef(nts[3].c,nts[3],1) and pblock(nts[6].c,nts[6])
    else:
        print('Syntax Failure')
        return False

def pdtype(ts,n):
    return True

def pparamdef_s(ts,n):
    return pdtype(ts[:-1]) and lexer.categorizer(ts[-1]) == 0


def pparamdef(ts,n,is_main=0):
#Parses the def parameter token
    nts = []
    start = 0
    count = 0
    if is_main == 0:
        
        for i in range(len(ts)):
            if ts[i] == ',' and i != len(ts)-1:
                nts.append(Node(103))
                nts[-1].c = ts[start:i]
                nts.append(',')
                start = i+1
                count += 1

            elif i == len(ts)-1:
                nts.append(Node(103))
                nts[-1].c = ts[start:i+1]
                count += 1
        
        for i in range(0,count+2,2):
            if not pparamdef_s(nts[i].c,n):
                return False
        return True

    else:
        if ts == ["int", "argc", ',' ,"char", '*', 'argv', '[', ']']:
            nts = ["int", "argc", "char", '*', 'argv', '[', ']']
            n.c = nts
            return True
        elif ts == ['void']:
            nts = ['void']
            n.c = nts
            return True
        elif ts == []:
            n.c = nts
            return True
        else: 
            return False
    

def pblock(ts,n):
#Parses the block token
    
    nts = []
    start = 0
    wait = -1
    wsearch = 0

    for i in range(len(ts)):

        if ts[i] == ';' and wait == -1:
            if wsearch == 0: nts.append(Node(104))
            else: nts.append(Node(106))
        
            nts[-1].c = ts[start:i]
            nts.append(';')
            start = i+1
            wsearch = 0 

        if ts[i] == '{':    
            wait += 1
            if wait == 0:
                    nts.append(Node(105))
                    nts[-1].c = ts[start:i]
                    start = i+1
                    if nts[-1].c[0] == 'do':
                        wsearch = 1

        if ts[i] == '}' and wait != -1:
            wait -= 1
            if wait  == -1:
                nts.append('{')
                nts.append(Node(101))
                nts[-1].c = ts[start:i]
                nts.append('}')
                wait = -1
                start = i + 1

def main():
    if len(sys.argv) != 2:
        print("Unspecified File Failure")
        return
    
    f = open(sys.argv[1], 'r')
    ts = lexer.get_tokens(f)
    
    pprog(ts)

if __name__ == "__main__":
    main()