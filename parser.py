import json

def parse_program(tokens):
    current = 0

    # Skip comments and newlines before HAI
    while current < len(tokens) and tokens[current][1] in ["Single Comment Line", "Multi Comment Start", "Newline"]:
        if tokens[current][1] == "Single Comment Line":
            _, current = parse_single_comment(tokens, current)
        elif tokens[current][1] == "Multi Comment Start":
            _, current = parse_multi_comment(tokens, current)
        else:
            current += 1  # skip newline

    if current >= len(tokens) or tokens[current][1] != "Code Start":
        raise SyntaxError("Program must start with HAI")

    current += 1  # skip HAI

    # Skip newlines after HAI
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    statements, current = parse_statement_list(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "Code End":
        raise SyntaxError("Program must end with KTHXBYE")

    ast = {
        "type": "Program",
        "body": statements
    }

    print("Parsing Successful.")
    
    return ast


def parse_statement_list(tokens, current):
    statements = []
    while current < len(tokens) and tokens[current][1] != "Code End":
        stmt, current = parse_statement(tokens, current)
        if stmt:
            statements.append(stmt)
    return statements, current


def parse_statement(tokens, current):
    if current >= len(tokens):
        raise SyntaxError(f"Unexpected end of tokens")
    
    token_type = tokens[current][1]

    match token_type:
        # Variable Declaration: I HAS A
        case "Variable Declaration":
            return parse_varDeclaration(tokens, current)

        # Variable Initialization Section: WAZZUP ... BUHBYE
        case "Start something":
            return parse_varInitSection(tokens, current)

        # Output: VISIBLE
        case "Output Keyword":
            return parse_output(tokens, current)

        # Input: GIMMEH
        case "Input Keyword":
            return parse_input(tokens, current)

        # Typecast: MAEK <var> A <type> or <var> IS NOW A <type>
        case "Typecasting Start Operation":
            return parse_typecast(tokens, current)

        # Single Comment: BTW
        case "Single Comment Line":
            return parse_single_comment(tokens, current)

        # Multi-line Comment: OBTW ... TLDR
        case "Multi Comment Start":
            return parse_multi_comment(tokens, current)

        # Expressions as statements
        case "Add Operation" | "Subtract Operation" | "Multiply Operation" | "Divide Operation" | "Modulo Operation" | "Greater Operation" | "Lesser Operation" | "And Operation" | "Or Operation" | "Xor Operation" | "Not Operation" | "Equal Operation" | "Unequal Operation" | "Multi Or Operation" | "Multi And Operation" | "String Concatenation":
            expr, current = parse_expression(tokens, current)
            return {"type": "ExpressionStatement", "expression": expr}, current

        # Control Flow
        case "If Else Start":
            return parse_if_structure(tokens, current)
        
        case "switch":
            return parse_switch(tokens, current)
        
        case "Loop Start Keyword":
            return parse_loop(tokens, current)

        # Functions
        case "Function Start":
            return parse_function_definition(tokens, current)
        
        case "Return Keyword":
            return parse_return_value(tokens, current)
        
        case "Function Call":
            expr, current = parse_call_function(tokens, current)
            return {"type": "ExpressionStatement", "expression": expr}, current

        # Variable Assignment
        case "Variable":
            if current + 1 < len(tokens):
                next_token = tokens[current + 1][1]
                if next_token == "Variable Assignment":
                    var_name = tokens[current][0]
                    current += 2  # skip variable and R
                    expr, current = parse_expression(tokens, current)
                    return {
                        "type": "Assignment",
                        "variable": var_name,
                        "value": expr
                    }, current
                elif next_token == "Typecasting Operation":
                    var_name = tokens[current][0]
                    current += 2  # skip variable and IS NOW A
                    if current >= len(tokens) or tokens[current][1] != "Type Literal":
                        raise SyntaxError(f"Expected type literal after 'IS NOW A' at token {current}")
                    type_name = tokens[current][0]
                    current += 1
                    return {
                        "type": "Typecast",
                        "variable": var_name,
                        "targetType": type_name
                    }, current
                else:
                    # Standalone variable
                    var_name = tokens[current][0]
                    current += 1
                    return {
                        "type": "ExpressionStatement",
                        "expression": {"type": "Variable", "name": var_name}
                    }, current
            else:
                var_name = tokens[current][0]
                current += 1
                return {
                    "type": "ExpressionStatement",
                    "expression": {"type": "Variable", "name": var_name}
                }, current

        # Newline
        case "Newline":
            return None, current + 1

        case _:
            raise SyntaxError(f"Unexpected token '{tokens[current][0]}' ('{tokens[current][1]}') at position {current}")


def parse_typecast(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Typecasting Start Operation":
        raise SyntaxError(f"Expected 'MAEK' at token {current}")
    current += 1

    # MAEK A <var> <type>
    if current < len(tokens) and tokens[current][1] == "Typecasting Value Operation":
        current += 1  # skip A
        if current >= len(tokens) or tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'MAEK A' at token {current}")
        var_name = tokens[current][0]
        current += 1
        if current >= len(tokens) or tokens[current][1] != "Type Literal":
            raise SyntaxError(f"Expected type literal at token {current}")
        type_name = tokens[current][0]
        current += 1
        
        print("Parsed <typecast> successfully.")
        return {
            "type": "TypecastExpression",
            "variable": var_name,
            "targetType": type_name
        }, current
    # MAEK <var> A <type>
    else:
        if current >= len(tokens) or tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'MAEK' at token {current}")
        var_name = tokens[current][0]
        current += 1

        if current >= len(tokens) or tokens[current][1] != "Typecasting Value Operation":
            raise SyntaxError(f"Expected 'A' after variable in typecast at token {current}")
        current += 1

        if current >= len(tokens) or tokens[current][1] != "Type Literal":
            raise SyntaxError(f"Expected type literal after 'A' at token {current}")
        type_name = tokens[current][0]
        current += 1

        print("Parsed <typecast> successfully.")
        return {
            "type": "TypecastExpression",
            "variable": var_name,
            "targetType": type_name
        }, current


def parse_varDeclaration(tokens, current):
    current += 1  # skip 'I HAS A'

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable name after 'I HAS A' at token {current}")
    var_name = tokens[current][0]
    current += 1

    init_value = None
    # Optional initialization
    if current < len(tokens) and tokens[current][1] == "Variable Assignment on Declaration":
        current += 1  # skip ITZ
        init_value, current = parse_expression(tokens, current)

    print(f"Declared variable '{var_name}' successfully.")
    return {
        "type": "VariableDeclaration",
        "name": var_name,
        "value": init_value
    }, current


def parse_varInitSection(tokens, current):
    current += 1  # skip WAZZUP

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    # Parse statements inside section
    statements = []
    while current < len(tokens) and tokens[current][1] != "End something":
        stmt, current = parse_statement(tokens, current)
        if stmt:
            statements.append(stmt)

    # Expect BUHBYE
    if current >= len(tokens) or tokens[current][1] != "End something":
        raise SyntaxError(f"Expected 'BUHBYE' to close varinitsection at token {current}")

    current += 1  # skip BUHBYE
    print("Parsed <varinitsection> successfully.")
    return {
        "type": "VariableInitSection",
        "declarations": statements
    }, current


def parse_output(tokens, current):
    current += 1  # skip VISIBLE

    # Parse first expression
    expressions = []
    expr, current = parse_expression(tokens, current)
    expressions.append(expr)

    # Handle multiple outputs
    while current < len(tokens) and tokens[current][1] in ["Parameter Delimiter", "YARN", "NUMBR", "NUMBAR", "TROOF", "Variable"]:
        if tokens[current][1] == "Parameter Delimiter":
            current += 1  # skip AN
        expr, current = parse_expression(tokens, current)
        expressions.append(expr)

    print("Parsed VISIBLE output successfully.")
    return {
        "type": "Output",
        "expressions": expressions
    }, current


def parse_expression(tokens, current):
    if current >= len(tokens):
        raise SyntaxError(f"Unexpected end of tokens in expression")

    token_type = tokens[current][1]

    # Literal or variable
    if token_type in ["YARN", "NUMBR", "NUMBAR", "TROOF"]:
        value = tokens[current][0]
        current += 1
        
        node = {
            "type": "Literal",
            "valueType": token_type,
            "value": value
        }
        
        # Handle concatenation operator (+)
        while current < len(tokens) and tokens[current][1] == "Concatenation Operator":
            current += 1  # skip +
            if current >= len(tokens):
                raise SyntaxError(f"Expected expression after '+' at token {current}")
            right, current = parse_expression(tokens, current)
            node = {
                "type": "BinaryOperation",
                "operator": "CONCATENATE",
                "left": node,
                "right": right
            }
        
        return node, current

    elif token_type == "Variable":
        var_name = tokens[current][0]
        current += 1
        
        node = {"type": "Variable", "name": var_name}
        
        # Handle concatenation operator (+)
        while current < len(tokens) and tokens[current][1] == "Concatenation Operator":
            current += 1  # skip +
            if current >= len(tokens):
                raise SyntaxError(f"Expected expression after '+' at token {current}")
            right, current = parse_expression(tokens, current)
            node = {
                "type": "BinaryOperation",
                "operator": "CONCATENATE",
                "left": node,
                "right": right
            }
        
        return node, current

    # Binary operations
    elif token_type in [
        "Add Operation", "Subtract Operation", "Multiply Operation",
        "Divide Operation", "Modulo Operation", "Equal Operation",
        "Unequal Operation", "Greater Operation", "Lesser Operation",
        "And Operation", "Or Operation", "Xor Operation"
    ]:
        op_map = {
            "Add Operation": "SUM",
            "Subtract Operation": "DIFF",
            "Multiply Operation": "PRODUKT",
            "Divide Operation": "QUOSHUNT",
            "Modulo Operation": "MOD",
            "Equal Operation": "BOTH SAEM",
            "Unequal Operation": "DIFFRINT",
            "Greater Operation": "BIGGR",
            "Lesser Operation": "SMALLR",
            "And Operation": "BOTH",
            "Or Operation": "EITHER",
            "Xor Operation": "WON"
        }
        operator = op_map[token_type]
        current += 1
        
        left, current = parse_expression(tokens, current)

        if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
            raise SyntaxError(f"Expected 'AN' in binary operation at token {current}")
        current += 1

        right, current = parse_expression(tokens, current)

        return {
            "type": "BinaryOperation",
            "operator": operator,
            "left": left,
            "right": right
        }, current

    # Unary operation (NOT)
    elif token_type == "Not Operation":
        current += 1
        operand, current = parse_expression(tokens, current)
        return {
            "type": "UnaryOperation",
            "operator": "NOT",
            "operand": operand
        }, current

    # Multi-operand operations
    elif token_type in ["Multi Or Operation", "Multi And Operation"]:
        operator = "ANY" if token_type == "Multi Or Operation" else "ALL"
        current += 1
        
        operands = []
        expr, current = parse_expression(tokens, current)
        operands.append(expr)
        
        if current >= len(tokens) or tokens[current][1] != "Parameter Delimiter":
            raise SyntaxError(f"Expected 'AN' after first operand in multi-operation at token {current}")
        current += 1
        
        expr, current = parse_expression(tokens, current)
        operands.append(expr)

        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
            current += 1
            expr, current = parse_expression(tokens, current)
            operands.append(expr)

        if current < len(tokens) and tokens[current][1] == "Concatenation Delimiter":
            current += 1

        return {
            "type": "MultiOperation",
            "operator": operator,
            "operands": operands
        }, current

    # String Concatenation (SMOOSH)
    elif token_type == "String Concatenation":
        return parse_concatenate(tokens, current)

    # Typecast expression (MAEK)
    elif token_type == "Typecasting Start Operation":
        return parse_typecast(tokens, current)

    # Function call
    elif token_type == "Function Call":
        return parse_call_function(tokens, current)

    else:
        raise SyntaxError(f"Unexpected expression token '{tokens[current][0]}' ('{token_type}') at position {current}")


def parse_concatenate(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "String Concatenation":
        raise SyntaxError(f"Expected 'SMOOSH' at token {current}")
    current += 1

    expressions = []
    expr, current = parse_expression(tokens, current)
    expressions.append(expr)

    while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
        current += 1
        expr, current = parse_expression(tokens, current)
        expressions.append(expr)

    print("Parsed SMOOSH concatenation successfully.")
    return {
        "type": "Concatenation",
        "expressions": expressions
    }, current


def parse_input(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Input Keyword":
        raise SyntaxError(f"Expected 'GIMMEH' at token {current}")
    current += 1

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected variable after 'GIMMEH' at token {current}")
    var_name = tokens[current][0]
    current += 1

    print("Parsed <userinput> successfully.")
    return {
        "type": "Input",
        "variable": var_name
    }, current


def parse_single_comment(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Single Comment Line":
        raise SyntaxError(f"Expected 'BTW' at token {current}")
    current += 1

    # Skip until newline
    while current < len(tokens) and tokens[current][1] != "Newline":
        current += 1

    if current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    print("Parsed <singlecomment> successfully.")
    return None, current  # Comments don't appear in AST


def parse_multi_comment(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Multi Comment Start":
        raise SyntaxError(f"Expected 'OBTW' at token {current}")
    current += 1

    while current < len(tokens) and tokens[current][1] != "Multi Comment End":
        current += 1

    if current >= len(tokens) or tokens[current][1] != "Multi Comment End":
        raise SyntaxError(f"Expected 'TLDR' to close multi-line comment at token {current}")

    current += 1
    print("Parsed <multicomment> successfully.")
    return None, current  # Comments don't appear in AST


def parse_if_structure(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "If Else Start":
        raise SyntaxError(f"Expected 'O RLY?' at token {current}")
    current += 1

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    if current >= len(tokens) or tokens[current][1] != "If Keyword":
        raise SyntaxError(f"Expected 'YA RLY' after 'O RLY?' at token {current}")
    current += 1

    then_branch, current = parse_codeblock(tokens, current)

    # Collect else-if branches
    elif_branches = []
    while current < len(tokens) and tokens[current][1] == "Else If Keyword":
        current += 1
        condition, current = parse_expression(tokens, current)
        body, current = parse_codeblock(tokens, current)
        elif_branches.append({
            "condition": condition,
            "body": body
        })

    # Optional else
    else_branch = None
    if current < len(tokens) and tokens[current][1] == "Else Keyword":
        current += 1
        else_branch, current = parse_codeblock(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "If Else End":
        raise SyntaxError(f"Expected 'OIC' to end if-structure at token {current}")
    current += 1

    print("Parsed <ifstructure> successfully.")
    return {
        "type": "IfStatement",
        "thenBranch": then_branch,
        "elifBranches": elif_branches,
        "elseBranch": else_branch
    }, current


def parse_switch(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "switch":
        raise SyntaxError(f"Expected 'WTF?' at token {current}")
    current += 1

    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    cases = []
    while current < len(tokens) and tokens[current][1] == "Switch Case Keyword":
        current += 1
        case_value, current = parse_expression(tokens, current)
        case_body, current = parse_codeblock(tokens, current)
        cases.append({
            "value": case_value,
            "body": case_body
        })

    default_case = None
    if current < len(tokens) and tokens[current][1] == "Switch Default Keyword":
        current += 1
        default_case, current = parse_codeblock(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "If Else End":
        raise SyntaxError(f"Expected 'OIC' to end switch structure at token {current}")
    current += 1

    print("Parsed <switchstructure> successfully.")
    return {
        "type": "SwitchStatement",
        "cases": cases,
        "default": default_case
    }, current


def parse_codeblock(tokens, current):
    # Skip newlines
    while current < len(tokens) and tokens[current][1] == "Newline":
        current += 1

    statements = []
    while current < len(tokens) and tokens[current][1] not in [
        "If Else End", "Else If Keyword", "Else Keyword",
        "Switch Case Keyword", "Switch Default Keyword", 
        "End something", "Code End", "Function End", "Loop End Keyword"
    ]:
        stmt, current = parse_statement(tokens, current)
        if stmt:
            statements.append(stmt)

    return statements, current


def parse_loop(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Loop Start Keyword":
        raise SyntaxError(f"Expected 'IM IN YR' at token {current}")
    current += 1

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected loop label after 'IM IN YR' at token {current}")
    loop_label = tokens[current][0]
    current += 1

    operation = None
    loop_var = None
    condition = None

    if current < len(tokens) and tokens[current][1] in ["Increment Operation", "Decrement Operation"]:
        operation = "UPPIN" if tokens[current][1] == "Increment Operation" else "NERFIN"
        current += 1

        if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
            raise SyntaxError(f"Expected 'YR' after operation at token {current}")
        current += 1

        if current >= len(tokens) or tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected variable after 'YR' at token {current}")
        loop_var = tokens[current][0]
        current += 1

        if current < len(tokens) and tokens[current][1] == "Loop Keyword":
            condition_type = tokens[current][0]  # TIL or WILE
            current += 1
            condition, current = parse_expression(tokens, current)
            condition = {
                "type": condition_type,
                "expression": condition
            }

    body, current = parse_codeblock(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "Loop End Keyword":
        raise SyntaxError(f"Expected 'IM OUTTA YR' to end loop at token {current}")
    current += 1

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected loop label after 'IM OUTTA YR' at token {current}")
    current += 1

    print(f"Parsed loop '{loop_label}' successfully.")
    return {
        "type": "Loop",
        "label": loop_label,
        "operation": operation,
        "variable": loop_var,
        "condition": condition,
        "body": body
    }, current


def parse_function_definition(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Function Start":
        raise SyntaxError(f"Expected 'HOW IZ I' at token {current}")
    current += 1

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected function name after 'HOW IZ I' at token {current}")
    func_name = tokens[current][0]
    current += 1

    parameters = []
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":
        current += 1

        if current >= len(tokens) or tokens[current][1] != "Variable":
            raise SyntaxError(f"Expected parameter name after 'YR' at token {current}")
        parameters.append(tokens[current][0])
        current += 1

        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
            current += 1
            
            if current >= len(tokens) or tokens[current][1] != "Loop Variable Assignment":
                raise SyntaxError(f"Expected 'YR' in parameter list at token {current}")
            current += 1

            if current >= len(tokens) or tokens[current][1] != "Variable":
                raise SyntaxError(f"Expected parameter name at token {current}")
            parameters.append(tokens[current][0])
            current += 1

    body, current = parse_codeblock(tokens, current)

    if current >= len(tokens) or tokens[current][1] != "Function End":
        raise SyntaxError(f"Expected 'IF U SAY SO' to end function at token {current}")
    current += 1

    print(f"Parsed function '{func_name}' successfully.")
    return {
        "type": "FunctionDefinition",
        "name": func_name,
        "parameters": parameters,
        "body": body
    }, current


def parse_return_value(tokens, current):
    if current >= len(tokens):
        raise SyntaxError(f"Unexpected end of tokens in return statement")
    
    return_keyword = tokens[current][0]
    current += 1

    return_value = None
    if return_keyword == "FOUND YR":
        return_value, current = parse_expression(tokens, current)

    print("Parsed <return> successfully.")
    return {
        "type": "Return",
        "value": return_value
    }, current


def parse_call_function(tokens, current):
    if current >= len(tokens) or tokens[current][1] != "Function Call":
        raise SyntaxError(f"Expected 'I IZ' at token {current}")
    current += 1

    if current >= len(tokens) or tokens[current][1] != "Variable":
        raise SyntaxError(f"Expected function name after 'I IZ' at token {current}")
    func_name = tokens[current][0]
    current += 1

    arguments = []
    if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":
        current += 1
        arg, current = parse_expression(tokens, current)
        arguments.append(arg)

        while current < len(tokens) and tokens[current][1] == "Parameter Delimiter":
            current += 1

            if current < len(tokens) and tokens[current][1] == "Loop Variable Assignment":
                current += 1

            arg, current = parse_expression(tokens, current)
            arguments.append(arg)

        if current < len(tokens) and tokens[current][1] == "Concatenation Delimiter":
            current += 1

    print(f"Parsed function call '{func_name}' successfully.")
    return {
        "type": "FunctionCall",
        "name": func_name,
        "arguments": arguments
    }, current