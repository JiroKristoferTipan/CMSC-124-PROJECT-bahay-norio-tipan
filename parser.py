def parse_program(tokens):
    current = 0

    if tokens[current][1] != "Code Start":
        raise SyntaxError("Program must start with HAI")

    current += 1  # skip HAI

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

        # Typecast: MAEK <var> A <type>
        case "Typecasting Start Operation":
            current = parse_typecast(tokens, current)

        # Single Comment: BTW
        case "Single Comment Line":
            current = parse_single_comment(tokens, current)

        # Multi-line Comment: OBTW ... TLDR
        case "Multi Comment Start":
            current = parse_multi_comment(tokens, current)

        # Default: Unknown statement
        case _:
            raise SyntaxError(
                f"Unexpected token '{tokens[current][0]}' at position {current}"
            )

    return current


def parse_typecast(tokens, current):
    if tokens[current][1] != "Typecasting Start Operation":  # MAEK
        raise SyntaxError(f"Expected 'MAEK' at token {current}")
    current += 1

    if tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable after 'MAEK' at token {current}")
    current += 1

    if tokens[current][1] != "Typecasting Value Operation":  # A
        raise SyntaxError(f"Expected 'A' after variable in typecast at token {current}")
    current += 1

    if tokens[current][1] != "Type Literal":  # NUMBR | NUMBAR | YARN | TROOF
        raise SyntaxError(f"Expected type literal after 'A' at token {current}")
    current += 1

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

    current = parse_expression(tokens, current)

    # Handle multiple outputs separated by AN
    while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":  # AN
        current += 1  # skip AN
        current = parse_expression(tokens, current)

    print("Parsed VISIBLE output successfully.")
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

    # Concatenation (SMOOSH)
    elif token_type == "String Concatenation":  # SMOOSH
        current = parse_concatenate(tokens, current)

    else:
        raise SyntaxError(
            f"Unexpected expression token '{tokens[current][0]}' at position {current}"
        )

    return current


def parse_concatenate(tokens, current):
    if tokens[current][1] != "String Concatenation":  # SMOOSH
        raise SyntaxError(f"Expected 'SMOOSH' at token {current}")
    current += 1  # skip SMOOSH

    # Expect at least one expression
    current = parse_expression(tokens, current)

    # Keep parsing expressions until MKAY
    while current < len(tokens) and tokens[current][1] != "Concatenation Delimiter":  # MKAY
        current = parse_expression(tokens, current)

    # Expect MKAY
    if current >= len(tokens) or tokens[current][1] != "Concatenation Delimiter":
        raise SyntaxError(f"Expected 'MKAY' to end SMOOSH at token {current}")

    current += 1  # skip MKAY
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

    # Skip until newline (or end)
    while current < len(tokens) and tokens[current][1] != "Newline":
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

    current += 1
    print("Parsed <multicomment> successfully.")
    return current

def parse_if_structure(tokens, current):
    # 1. Parse condition first
    current = parse_expression(tokens, current)  # condition before O RLY?

    # 2. Expect O RLY?
    if tokens[current][1] != "If Else Start":  # O RLY?
        raise SyntaxError(f"Expected 'O RLY?' after condition at token {current}")
    current += 1

    # 3. Expect YA RLY
    if tokens[current][1] != "If Keyword":  # YA RLY
        raise SyntaxError(f"Expected 'YA RLY' after 'O RLY?' at token {current}")
    current += 1

    # 4. Parse true branch (code block)
    current = parse_codeblock(tokens, current)

    # 5. Optional MEBBE (else if) chain
    while current < len(tokens) and tokens[current][1] == "Else If Keyword":  # MEBBE
        current = parse_multiifelse(tokens, current)

    # 6. Optional NO WAI (else)
    if current < len(tokens) and tokens[current][1] == "Else Keyword":  # NO WAI
        current += 1
        current = parse_codeblock(tokens, current)

    # 7. Expect OIC
    if current >= len(tokens) or tokens[current][1] != "If Else End":
        raise SyntaxError(f"Expected 'OIC' to end if-structure at token {current}")
    current += 1

    print("Parsed <ifstructure> successfully.")
    return current

def parse_multiifelse(tokens, current):
    if tokens[current][1] != "Else If Keyword":  # MEBBE
        raise SyntaxError(f"Expected 'MEBBE' at token {current}")
    current += 1

    # Condition after MEBBE
    current = parse_expression(tokens, current)

    # Code block for this branch
    current = parse_codeblock(tokens, current)

    print("Parsed <multiifelse> successfully.")
    return current

def parse_switchstructure(tokens, current):
    # Parse switch expression first
    current = parse_expression(tokens, current)

    if tokens[current][1] != "switch":  # WTF?
        raise SyntaxError(f"Expected 'WTF?' after condition at token {current}")
    current += 1

    # Parse all OMG cases
    while current < len(tokens) and tokens[current][1] == "Switch Case Keyword":  # OMG
        current = parse_multicase(tokens, current)

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

def parse_multicase(tokens, current):
    if tokens[current][1] != "Switch Case Keyword":  # OMG
        raise SyntaxError(f"Expected 'OMG' at token {current}")
    current += 1

    # Case value (YARN, NUMBR, TROOF, Variable, etc.)
    current = parse_expression(tokens, current)

    # Case code block
    current = parse_codeblock(tokens, current)

    print("Parsed <multicase> successfully.")
    return current

def parse_codeblock(tokens, current):
    while current < len(tokens) and tokens[current][1] not in [
        "If Else End", "Else If Keyword", "Else Keyword",
        "Switch Case Keyword", "Switch Default Keyword", "End something", "Code End"
    ]:
        current = parse_statement(tokens, current)
    return current
