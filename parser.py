# #functions from here are for catching specific syntax, use milestone 2 as reference
# def varDeclaration(line):
#     print(line)
#     if line[0] == "Variable Declaration" and line[1] == "Variable":
#         if len(line) == 2:
#             #only instantiation, no assignment
#             return "variable instantiation"
#         elif len(line) >= 4 and line[2] == "Variable Assignment on Declaration" and value(line[3]):
#             #instantiation with assignment
#             return "variable instantiation with assignment"
#         else:
#             return "invalid variable declaration"

# def value(line):
#     if line in ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]:
#         return True

# #<----------------------------------------------------------------------------------------------------------------------------->
# #helper for parser to split tokens by newline
# def splittokens(tokens):
#     splitlist = []
#     templist = []
#     for item in tokens:
#         if item[1] == "Newline":
#             if templist:
#                 splitlist.append(templist)
#                 templist = []
#         else :
#             templist.append(item[1])
#     if templist:
#         splitlist.append(templist)
#     # print(splitlist)
#     return splitlist

# # Main parser function 
# def parser(line):
#     splitlist = splittokens(line)
#     #test 1 only, normally shuold loop thru all
#     testparser = splitlist[2][0]
#     print(testparser)
#     #check start of every statement to see what it wants to do then pass to parser
#     #KULANG PA PLS ADD MORE TYVMMM
#     match testparser:
#         case "Code Start":
#             print("Code Start detected")
#         case "Variable Declaration":
#             print(varDeclaration(splitlist[2]))
#         case "Variable Assignment":
#             print("Variable Assignment detected")
#         case _:
#             print("No match, this should not happen")


def parse_statement(tokens, current):
    token_type = tokens[current][1]

    if token_type == "Variable Declaration":  # e.g. I HAS A var
        current = parse_variable_declaration(tokens, current)

    elif token_type == "Variable Assignment":  # e.g. var R 10
        current = parse_assignment(tokens, current)

    elif token_type == "Output Keyword":  # e.g. VISIBLE "Hello"
        current = parse_output(tokens, current)

    elif token_type == "Input Keyword":  # e.g. GIMMEH var
        current = parse_input(tokens, current)

    else:
        raise SyntaxError(f"Unexpected token '{tokens[current][0]}' at position {current}")

    return current
    
def parse_statement_list(tokens, current):
    while current < len(tokens) and tokens[current][1] != "Code End":
        current = parse_statement(tokens, current)
    return current

def parse_program(tokens):
    current = 0
    
    if tokens[current][1] != "Code Start":
        raise SyntaxError("Program must start with HAI")
    
    current += 1
    
    current = parse_statement_list(tokens, current)
    
    if tokens[current][1] != "Code End":
        raise SyntaxError("Program must end with KTHXBYE")

    print("Parsing Successful")
    return True