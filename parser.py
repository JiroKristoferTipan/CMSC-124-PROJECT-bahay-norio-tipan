

def parse_statement(tokens, current):
    token_type = tokens[current][1]

    match token_type:
        case "Variable Declaration":  # e.g. I HAS A var
            current = parse_varDeclaration(tokens, current)
        
        ## ADD HERE

        case "Add Operation":  # e.g. SUM OF
            current = parse_add(tokens, current)

        case "Subtract Operation":  # e.g. DIFF OF
            current = parse_subtract(tokens, current)

        case "Multiply Operation":  # e.g. PRODUKT OF
            current = parse_multiply(tokens, current)

        case "Divide Operation":  # e.g. QUOSHUNT OF
            current = parse_divide(tokens, current)

        case "Modulo Operation":  # e.g. MOD OF
            current = parse_modulo(tokens, current)

        case "Greater Operation":  # e.g. BIGGR OF
            current = parse_greater(tokens, current)

        case "Lesser Operation":  # e.g. SMALLR OF
            current = parse_lesser(tokens, current)

        case "And Operation":  # e.g. BOTH OF
            current = parse_and(tokens, current)

        case "Or Operation":  # e.g. EITHER OF
            current = parse_or(tokens, current)

        case "Xor Operation":  # e.g. WON OF
            current = parse_xor(tokens, current)

        case "Not Operation":  # e.g. NOT
            current = parse_not(tokens, current)

        case "Equal Operation":  # e.g. BOTH SAEM
            current = parse_equal(tokens, current)

        case "Unequal Operation":  # e.g. DIFFRINT
            current = parse_unequal(tokens, current)

        case "Multi Or Operation":  # e.g. ANY OF
            current = parse_multi_or(tokens, current)

        case "Multi And Operation":  # e.g. ALL OF
            current = parse_multi_and(tokens, current)

        case "Loop Start Keyword":  # e.g. IM IN YR
            current = parse_loop(tokens, current)

        case "switch":  # e.g. WTF?
            current = parse_switch(tokens, current)

        case "Increment Operation":  # e.g. UPPIN
            current = parse_increment(tokens, current)

        case "Decrement Operation":  # e.g. NERFIN
            current = parse_decrement(tokens, current)

        case "Function Start":  # e.g. HOW IZ I
            current = parse_function_definition(tokens, current)

        case "Return Keyword":  # e.g. GTFO or FOUND YR
            current = return_value(tokens, current)

        case "Function Call":  # e.g. I IZ
            current = parse_call_function(tokens, current)

        case "Newline":  # e.g. \n
            current += 1  # Just skip newlines

        case "Start something": # e.g. WAZZUP
            current += 1

        case "End something": # e.g. BUHBYE
            current += 1

        case _:  # Default case
            raise SyntaxError(
                f"Unexpected token '{tokens[current][0]}' '{tokens[current][1]}' at position {current}"
            )

    return current


def parse_expression(tokens, current):
    token_type = tokens[current][1]

    # Literal or variable
    if token_type in ["YARN", "NUMBR", "NUMBAR", "TROOF", "Variable"]:
        current += 1

    # Math or logic operation
    elif token_type in [
        "Add Operation", "Subtract Operation", "Multiply Operation",
        "Divide Operation", "Modulo Operation", "Equal Operation",
        "Unequal Operation", "Greater Operation", "Lesser Operation"
    ]:
        current += 1  # skip operation keyword
        current = parse_expression(tokens, current)  # left operand

        if tokens[current][1] != "Parameter Delimiter":  # expect AN
            raise SyntaxError(f"Expected 'AN' in expression at token {current}")
        current += 1

        current = parse_expression(tokens, current)  # right operand
    return current


def parse_varDeclaration(tokens, current):
    current += 1  # Skip 'I HAS A'

    # Must have a variable name next
    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable name after 'I HAS A' at token {current}")
    var_name = tokens[current][0]
    current += 1

    # Optional initialization
    if current < len(tokens) and tokens[current][1] == "Variable Assignment on Declaration":  # ITZ
        current += 1  # Skip 'ITZ'
        current = parse_expression(tokens, current)  # Handle expression parsing

    # End of declaration
    print(f"Declared variable '{var_name}' successfully.")
    return current

def parse_add(tokens, current):
    current += 1 # Skip 'SUM OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_subtract(tokens, current):
    current += 1 # Skip 'DIFF OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_multiply(tokens, current):
    current += 1 # Skip 'PRODUKT OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_divide(tokens, current):
    current += 1 # Skip 'QUOSHUNT OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_modulo(tokens, current):
    current += 1 # Skip 'MOD OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_arithmetic(tokens, current, operator):
    if current >= len(tokens) or not tokens[current][1] in ["Addition Operation", "Subtraction Operation", "Multiplication Operation", "Division Operation","Modulo Operation"]:
        raise SyntaxError(f"Expected arithmetic operator at token {current}")
    current += 1 # Skip operator
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_greater(tokens, current):
    current += 1 # Skip 'BIGGR OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_lesser(tokens, current):
    current += 1 # Skip 'SMALLR OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_and(tokens, current):
    current += 1 # Skip 'BOTH OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_or(tokens, current):
    current += 1 # Skip 'EITHER OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_xor(tokens, current):
    current += 1 # Skip 'WON OF'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_not(tokens, current):
    current += 1 # Skip 'NOT'
    current = parse_expression(tokens, current) # Parse first operand
    return current

def parse_equal(tokens, current):
    current += 1 # Skip 'BOTH SAEM'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_unequal(tokens, current):
    current += 1 # Skip 'DIFFRINT'
    current = parse_expression(tokens, current) # Parse first operand
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) # Parse second operand
    return current

def parse_multi_param(tokens, current):
    morethan2 = False
    #check if there actually is an additional parameter or none
    if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
        raise SyntaxError(f"Expected 'AN' after first operand at token {current}")
    current += 1 # Skip 'AN'
    current = parse_expression(tokens, current) #parse additional operand
    #check if more parameters exist, then parse if so
    while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
        morethan2 = True
        current += 1 # Skip 'AN'
        current = parse_expression(tokens, current) #parse additional operand
    #remove 'MKAY' if exists
    if (current >= len(tokens) or tokens[current][1] != "Concatenation Delimiter") and morethan2:
        raise SyntaxError(f"Expected 'MKAY' after last operand at token {current}")
    elif morethan2:
        current += 1 # Skip 'MKAY'
    return current

def parse_multi_or(tokens, current):
    current += 1 # Skip 'ANY OF'
    current = parse_expression(tokens, current) # Parse first operand
    current = parse_multi_param(tokens, current) # Parse additional operands
    return current

def parse_multi_and(tokens, current):
    current += 1 # Skip 'ALL OF'
    current = parse_expression(tokens, current) # Parse first operand
    current = parse_multi_param(tokens, current) # Parse additional operands
    return current

def parse_loop_start(tokens, current):
    current += 1 # Skip 'IM IN YR'
    current = parse_expression(tokens, current) # Parse loop name
    if current < len(tokens) and (tokens[current][1] == "Increment Operation" or tokens[current][1] == "Decrement Operation"):
        current += 1 # Skip 'UPPIN' or 'NERFIN'
        if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
            raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
        current += 1 # Skip 'YR'
        current = parse_expression(tokens, current) # Parse variable
        if current < len(tokens) and (tokens[current][1] == "Loop Keyword"):
            current += 1 # Skip 'TIL' or 'WILE'
            current = parse_expression(tokens, current) # Parse condition
    return current

def parse_loop_end(tokens, current):
    current += 1 # Skip 'IM OUTTA YR'
    return current

def parse_loop(tokens, current):
    current = parse_loop_start(tokens, current)
    while current < len(tokens) and tokens[current][1] != "Loop End Keyword":  # e.g. IM OUTTA YR
        continue
        #ADD CODEBLOCK HERE LATER
    if current >= len(tokens) and tokens[current][1] != "Loop End Keyword":
        raise SyntaxError(f"Expected 'IM OUTTA YR' to end loop at token {current}")
    current += 1  # Skip 'IM OUTTA YR'
    return current

def parse_increment(tokens, current):
    current += 1 # Skip 'UPPIN'
    if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
        raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
    current += 1 # Skip 'YR'
    current = parse_expression(tokens, current) # Parse variable
    return current

def parse_decrement(tokens, current):
    current += 1 # Skip 'NERFIN'
    if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
        raise SyntaxError(f"Expected 'YR' after first operand at token {current}")
    current += 1 # Skip 'YR'
    current = parse_expression(tokens, current) # Parse variable
    return current

def parse_switch(tokens, current):
    current += 1  # Skip 'WTF?'
    while current < len(tokens) and tokens[current][1] not in ["Switch Default Keyword", "If Else End"]:  # e.g. OMGWTF or OIC
        if tokens[current][1] != "Switch Case Keyword":  # e.g. OMG
            raise SyntaxError(f"Expected 'OMG' for switch case at token {current}")
        current += 1  # Skip 'OMG'
        current = parse_expression(tokens, current)  # Parse case expression
        continue
        #ADD CODEBLOCK HERE LATER
    if current >= len(tokens) and tokens[current][1] != "Switch Default Keyword":
        raise SyntaxError(f"Expected 'OMGWTF' ketword at token {current}")
    current += 1  # Skip 'OMGWTF'
    #ADD CODEBLOCK HERE LATER
    if current >= len(tokens) and tokens[current][1] != "If Else End":
        raise SyntaxError(f"Expected 'OIC' keyword at token {current}")
    current += 1  # Skip 'OIC'
    return current

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

def parse_function_definition(tokens, current):
    current = parse_function_condition(tokens, current)
    while current < len(tokens) and tokens[current][1] != "Function End":  # e.g. IF U SAY SO
        continue
        #ADD CODEBLOCK HERE LATER
    if current >= len(tokens) and tokens[current][1] != "Function End":
        raise SyntaxError(f"Expected 'IF U SAY SO' to end function at token {current}")
    current += 1  # Skip 'IF U SAY SO'
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