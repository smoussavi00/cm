# Finds tokens in a c file
def candidates(file):
    lines = file.read().splitlines()

    token = []

    for line in lines:
        for word in line.split():
            token.append(word)
    return token

def fsep(t):
    t2 = []
    for token in t:
        st = ""
        for char in token:
            if char in "{}[]();":
                if st != "":
                    t2.append(st)
                    st = ""
                t2.append(char)
            else:
                st = st + char
        if st != "":
            t2.append(st)  
    return t2
'''
 0 - Name
 1 - Integer Literal

 2 - Open Brace
 3 - Close Brace
 4 - Open Bracket
 5 - Close Bracket
 6 - Open Parenthesis
 7 - Close Parenthesis

 8 - Colon
 9 - Semicolon

 10 - return Keyword
 11 - main Keyword
 12 - int Keyword

100 - function
101 - statement
102 - parameters
'''
def categorizer(t):

    if t.isnumeric():
        return 1
    elif t == '{':
        return 2
    elif t == '}':
        return 3
    elif t == '[':
        return 4
    elif t == ']':
        return 5
    elif t == '(':
        return 6
    elif t == ')':
        return 7
    elif t == ':':
        return 8
    elif t == ';':
        return 9
    elif t == 'return':
        return 10
    elif t == 'main':
        return 11
    elif t == 'int':
        return 12
    else:
        return 0

def translator(n):
        if n == 0: return "User-defined Keyword"
        elif n == 1: return "Integer Literal"
        elif n == 2: return "Open Brace"
        elif n == 3: return "Close Brace"
        elif n == 4: return "Open Bracket"
        elif n == 5: return "Close Bracket"
        elif n == 6: return "Open Parenthesis"
        elif n == 7: return "Closed Parenthesis"
        elif n == 8: return "Colon"
        elif n == 9: return "Semicolon"
        elif n == 10: return "Keyword - return"
        elif n == 11: return "Keyword - main"
        elif n == 12: return "Keyword - int"
        elif n == 100: return "<FUNCTION>"
        elif n == 101: return "<BODY>"
        elif n == 102: return "<FUNCTION PARAMETERS>"
        else: return "--"
        
def get_tokens(file):
    return fsep(candidates(file))

def main():
    f = open('test.c', 'r')

if __name__ == "__main__":
    main()

