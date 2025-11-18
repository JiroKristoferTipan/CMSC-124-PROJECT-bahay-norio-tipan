#<-----------------------------------------------------------MAIN PARSE BLOCKS--------------------------------------------------------------------->

# checks if code has 'HAI' :3 and 'KTHXBYE'
def parse_program(tokens):
    current = 0

    #ignore comments before start of code
    current = parse_comments(tokens, current)

    #must start with 'HAI' :3
    if tokens[current][1] != "Code Start":
        raise SyntaxError("Program must start with HAI")
    current += 1  # skip HAI

    current = parse_statement_list(tokens, current)

    #must end
    if current >= len(tokens) or tokens[current][1] != "Code End":
        raise SyntaxError("Program must end with KTHXBYE")

    print("Parsing Successful.")
    return True

# checks if there are declarations(which should be the 1st line after HAI) and handles it; otherwise go thru every line and check syntax
def parse_statement_list(tokens, current):
    # remove stuff
    current = parse_comments(tokens, current)

    #if we need to declare any variables, needs 'WAZZUP'
    if current < len(tokens) and tokens[current][1] == "Start Declarations":
        current += 1    # this is for 'WAZZUP' keyword
        current = parse_comments(tokens, current)
        #keep going until 'BUHBYE' found
        while current < len(tokens) and tokens[current][1] != "End Declarations":
            current = parse_declarations(tokens, current)
            current = parse_comments(tokens, current)
        current += 1    # this is for 'BUHBYE' keyword
        current = parse_comments(tokens, current)

    #the rest of the code, must end at 'KTHXBYE'
    while current <= len(tokens) and tokens[current][1] != "Code End":
        current = parse_statement(tokens, current)
        current = parse_comments(tokens, current)
        print("Finished a statement!")
    return current

# code to check if maayos yung declarations
# ONLY accepts declarations here
def parse_declarations(tokens, current):
    #check if any comments
    current = parse_comments(tokens, current)
    if current > len(tokens) or tokens[current][1] != "Variable Declaration":                   # 'I HAS A'
        raise SyntaxError(f"Expected 'I HAS A' at position {current}")
    current += 1
    if current > len(tokens) or tokens[current][1] != "Variable":                               # variable
        raise SyntaxError(f"Expected variable at position {current}")
    current += 1
    if current < len(tokens) and tokens[current][1] == "Variable Assignment on Declaration":    # optional assignment
        current += 1                                                                            # 'ITZ'
        current = parse_expression(tokens, current, "Single")                                   # value to assign
    print("Successfully parsed a declaration!")
    return current
    
# determines what each statement is, looped by parse_statement_list to check all lines of code
# TODO FOR SEMANTICS: UNLESS THE LINE STARTS WITH USING 'parse_reassign', ALWAYS ASSIGN THE RESULT TO IMPLICIT VARIABLE IT
# THIS MUST BE DONE FROM THE OUTERMOST OPERATOR IF NESTED SYA WHICH IS LIKELY IN DEFAULT CASE
def parse_statement(tokens, current):
    # remove statement before statement
    current = parse_comments(tokens, current)
    token_type = tokens[current][1]
    print(token_type, "parse_statement")

    match token_type:
        # ignore newlines
        case "Newline":
            current += 1
        # these 2 arent rly huge blocks pero di bagay sa expression kase
        # VISIBLE
        case "Input Keyword":
            current = parse_input(tokens, current)

        # GIMMEH
        case "Output Keyword":
            current = parse_output(tokens, current)
        
        ## TODO: ADD HERE
        # if else, switch, loops, function
        case "If Else Start":
            current = parse_if_structure(tokens, current)

        case "switch":
            current = parse_switch_structure(tokens, current)

        case "Loop Start Keyword":
            current = parse_loop(tokens, current)

        case "Function Start":
            current = parse_function(tokens, current)

        # if not a huge block, check what the line does
        # so much cases in expression so i just made it default, do error checking in parse_expression's if else
        case _:  # Default case
            current = parse_expression(tokens, current, "Single")
    # removing comments after statement
    #current = parse_comments(tokens, current)
    return current

#<-----------------------------------------------------------DETERMINE VAR TYPE--------------------------------------------------------------------->

# Regarding param_type
# its either 'Single' or 'Multi'
# if single edi chill lang, pass lang ulit eto basically yung default which is why hardcoded sya sa parse_statement
# if detected smoosh, all of, any of, set to 'Multi' then DO NOT ACCEPT any more of these 3
# bawal kase sila mag nest so parang for making sure na isa lang

#string value expected
def parse_yarn(tokens, current, param_type):
    match tokens[current][1]:
        case "String Concatenation":
            current = parse_concatenate(tokens, current)

        #no matches somehow, shouldnt ever go here
        case _:
            raise SyntaxError(f"Expected numbr or numbar data type at position {current}")
    print("Successfully parsed a yarn!")
    return current

#int value expected
def parse_numbar(tokens, current, param_type):
    match tokens[current][1]:
        case "Add Operation":  # e.g. SUM OF
            current = parse_add(tokens, current, param_type)

        case "Subtract Operation":  # e.g. DIFF OF
            current = parse_subtract(tokens, current, param_type)

        case "Multiply Operation":  # e.g. PRODUKT OF
            current = parse_multiply(tokens, current, param_type)

        case "Divide Operation":  # e.g. QUOSHUNT OF
            current = parse_divide(tokens, current, param_type)

        case "Modulo Operation":  # e.g. MOD OF
            current = parse_modulo(tokens, current, param_type)

        case "Greater Operation":  # e.g. BIGGR OF
            current = parse_greater(tokens, current, param_type)

        case "Lesser Operation":  # e.g. SMALLR OF
            current = parse_lesser(tokens, current, param_type)

        #no matches somehow, shouldnt ever go here
        case _:
            raise SyntaxError(f"Expected numbr or numbar data type at position {current}")
    print("Successfully parsed a numbr/numbar!")
    return current

#bool value expected
def parse_troof(tokens, current, param_type):
    match tokens[current][1]:
        case "And Operation":  # e.g. BOTH OF
            current = parse_and(tokens, current, param_type)

        case "Or Operation":  # e.g. EITHER OF
            current = parse_or(tokens, current, param_type)

        case "Xor Operation":  # e.g. WON OF
            current = parse_xor(tokens, current, param_type)

        case "Not Operation":  # e.g. NOT
            current = parse_not(tokens, current, param_type)

        case "Equal Operation":  # e.g. BOTH SAEM
            current = parse_equal(tokens, current, param_type)

        case "Unequal Operation":  # e.g. DIFFRINT
            current = parse_unequal(tokens, current, param_type)

        case "Multi Or Operation":  # e.g. ANY OF
            current = parse_multi_or(tokens, current)

        case "Multi And Operation":  # e.g. ALL OF
            current = parse_multi_and(tokens, current)

        #no matches somehow, shouldnt ever go here
        case _:
            raise SyntaxError(f"Expected troof data type at position {current}")
    print("Successfully parsed a troof!")
    return current

# determine what type of data type we are expecting
# kailangan to for implicit typecasting
# TODO FOR SEMANTICS: when we have nested operations, need sya i typecast depending on
# previous operator so need ng isa pang parameter to see this
def parse_expression(tokens, current, param_type):
    token_type = tokens[current][1]

    # Literal
    if token_type in ["YARN", "NUMBR", "NUMBAR", "TROOF"]:
        print("Successfully parsed a literal!")
        current += 1

    # Numbr/Numbar operation
    elif token_type in [
        "Add Operation", "Subtract Operation", "Multiply Operation",
        "Divide Operation", "Modulo Operation", "Greater Operation", "Lesser Operation",
    ]:
        current = parse_numbar(tokens, current, param_type)  # check if number

    # Bool single operation
    elif token_type in [
        "Equal Operation", "Unequal Operation", "And Operation",
        "Or Operation", "Xor Operation", "Not Operation"
    ]:
        current = parse_troof(tokens, current, param_type) # check if single bool

    # Bool multi operation (IF YOU ALREADY HAVE MULTI, DO NOT NEST ANOTHER)
    elif token_type in [
        "Multi And Operation", "Multi Or Operation"
    ]:
        if param_type !="Multi":
            current = parse_troof(tokens, current, "Multi") # check if multi trool
        else:
            raise SyntaxError(f"Cannot nest infinite arity operators in token {current}")

    # String operation (IF YOU HAVE MULTI DO NOT NEST ANOTHER)
    elif token_type in ["String Concatenation"]:
        if param_type !="Multi":
            current = parse_yarn(tokens, current, "Multi") # check if concatenation
        else:
            raise SyntaxError(f"Cannot nest  infinite arity operators in token {current}")

    # Typecasting operation using 'MAEK'
    elif token_type == "Typecasting Start Operation":
        current = parse_typecast_make(tokens, current, param_type)
    
    elif token_type == "Variable":
        #check if reassign value by 'R' or typecast by 'IS NOW A'
        if current+1 < len(tokens) and tokens[current+1][1] == "Typecasting Operation":
            current = parse_typecast_isnow(tokens, current)
        elif current+1 < len(tokens) and tokens[current+1][1] == "Variable Assignment":
            current = parse_reassign(tokens, current, param_type)
        else:
            #its just a variable lmfao
            current += 1

    elif token_type == "Concatenation Delimiter":
        #in a multi arity operator, exit
        return current

    #maybe still in comment?
    elif token_type in ["Single Comment Line", "Multi Comment Start", "Multi Comment End"]:
        current = parse_comments(tokens, current)

    # not registered token found
    elif token_type == "Invalid":
        raise SyntaxError(f"Invalid token '{tokens[current][0]}' at position {current}")

    # Undetected token, idk pano mapupunta dito nilagay ko lang
    else:
        raise SyntaxError(f"Unexpected token '{tokens[current][0]}' at position {current}")
    current = parse_comments(tokens, current)
    return current

#<-----------------------------------------------------------BOOL FUNCTIONS--------------------------------------------------------------------->

# mostly binary operators
# skip operator, check if current is var/expr/literal, skip an, check if current is var/expr/literal
# TODO FOR SEMANTICS: implement actually solving right before return statement if 2 operands are allowed
# check bottom bool functions for infinite arity

def parse_and(tokens, current, param_type):
    current += 1 # Skip 'BOTH OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed an and!")
    return current

def parse_or(tokens, current, param_type):
    current += 1 # Skip 'EITHER OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed an or!")
    return current

def parse_xor(tokens, current, param_type):
    current += 1 # Skip 'WON OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a xor!")
    return current

def parse_not(tokens, current, param_type):
    current += 1 # Skip 'NOT'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    print("Successfully parsed a not!")
    return current

def parse_equal(tokens, current, param_type):
    current += 1 # Skip 'BOTH SAEM'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed an equal!")
    return current

def parse_unequal(tokens, current, param_type):
    current += 1 # Skip 'DIFFRINT'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed an unequal!")
    return current

# infinite arity operators
# skip operator, check if current is var/expr/literal, continuously skip an and then var/expr/literal until newline
# TODO FOR SEMANTICS: implement actually solving right before return statement if ALL operands are allowed

def parse_multi_or(tokens, current):
    current += 1 # Skip 'ANY OF'
    current = parse_expression(tokens, current, "Multi") # Parse first operand
    current = parse_multi_param(tokens, current, "Parameter Delimiter") # Parse additional operands
    if current >= len(tokens) or tokens[current][1] != "Concatenation Delimiter":
        raise SyntaxError(f"Expected 'MKAY' after 'ANY OF' in position {current}")
    current += 1 # skip 'MKAY'
    print("Successfully parsed an any!")
    return current

def parse_multi_and(tokens, current):
    current += 1 # Skip 'ALL OF'
    current = parse_expression(tokens, current, "Multi") # Parse first operand
    current = parse_multi_param(tokens, current, "Parameter Delimiter") # Parse additional operands
    if current >= len(tokens) or tokens[current][1] != "Concatenation Delimiter":
        raise SyntaxError(f"Expected 'MKAY' after 'ALL OF' in position {current}")
    current += 1 # skip 'MKAY'
    print("Successfully parsed an all!")
    return current

#<-----------------------------------------------------------INT FUNCTIONS--------------------------------------------------------------------->

# all binary operators
# skip operator, check if current is var/expr/literal, skip an, check if current is var/expr/literal
# TODO FOR SEMANTICS: implement actually solving right before return statement if 2 operands are allowed

def parse_add(tokens, current, param_type):
    current += 1 # Skip 'SUM OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed an add!")
    return current

def parse_subtract(tokens, current, param_type):
    current += 1 # Skip 'DIFF OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a sub!")
    return current

def parse_multiply(tokens, current, param_type):
    current += 1 # Skip 'PRODUKT OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a mult!")
    return current

def parse_divide(tokens, current, param_type):
    current += 1 # Skip 'QUOSHUNT OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a div!")
    return current

def parse_modulo(tokens, current, param_type):
    current += 1 # Skip 'MOD OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a mod!")
    return current

def parse_greater(tokens, current, param_type):
    current += 1 # Skip 'BIGGR OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a greater!")
    return current

def parse_lesser(tokens, current, param_type):
    current += 1 # Skip 'SMALLR OF'
    current = parse_expression(tokens, current, param_type) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current, param_type) # Parse second operand
    print("Successfully parsed a lesser!")
    return current

#<-----------------------------------------------------------STRING FUNCTIONS--------------------------------------------------------------------->

# infinite arity operator
# skip operator, check if current is var/expr/literal, continuously skip an and then var/expr/literal until newline
# TODO FOR SEMANTICS: implement actually solving right before return statement if ALL operands are allowed
def parse_concatenate(tokens, current):
    if tokens[current][1] != "String Concatenation":  # SMOOSH
        raise SyntaxError(f"Expected 'SMOOSH' at token {current}")
    current += 1  # skip SMOOSH

    # Expect at least one expression
    current = parse_expression(tokens, current, "Multi")
    current = parse_multi_param(tokens, current, "Parameter Delimiter") # Parse additional operands


    # current += 1  # skip MKAY
    print("Successfully parsed a concat!")
    return current

#<-----------------------------------------------------------VARIABLE FUNCTIONS--------------------------------------------------------------------->

# this doesnt actually edit the variable, it just make a result that is typecasted
# SEE 'parse_typecast_isnow' TO EDIT VARIABLE
def parse_typecast_make(tokens, current, param_type):
    # Should be confirmed at parse_expression pero nilagay ko na rin
    if tokens[current][1] != "Typecasting Start Operation":  # MAEK
        raise SyntaxError(f"Expected 'MAEK' at token {current}")
    current += 1

    # get variable to typecast
    current = parse_expression(tokens, current, param_type)

    if tokens[current][1] != "Typecasting Value Operation":  # A
        raise SyntaxError(f"Expected 'A' after variable in typecast at token {current}")
    current += 1

    if tokens[current][1] != "Type Literal":  # NUMBR | NUMBAR | YARN | TROOF
        raise SyntaxError(f"Expected type literal after 'A' at token {current}")
    current += 1
    print(current, "typcast")
    print("Successfully parsed a typecast!")
    return current

# actually edits the variable to a new data type
# SEE 'parse_typecast_make' TO NOT EDIT ORIGINAL VARIABLE
def parse_typecast_isnow(tokens, current):
    # we are typecasting, enter variable to typecast
    current += 1 # this is for the variable, confirmed at parse_expression
    current += 1 # this is for 'IS NOW A', confirmed at parse_expression

    if tokens[current][1] != "Type Literal":
        raise SyntaxError(f"Expected type literal after 'IS NOW A' at token {current}")
    current += 1
    print("Successfully parsed an explicit typecast!")
    return current

# skip var, reassign operator and next expression
# if the line doesnt have this at the start and its an operator, assign the answer to implicit variable IT
def parse_reassign(tokens, current, param_type):
    current += 1    # this is for variable, confirmed at parse_expression
    current += 1    # this is for 'R', confirmed at parse_expression

    # parse the new value being assigned
    current = parse_expression(tokens, current, param_type)
    print("Successfully parsed a reassign!")
    return current

#<-----------------------------------------------------------I/O FUNCTIONS--------------------------------------------------------------------->

# skip operator then check optional variable
def parse_input(tokens, current):
    current += 1 # 'GIMMEH', should be confirmed in parse_statement
    if current < len(tokens) and tokens[current][1] == "variable":
        #save input
        #if we go here, save to what ever the variable is; if not then save to 'IT'
        current += 1
    print("Successfully parsed an input!")
    return current

# skip operator then read expression
# TODO FOR SEMANTICS, implicit typecast the expression into string
def parse_output(tokens, current):
    current += 1 # 'VISIBLE', should be confirmed in parse_statement
    current = parse_expression(tokens, current, "Single")
    current = parse_multi_param(tokens, current, "Output Concatenation") # Parse additional operands
    #typecast output of parse expression to string then print
    print("Successfully parsed an output!")
    return current

#<-----------------------------------------------------------CONDITIONAL FUNCTIONS--------------------------------------------------------------------->

def parse_if_structure(tokens, current):
    # Parse optional condition (if wala then implicit 'IT' is condition)
    if current < len(tokens) and tokens[current][1] == "Variable":
        current = parse_expression(tokens, current)
    current = parse_comments(tokens, current) # remove newlines

    if tokens[current][1] != "If Else Start":  # O RLY?
        raise SyntaxError(f"Expected 'O RLY?' after condition at token {current}")
    current += 1
    current = parse_comments(tokens, current) # remove newlines

    if tokens[current][1] != "If Keyword":  # YA RLY
        raise SyntaxError(f"Expected 'YA RLY' after 'O RLY?' at token {current}")
    current += 1
    current = parse_codeblock(tokens, current)

    # THIS IS OPTIONAL PAGISIPAN KO NALANG TO PAG TAPOS NA SEMANTICS SIGURO
    # 5. Optional MEBBE (else if) chain
    # if tokens[current][1] == "Else If Keyword":
    #     current += 1
    #     while current < len(tokens) and tokens[current][1] != "Else If Keyword":  # MEBBE
    #         current = parse_statement(tokens, current)

    # 6. Optional NO WAI (else)
    if current < len(tokens) and tokens[current][1] == "Else Keyword":  # NO WAI
        current += 1 # parse 'NO WAI' because codeblock wont
        current = parse_codeblock(tokens, current)

    print(tokens[current][1], "if")
    # 7. Expect OIC
    if current >= len(tokens) or tokens[current][1] != "Conditional End":
        raise SyntaxError(f"Expected 'OIC' to end if-structure at token {current}")
    current += 1

    print("Successfully parsed an If-else!")
    return current

# def parse_multiifelse(tokens, current):
#     if tokens[current][1] != "Else If Keyword":  # MEBBE
#         raise SyntaxError(f"Expected 'MEBBE' at token {current}")
#     current += 1

#     # Condition after MEBBE
#     current = parse_expression(tokens, current)

#     # Code block for this branch
#     current = parse_codeblock(tokens, current)

#     print("Parsed <multiifelse> successfully.")
#     return current

def parse_switch_structure(tokens, current):
    #parang 'IT' lang ginagamit dito
    # Parse switch expression first
    # current = parse_expression(tokens, current)


    if tokens[current][1] != "switch":  # WTF?
        raise SyntaxError(f"Expected 'WTF?' after condition at token {current}")
    current += 2 # one for 'WTF?' keyword, one for newline

    # Parse all OMG cases
    while current < len(tokens) and tokens[current][1] == "Switch Case Keyword":  # OMG
        current = parse_multicase(tokens, current)
        if current >= len(tokens) or tokens[current][1] != "Switch Default Keyword":
            current += 1 # parse 'GTFO' 
        current = parse_comments(tokens, current)

    # Optional default case OMGWTF
    if current >= len(tokens) or tokens[current][1] != "Switch Default Keyword":  # OMGWTF
        raise SyntaxError(f"Expected 'OMGWTF' token in position {current}")
    current += 2 # parse 'OMGWTF' and newline
    while current < len(tokens) and tokens[current][1] != "Conditional End":
        current = parse_codeblock(tokens, current)

    # Expect OIC to end
    if current >= len(tokens) or tokens[current][1] != "Conditional End":  # OIC
        raise SyntaxError(f"Expected 'OIC' to end switch structure at token {current}")
    current += 1

    print("Successfully parsed a switch!")
    return current

def parse_multicase(tokens, current):
    if tokens[current][1] != "Switch Case Keyword":  # OMG
        raise SyntaxError(f"Expected 'OMG' at token {current}")
    current += 1

    # Case value (YARN, NUMBR, TROOF, Variable, etc.)
    current = parse_expression(tokens, current, "Single")

    # Case code block
    current = parse_codeblock(tokens, current)

    print("Parsed <multicase> successfully.")
    return current

#<-----------------------------------------------------------LOOP FUNCTIONS--------------------------------------------------------------------->

def parse_loop_condition(tokens, current):
    current += 1 # Skip 'IM IN YR'
    current = parse_expression(tokens, current, "Single") # Parse loop name
    if current < len(tokens) and tokens[current][1] == "Increment Operation":
        current = parse_increment(tokens, current)
    elif current < len(tokens) and tokens[current][1] == "Decrement Operation":
        current = parse_decrement(tokens, current)
    
    return current

def parse_loop(tokens, current):
    current = parse_loop_condition(tokens, current)
    current = parse_codeblock(tokens, current)
    # incase loop never closes
    if current >= len(tokens) and tokens[current][1] != "Loop End Keyword":
        raise SyntaxError(f"Expected 'IM OUTTA YR' to end loop at token {current}")
    current += 1  # Skip 'IM OUTTA YR'
    return current

def parse_increment(tokens, current):
    current += 1 # Skip 'UPPIN'
    if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
        raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
    current += 1 # Skip 'YR'
    current = parse_expression(tokens, current, "Single") # Parse variable
    # check for optional 'TIL'
    if current < len(tokens) and (tokens[current][1] == "Loop Keyword"):
        current += 1 # Skip 'TIL' or 'WILE'
        current = parse_expression(tokens, current,"Single") # Parse condition
    return current

def parse_decrement(tokens, current):
    current += 1 # Skip 'NERFIN'
    if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
        raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
    current += 1 # Skip 'YR'
    current = parse_expression(tokens, current, "Single") # Parse variable
    # check for optional 'TIL'
    if current < len(tokens) and (tokens[current][1] == "Loop Keyword"):
        current += 1 # Skip 'TIL' or 'WILE'
        current = parse_expression(tokens, current, "Single") # Parse condition
    return current

#<-----------------------------------------------------------FUNCTION FUNCTIONS--------------------------------------------------------------------->

def parse_multi_function_param(tokens, current):
    morethan2 = False
    #check if there actually is an additional parameter or none
    if current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
        current += 1 # Skip 'AN'
        if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
            raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
        current += 1 # Skip 'YR'
        current = parse_expression(tokens, current) #parse additional operand
        #check if more parameters exist, then parse if so
        if current+1 < len(tokens) and tokens[current+1][1] == "Concatenation Delimiter":
            morethan2 = True
            current += 1 # Skip 'AN'
            if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
                raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
            current += 1 # Skip 'YR'
            current = parse_expression(tokens, current) #parse additional operand
    #remove 'MKAY' if exists
    if (current >= len(tokens) or tokens[current][1] != "Concatenation Delimiter") and morethan2:
        raise SyntaxError(f"Expected 'MKAY' after last operand at token {current}")
    elif morethan2:
        current += 1 # Skip 'MKAY'
    return current
    
def parse_function_condition(tokens, current):
    current += 1  # Skip 'HOW IZ I'
    func_name = tokens[current][0]
    current = parse_expression(tokens, current)  # Parse function name
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment": # check for params with 'YR'
        current += 1  # Skip 'YR'
        current = parse_expression(tokens, current)  # Parse first parameter
        current = parse_multi_function_param(tokens, current)  # Parse additional parameters
    return current

def return_value(tokens, current):
    current += 1  # Skip 'GTFO' or 'FOUND YR'
    if current < len(tokens) and tokens[current][1] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Variable"]:
        current = parse_expression(tokens, current)  # Parse return expression
    return current

def parse_call_function(tokens, current):
    current += 1  # Skip 'I IZ'
    func_name = tokens[current][0]
    current = parse_expression(tokens, current)  # Parse function name
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment": # check for params with 'YR'
        current += 1  # Skip 'YR'
        current = parse_expression(tokens, current)  # Parse first parameter
        current = parse_multi_function_param(tokens, current)  # Parse additional parameters
    return current

def parse_function(tokens, current):
    current = parse_function_condition(tokens, current)
    while current < len(tokens) and tokens[current][1] != "Function End":  # e.g. IF U SAY SO
        continue
        #ADD CODEBLOCK HERE LATER
    if current >= len(tokens) and tokens[current][1] != "Function End":
        raise SyntaxError(f"Expected 'IF U SAY SO' to end function at token {current}")
    current += 1  # Skip 'IF U SAY SO'
    return current

#<-----------------------------------------------------------COMMENT FUNCTIONS--------------------------------------------------------------------->

# combined single and multi comments, checks if there are any then runs the appropriate one until no more comments
def parse_comments(tokens, current):
    #check if there even are comments
    while tokens[current][1] in ["Single Comment Line", "Multi Comment Start"]:
        if tokens[current][1] == "Single Comment Line":  # BTW
            current = parse_single_comment(tokens, current)
        elif tokens[current][1] == "Multi Comment Start":  # OBTW
            current = parse_multi_comment(tokens, current)
    #if none of these run, no comments exist

    #possible to have a newline, use this to fix
    while tokens[current][1] == "Newline":
        current += 1
    return current

# skip keyword then go to next line
def parse_single_comment(tokens, current):
    current += 1    # this is for 'BTW'

    # Skip until newline (or end)
    while current < len(tokens) and tokens[current][1] != "Newline":
        current += 1
    #currently at newline, skip it here
    current += 1
    print("Successfully parsed a single comment!")
    return current

# make sure no logic in same line of 'OBTW' and 'TLDR'
# do this by checking if they r in between newline tokens since comments dont have tokens
def parse_multi_comment(tokens, current):
    # OBTW should not be in same line as non comments
    if current+1 > len(tokens) or tokens[current-1][1] != "Newline":
        raise SyntaxError(f"Expected 'OBTW' to be isolated by newlines at token {current}")
    current += 1    # this one is for 'OBTW'

    # Skip all tokens until TLDR
    while current < len(tokens) and tokens[current][1] != "Multi Comment End":
        current += 1

    if current >= len(tokens) or tokens[current][1] != "Multi Comment End":
        raise SyntaxError(f"Expected 'TLDR' to close multi-line comment at token {current}")
    if current+1 > len(tokens) or tokens[current+1][1] != "Newline":
        raise SyntaxError(f"Expected 'TLDR' to be isolated by newlines at token {current}")
    current += 1    # this one is for 'TLDR'
    current += 1    # this one is for newline
    print("Successfully parsed a multi comment!")
    return current

#<-----------------------------------------------------------HELPER FUNCTIONS--------------------------------------------------------------------->

# for operators with at least 2 parameters (multi and, multi or, concatenate)
# continuously skip separator then next operand until no more separator
# "Parameter Delimiter" for 'AN', "Output Concatenation" for '+'
def parse_multi_param(tokens, current, separator):
    #check if there actually is an additional parameter or none
    if current >= len(tokens) or tokens[current][1] != separator:
        return current
    current += 1 # Skip separator
    current = parse_expression(tokens, current, "Multi") #parse additional operand
    #check if more parameters exist, then parse if so
    while current < len(tokens) and (tokens[current][1] == separator):
        current += 1 # Skip separator
        current = parse_expression(tokens, current, "Multi") #parse additional operand
    
    return current

def parse_codeblock(tokens, current):
    while current < len(tokens) and tokens[current][1] not in [
        "Conditional End", "Else If Keyword", "Else Keyword", "Loop End Keyword",
        "Switch Case Keyword", "Switch Default Keyword", "Code End", "Break Keyword", "Return Keyword"
    ]:
        print(tokens[current][1], "codeblock")
        current = parse_statement(tokens, current)
    print("Successfully parsed a codeblock!")
    return current