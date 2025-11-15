def parse_program(tokens):
    current = 0

    # Skip comments and newlines before HAI
    while current < len(tokens) and tokens[current][1] in ["Single Comment Line", "Multi Comment Start", "Newline"]:
        if tokens[current][1] == "Single Comment Line":
            current = parse_single_comment(tokens, current)
        elif tokens[current][1] == "Multi Comment Start":
            current = parse_multi_comment(tokens, current)
        else:
            current += 1  # skip newline

    if current >= len(tokens) or tokens[current][1] != "Code Start":
        raise SyntaxError("Program must start with HAI")

    current += 1  # skip HAI

    # Skip newlines after HAI
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    current = parse_statement_list(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "Code End":
        raise SyntaxError("Program must end with KTHXBYE")

    print("Parsing Successful.")
    return True


def parse_statement_list(tokens, current):
    while current < len(tokens) and tokens[current][1] != "Code End":
        current = parse_statement(tokens, current)
    return current


def parse_statement(tokens, current):
    token_type = tokens[current][1]

    match token_type:
        # Variable Declaration: I HAS A
        case "Variable Declaration":
            current = parse_varDeclaration(tokens, current)

        # Variable Initialization Section: WAZZUP ... BUHBYE
        case "Start something":
            current = parse_varInitSection(tokens, current)

        # Output: VISIBLE
        case "Output Keyword":
            current = parse_output(tokens, current)

        # Input: GIMMEH
        case "Input Keyword":
            current = parse_input(tokens, current)

        # Typecast: MAEK <var> A <type> or <var> IS NOW A <type>
        case "Typecasting Start Operation":
            current = parse_typecast(tokens, current)

        # Single Comment: BTW
        case "Single Comment Line":
            current = parse_single_comment(tokens, current)

        # Multi-line Comment: OBTW ... TLDR
        case "Multi Comment Start":
            current = parse_multi_comment(tokens, current)

        # Expressions as statements (can appear standalone before O RLY? or WTF?)
        case "Add Operation" | "Subtract Operation" | "Multiply Operation" | "Divide Operation" | "Modulo Operation" | "Greater Operation" | "Lesser Operation" | "And Operation" | "Or Operation" | "Xor Operation" | "Not Operation" | "Equal Operation" | "Unequal Operation" | "Multi Or Operation" | "Multi And Operation" | "String Concatenation":
            current = parse_expression(tokens, current)

        # Control Flow
        case "If Else Start":
            current = parse_if_structure(tokens, current)
        
        case "switch":
            current = parse_switch(tokens, current)
        
        case "Loop Start Keyword":
            current = parse_loop(tokens, current)

        # Functions
        case "Function Start":
            current = parse_function_definition(tokens, current)
        
        case "Return Keyword":
            current = parse_return_value(tokens, current)
        
        case "Function Call":
            current = parse_call_function(tokens, current)

        # Variable Assignment: <var> R <expr> or <var> IS NOW A <type>
        case "Variable":
            if current + 1 < len(tokens):
                next_token = tokens[current + 1][1]
                if next_token == "Variable Assignment":
                    current += 1  # skip variable
                    current += 1  # skip R
                    current = parse_expression(tokens, current)
                elif next_token == "Typecasting Operation":
                    # <var> IS NOW A <type>
                    current += 1  # skip variable
                    current += 1  # skip IS NOW A
                    if tokens[current][1] != "Type Literal":
                        raise SyntaxError(f"Expected type literal after 'IS NOW A' at token {current}")
                    current += 1  # skip type
                else:
                    # Standalone variable (could be before WTF?)
                    current += 1
            else:
                current += 1

        # Newline
        case "Newline":
            current += 1

        case _:
            raise SyntaxError(f"Unexpected token '{tokens[current][0]}' ('{tokens[current][1]}') at position {current}")

    return current


def parse_typecast(tokens, current):
    if tokens[current][1] != "Typecasting Start Operation":  # MAEK
        raise SyntaxError(f"Expected 'MAEK' at token {current}")
    current += 1

    # MAEK A <var> <type>
    if tokens[current][1] == "Typecasting Value Operation":  # A
        current += 1  # skip A
        if tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'MAEK A' at token {current}")
        current += 1  # skip variable
        if tokens[current][1] != "Type Literal":
            raise SyntaxError(f"Expected type literal at token {current}")
        current += 1  # skip type
    # MAEK <var> A <type>
    else:
        if tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'MAEK' at token {current}")
        current += 1  # skip variable

        if tokens[current][1] != "Typecasting Value Operation":  # A
            raise SyntaxError(f"Expected 'A' after variable in typecast at token {current}")
        current += 1  # skip A

        if tokens[current][1] != "Type Literal":
            raise SyntaxError(f"Expected type literal after 'A' at token {current}")
        current += 1  # skip type

    print("Parsed <typecast> successfully.")
    return current


def parse_varDeclaration(tokens, current):
    current += 1  # skip 'I HAS A'

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable name after 'I HAS A' at token {current}")
    var_name = tokens[current][0]
    current += 1

    # Optional initialization
    if current < len(tokens) and tokens[current][1] == "Variable Assignment on Declaration":  # ITZ
        current += 1  # skip ITZ
        current = parse_expression(tokens, current)

    print(f"Declared variable '{var_name}' successfully.")
    return current


def parse_varInitSection(tokens, current):
    current += 1  # skip WAZZUP

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    # Parse statements inside section
    while current < len(tokens) and tokens[current][1] != "End something":  # BUHBYE
        current = parse_statement(tokens, current)

    # Expect BUHBYE
    if current >= len(tokens) or tokens[current][1] != "End something":
        raise SyntaxError(f"Expected 'BUHBYE' to close varinitsection at token {current}")

    current += 1  # skip BUHBYE
    print("Parsed <varinitsection> successfully.")
    return current


def parse_output(tokens, current):
    current += 1  # skip VISIBLE

    # Parse first expression
    current = parse_expression(tokens, current)

    # Handle multiple outputs separated by space (implicit) or AN
    while current < len(tokens) and tokens[current][1] in ["Parameter Delimiter", "YARN", "NUMBR", "NUMBAR", "TROOF", "Variable"]:
        if tokens[current][1] == "Parameter Delimiter":
            current += 1  # skip AN
        current = parse_expression(tokens, current)

    print("Parsed VISIBLE output successfully.")
    return current


def parse_expression(tokens, current):
    if current >= len(tokens):
        raise SyntaxError(f"Unexpected end of tokens in expression")

    token_type = tokens[current][1]

    # Literal or variable
    if token_type in ["YARN", "NUMBR", "NUMBAR", "TROOF", "Variable", "Void Literal"]:
        current += 1
        
        # Handle concatenation operator (+)
        while current < len(tokens) and tokens[current][1] == "Concatenation Operator":
            current += 1  # skip +
            if current >= len(tokens):
                raise SyntaxError(f"Expected expression after '+' at token {current}")
            # Recursively parse the next expression (handles nested operations)
            current = parse_expression(tokens, current)

    # Binary operations (require two operands with AN)
    elif token_type in [
        "Add Operation", "Subtract Operation", "Multiply Operation",
        "Divide Operation", "Modulo Operation", "Equal Operation",
        "Unequal Operation", "Greater Operation", "Lesser Operation",
        "And Operation", "Or Operation", "Xor Operation"
    ]:
        current += 1  # skip operation keyword
        current = parse_expression(tokens, current)  # left operand

        if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":  # expect AN
            raise SyntaxError(f"Expected 'AN' in binary operation at token {current}")
        current += 1  # skip AN

        current = parse_expression(tokens, current)  # right operand

    # Unary operation (NOT)
    elif token_type == "Not Operation":
        current += 1  # skip NOT
        current = parse_expression(tokens, current)

    # Multi-operand operations (ANY OF, ALL OF)
    elif token_type in ["Multi Or Operation", "Multi And Operation"]:
        current += 1  # skip operation
        current = parse_expression(tokens, current)  # first operand
        
        # At least one more operand required
        if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
            raise SyntaxError(f"Expected 'AN' after first operand in multi-operation at token {current}")
        current += 1  # skip AN
        current = parse_expression(tokens, current)  # second operand

        # Additional operands (optional, ended by MKAY)
        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
            current += 1  # skip AN
            current = parse_expression(tokens, current)

        # Expect MKAY to end multi-operation
        if current < len(tokens) and tokens[current][1] == "Concatenation Delimiter":
            current += 1  # skip MKAY

    # String Concatenation (SMOOSH)
    elif token_type == "String Concatenation":
        current = parse_concatenate(tokens, current)

    # Typecast expression (MAEK)
    elif token_type == "Typecasting Start Operation":
        current = parse_typecast(tokens, current)

    # Function call
    elif token_type == "Function Call":
        current = parse_call_function(tokens, current)

    else:
        raise SyntaxError(f"Unexpected expression token '{tokens[current][0]}' ('{token_type}') at position {current}")

    return current


def parse_concatenate(tokens, current):
    if tokens[current][1] != "String Concatenation":  # SMOOSH
        raise SyntaxError(f"Expected 'SMOOSH' at token {current}")
    current += 1  # skip SMOOSH

    # Expect at least one expression
    current = parse_expression(tokens, current)

    # Keep parsing expressions with AN delimiter
    while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
        current += 1  # skip AN
        current = parse_expression(tokens, current)

    print("Parsed SMOOSH concatenation successfully.")
    return current


def parse_input(tokens, current):
    if tokens[current][1] != "Input Keyword":  # GIMMEH
        raise SyntaxError(f"Expected 'GIMMEH' at token {current}")
    current += 1

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable after 'GIMMEH' at token {current}")
    current += 1

    print("Parsed <userinput> successfully.")
    return current


def parse_single_comment(tokens, current):
    if tokens[current][1] != "Single Comment Line":  # BTW
        raise SyntaxError(f"Expected 'BTW' at token {current}")
    current += 1

    # Skip until newline (comments are already handled by tokenizer)
    while current < len(tokens) and tokens[current][1] != "Newline":
        current += 1

    if current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    print("Parsed <singlecomment> successfully.")
    return current


def parse_multi_comment(tokens, current):
    if tokens[current][1] != "Multi Comment Start":  # OBTW
        raise SyntaxError(f"Expected 'OBTW' at token {current}")
    current += 1

    # Skip all tokens until TLDR
    while current < len(tokens) and tokens[current][1] != "Multi Comment End":
        current += 1

    if current >= len(tokens) or tokens[current][1] != "Multi Comment End":
        raise SyntaxError(f"Expected 'TLDR' to close multi-line comment at token {current}")

    current += 1  # skip TLDR
    print("Parsed <multicomment> successfully.")
    return current


def parse_if_structure(tokens, current):
    # Expect O RLY? (condition should be evaluated before this)
    if tokens[current][1] != "If Else Start":  # O RLY?
        raise SyntaxError(f"Expected 'O RLY?' at token {current}")
    current += 1

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    # Expect YA RLY
    if tokens[current][1] != "If Keyword":  # YA RLY
        raise SyntaxError(f"Expected 'YA RLY' after 'O RLY?' at token {current}")
    current += 1

    # Parse true branch
    current = parse_codeblock(tokens, current)

    # Optional MEBBE (else if) chain
    while current < len(tokens) and tokens[current][1] == "Else If Keyword":  # MEBBE
        current += 1  # skip MEBBE
        current = parse_expression(tokens, current)  # condition
        current = parse_codeblock(tokens, current)

    # Optional NO WAI (else)
    if current < len(tokens) and tokens[current][1] == "Else Keyword":  # NO WAI
        current += 1
        current = parse_codeblock(tokens, current)

    # Expect OIC
    if current >= len(tokens) or tokens[current][1] != "If Else End":
        raise SyntaxError(f"Expected 'OIC' to end if-structure at token {current}")
    current += 1

    print("Parsed <ifstructure> successfully.")
    return current


def parse_switch(tokens, current):
    if tokens[current][1] != "switch":  # WTF?
        raise SyntaxError(f"Expected 'WTF?' at token {current}")
    current += 1

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    # Parse all OMG cases
    while current < len(tokens) and tokens[current][1] == "Switch Case Keyword":  # OMG
        current += 1  # skip OMG
        current = parse_expression(tokens, current)  # case value
        current = parse_codeblock(tokens, current)

    # Optional default case OMGWTF
    if current < len(tokens) and tokens[current][1] == "Switch Default Keyword":  # OMGWTF
        current += 1
        current = parse_codeblock(tokens, current)

    # Expect OIC to end
    if current >= len(tokens) or tokens[current][1] != "If Else End":  # OIC
        raise SyntaxError(f"Expected 'OIC' to end switch structure at token {current}")
    current += 1

    print("Parsed <switchstructure> successfully.")
    return current


def parse_codeblock(tokens, current):
    # Skip newlines at start of block
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    # Parse statements until we hit a block terminator
    while current < len(tokens) and tokens[current][1] not in [
        "If Else End", "Else If Keyword", "Else Keyword",
        "Switch Case Keyword", "Switch Default Keyword", 
        "End something", "Code End", "Function End", "Loop End Keyword"
    ]:
        current = parse_statement(tokens, current)

    return current


def parse_loop(tokens, current):
    current += 1  # Skip 'IM IN YR'

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected loop label after 'IM IN YR' at token {current}")
    loop_label = tokens[current][0]
    current += 1  # skip loop label

    # Optional operation and condition
    if current < len(tokens) and tokens[current][1] in ["Increment Operation", "Decrement Operation"]:
        current += 1  # Skip 'UPPIN' or 'NERFIN'

        if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
            raise SyntaxError(f"Expected 'YR' after operation at token {current}")
        current += 1  # Skip 'YR'

        if tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'YR' at token {current}")
        current += 1  # skip variable

        # Optional condition (TIL or WILE)
        if current < len(tokens) and tokens[current][1] == "Loop Keyword":
            current += 1  # Skip 'TIL' or 'WILE'
            current = parse_expression(tokens, current)  # Parse condition

    # Parse loop body
    current = parse_codeblock(tokens, current)

    # Expect IM OUTTA YR
    if current >= len(tokens) or tokens[current][1] != "Loop End Keyword":
        raise SyntaxError(f"Expected 'IM OUTTA YR' to end loop at token {current}")
    current += 1  # Skip 'IM OUTTA YR'

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected loop label after 'IM OUTTA YR' at token {current}")
    current += 1  # skip loop label

    print(f"Parsed loop '{loop_label}' successfully.")
    return current


def parse_function_definition(tokens, current):
    current += 1  # Skip 'HOW IZ I'

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected function name after 'HOW IZ I' at token {current}")
    func_name = tokens[current][0]
    current += 1

    # Optional parameters
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":  # YR
        current += 1  # Skip 'YR'

        if tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected parameter name after 'YR' at token {current}")
        current += 1

        # Additional parameters
        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":  # AN
            current += 1  # Skip 'AN'
            
            if tokens[current][1] != "Loop Variable Assignment":
                raise SyntaxError(f"Expected 'YR' in parameter list at token {current}")
            current += 1  # Skip 'YR'

            if tokens[current][1] != "Variable":
                raise SyntaxError(f"Expected parameter name at token {current}")
            current += 1

    # Parse function body
    current = parse_codeblock(tokens, current)

    # Expect IF U SAY SO
    if current >= len(tokens) or tokens[current][1] != "Function End":
        raise SyntaxError(f"Expected 'IF U SAY SO' to end function at token {current}")
    current += 1

    print(f"Parsed function '{func_name}' successfully.")
    return current


def parse_return_value(tokens, current):
    return_type = tokens[current][0]
    current += 1  # Skip 'GTFO' or 'FOUND YR'

    # FOUND YR requires a return value
    if return_type == "FOUND YR":
        current = parse_expression(tokens, current)

    print("Parsed <return> successfully.")
    return current


def parse_call_function(tokens, current):
    current += 1  # Skip 'I IZ'

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected function name after 'I IZ' at token {current}")
    func_name = tokens[current][0]
    current += 1

    # Optional arguments
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":  # YR
        current += 1  # Skip 'YR'
        current = parse_expression(tokens, current)

        # Additional arguments
        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":  # AN
            current += 1  # Skip 'AN'

            if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":
                current += 1  # Skip 'YR'

            current = parse_expression(tokens, current)

        # Optional MKAY
        if current < len(tokens) and tokens[current][1] == "Concatenation Delimiter":
            current += 1  # Skip 'MKAY'

    print(f"Parsed function call '{func_name}' successfully.")
    return current