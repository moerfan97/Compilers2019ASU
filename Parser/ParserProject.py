import sys

tokens = [("read","READ"),
("x","IDENTIFIER"),
(";","SEMICOLON"),
("if","IF"),
("0","NUMBER"),
("<","LESSTHAN"),
("x","IDENTIFIER"),
("then","THEN"),
("fact","IDENTIFIER"),
(":=","ASSIGN"),
("1","NUMBER"),
(";","SEMICOLON"),
("repeat","REPEAT"),
("fact","IDENTIFIER"),
(":=","ASSIGN"),
("fact","IDENTIFIER"),
("*","MULT"),
("x","IDENTIFIER"),
(";","SEMICOLON"),
("x","IDENTIFIER"),
(":=","ASSIGN"),
("x","IDENTIFIER"),
("-","MINUS"),
("1","NUMBER"),
("until","UNTIL"),
("x","IDENTIFIER"),
("=","EQUAL"),
("0","NUMBER"),
(";","SEMICOLON"),
("write","WRITE"),
("fact","IDENTIFIER"),
("end","END")]

global_id=0
token_index = 0
level=0
flag=1
Nodes = []


def Error() :
    print("Error in program")
    return sys.exit()

def match(token):
    global token_index,tokens,Nodes,global_id,flag
    if token == tokens[token_index][0] or token == tokens[token_index][1] :
        token_index+=1
        if token_index == len(tokens) :
            token_index = 0
            return

    else :
        Error()

    return 

def program (level,id):
    stmt_sequence(level,id)
    modify_childrens()
    set_cord()
    print("Correct Program ^_^ ")
    return

def stmt_sequence(level,id):
    global token_index,tokens,Nodes,global_id,flag
    m = len(Nodes)
    statement(level,id)
    while tokens[token_index][0] == ';' :
        w = len(Nodes)
        match(';')
        statement(level,m)
        m = w

    return

def statement(level,id):
    global token_index,tokens,Nodes,global_id,flag
    if tokens[token_index][0] == "if" :
        if_stmt(level,id)

    elif tokens[token_index][0] == "repeat" :
        repeat_stmt(level,id)

    elif tokens[token_index][1] == "IDENTIFIER" :
        assign_stmt(level,id)

    elif tokens[token_index][0] == "read" :
        read_stmt(level,id)

    elif tokens[token_index][0] == "write" :
        write_stmt(level,id)

    else :
        Error()

    return

def if_stmt(level,id) :
    global token_index,tokens,Nodes,global_id,flag 
    Nodes.append(Node(tokens[token_index][0] ,"",level,id,"rect",2))
    indexOfIf=len(Nodes)-1
    idOfLastNode = global_id-1
    match("if")
    exp(level+1,idOfLastNode)
    match("then")
    stmt_sequence(level+1,idOfLastNode) 
    if tokens[token_index][0] == "else" :
        Nodes[indexOfIf].childrens_no+=1
        match("else")
        stmt_sequence(level+1,idOfLastNode)

    match("end")

    return

def repeat_stmt(level,id):
    global token_index,tokens,Nodes,global_id,flag 
    Nodes.append(Node(tokens[token_index][0] ,"",level,id,"rect",2))
    idOfLastNode = global_id-1
    match("repeat")
    stmt_sequence(level+1,idOfLastNode)
    match("until")
    exp(level+1,idOfLastNode)
    return

def assign_stmt(level,id) :
    global token_index,tokens,Nodes,global_id,flag
    Nodes.append(Node("assign" ,tokens[token_index][0] ,level,id,"rect",1))
    idOfLastNode = global_id-1
    match("IDENTIFIER")
    match(":=");
    exp(level+1 , idOfLastNode )
    return

def read_stmt(level,id):
    global token_index,tokens,Nodes,global_id,flag
    Nodes.append(Node("read" ,tokens[token_index+1][0] ,level,id,"rect",0))
    match("read")
    match("IDENTIFIER")
    return

def write_stmt(level,id):
    global token_index,tokens,Nodes,global_id,flag
    Nodes.append(Node("write" ,"",level,id,"rect",1))
    idOfLastNode = global_id-1
    match("write")
    exp(level+1,idOfLastNode)
    return
 
    
def exp(level,id):
    global token_index,tokens,Nodes,global_id,flag
    temp = simple_exp()
    if tokens[token_index][0] =="<"  or tokens[token_index][0] == "=" :
        idOfLastNode = comparison_op(temp,level,id)
        temp = simple_exp()
        correctLevels(temp,level+1,idOfLastNode)
    else:
        correctLevels(temp,level,id)
    return 

def comparison_op(temp,level,id) :
    global token_index,tokens,Nodes,global_id,flag
    if tokens[token_index][0] == "<" :
        Nodes.append(Node("op","<",level,id,"elipse",2))
        idOfLastNode = global_id-1
        correctLevels(temp,level+1,idOfLastNode)
        match("<")

    elif tokens[token_index][0] == "=" :
        Nodes.append(Node("op","=",level,id,"elipse",2))
        idOfLastNode = global_id-1
        correctLevels(temp,level+1,idOfLastNode)
        match("=")

    return idOfLastNode


def correctLevels(k,level,id):
    Nodes.append(Node(k.kind , k.tag,level,id,k.shape,k.childrens_no))
    idOfLastNode = global_id-1
    indexOfLastNode=len(Nodes)-1
    if Nodes[indexOfLastNode].childrens_no != 0 :
        left = k.childrens[0]
        right = k.childrens[1]
        correctLevels(left,level+1,idOfLastNode)
        correctLevels(right,level+1,idOfLastNode)


    return

def simple_exp() :
    global token_index,tokens,Nodes,global_id,flag
    temp = term()
    while tokens[token_index][0] == "+"  or tokens[token_index][0] == "-" :
        temp1 = addop()
        temp1.childrens.append(temp)
        temp = term()
        temp1.childrens.append(temp)
        temp = temp1

    return temp

def addop() :
    global token_index,tokens,Nodes,global_id,flag
    if tokens[token_index][0] == "+" :
        flag=0
        temp = Node("op","+",0,0,"elipse",2)
        flag=1
        match("+")

    elif tokens[token_index][0] == "-" :
        flag=0
        temp = Node("op","-",0,0,"elipse",2)
        flag=1
        match("-")

    else :
        Error()

    return temp

def term():
    global token_index,tokens,Nodes,global_id,flag
    temp = factor()
    while tokens[token_index][0] == "*"  or tokens[token_index][0] == "/" :
        temp1 = mulop()
        temp1.childrens.append(temp)
        temp = factor()
        temp1.childrens.append(temp)
        temp = temp1

    return temp

def mulop():
    global token_index,tokens,Nodes,global_id,flag
    if tokens[token_index][0] == "*" :
        flag=0
        temp = Node("op","*",0,0,"elipse",2)
        flag=1
        match("*")

    elif tokens[token_index][0] == "/" :
        flag=0
        temp = Node("op","/",0,0,"elipse",2)
        flag=1
        match("/")

    else :
        Error()

    return temp

def factor():
    global token_index,tokens,Nodes,global_id,flag
    if tokens[token_index][0] == "(" :
        match("(")
        temp = simple_exp()
        match(")")

    elif tokens[token_index][1] == "NUMBER" :
        flag=0
        temp = Node("const",tokens[token_index][0],0,0,"elipse",0)
        flag=1
        match("NUMBER");

    elif tokens[token_index][1] == "IDENTIFIER" :
        flag=0
        temp = Node("id",tokens[token_index][0],0,0,"elipse",0)
        flag=1
        match("IDENTIFIER")

    else :
        Error()

    return temp
       

def modify_childrens():
    m = len(Nodes)
    for i in range(m):
        count = 0
        for j in range(m):
            if Nodes[j].parent_id == i :
                Nodes[i].childrens.append(Nodes[j])
                count+=1
        Nodes[i].childrens_no = count
       

    return

class Node :
    def __init__(self, kind, text, level , parent_id , shape ,childrens_no = 0):
        global global_id,flag
        self.ID = global_id
        self.kind = kind
        self.tag = text
        self.level = level
        self.parent_id = parent_id
        self.shape = shape
        self.xCord = -1
        self.yCord = -1
        self.childrens_no = childrens_no
        self.childrens = []
        if flag == 1 :
            global_id+=1



def set_cord():
    
    nodesNo = len(Nodes)
    maxCol = 0
    Nodes[0].xCord = 0
    Nodes[0].yCord = 0
    for i in range(1,nodesNo):
        parent_id = Nodes[i].parent_id
        parent_level = Nodes[parent_id].level 
        my_id = Nodes[i].ID
        my_level = Nodes[i].level 
        Nodes[i].xCord = my_level
        if parent_level == my_level :
            Nodes[i].yCord = maxCol+1
            maxCol+=1
        else:
            if Nodes[parent_id].childrens_no > 0 :

                if my_id == Nodes[parent_id].childrens[0].ID :
                    Nodes[i].yCord =  Nodes[parent_id].yCord

                elif my_id == Nodes[parent_id].childrens[1].ID :
                    if Nodes[parent_id].yCord+1 > maxCol :
                        Nodes[i].yCord =  Nodes[parent_id].yCord+1
                        maxCol = Nodes[i].yCord
                    else:
                        Nodes[i].yCord = maxCol+1
                        maxCol = Nodes[i].yCord 

                elif my_id == Nodes[parent_id].childrens[2].ID :
                    if Nodes[parent_id].yCord+1 > maxCol :
                        Nodes[i].yCord =  Nodes[parent_id].yCord+1
                        maxCol = Nodes[i].yCord
                    else:
                        Nodes[i].yCord = maxCol+1
                        maxCol = Nodes[i].yCord 
           

    return



""" Main Function """

program(0,-1)


# Print list of Nodes
nodesNo = len(Nodes)
for i in range(nodesNo):
    print("ID :",Nodes[i].ID,"\t","Parent: " ,Nodes[i].parent_id,"\t","kind: " ,Nodes[i].kind,"(",Nodes[i].tag,")","level: ",Nodes[i].level,"Shape: ",Nodes[i].shape,"\t","childrens_no: " ,Nodes[i].childrens_no)
    for j in range(Nodes[i].childrens_no):
        print(Nodes[i].childrens[j].ID,"  ")

# Print Coordinates
for i in range(nodesNo):
    print("kind: " ,Nodes[i].kind,Nodes[i].tag,"\t",Nodes[i].xCord," ",Nodes[i].yCord)
