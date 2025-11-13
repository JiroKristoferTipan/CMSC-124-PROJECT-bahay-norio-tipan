

def parse_statement(tokens, current):
    token_type = tokens[current][1]

    match token_type:
        case "Variable Declaration":  # e.g. I HAS A var
            current = parse_varDeclaration(tokens, current)
        
        ## ADD HERE

        case _:  # Default case
            raise SyntaxError(
                f"Unexpected token '{tokens[current][0]}' at position {current}"
            )

    return current


def parse_expression(tokens, current):
    if current < len(tokens) and tokens[current][1] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Variable"]:
        current += 1
    else:
        raise SyntaxError(f"Expected expression at token {current}")
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