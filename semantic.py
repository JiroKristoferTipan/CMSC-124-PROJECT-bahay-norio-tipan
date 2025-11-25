import re

symbolTable = {}
functionTable = {}

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


def executeProgram(ast):
    body = ast["body"]

    for elements in body:
        match elements["type"]:
            case "VariableInitSection":
                execute_variableInit(elements["declarations"])
            case "Input":
                execute_input(elements["variable"])
            case "Output":
                execute_output(elements["expressions"])
            case "Assignment":
                execute_assignment(elements)
            case "Typecast":
                execute_typecast(elements)
            case "TypecastExpression":
                execute_typecast(elements)
            case "ExpressionStatement":
                execute_expressionStatement(elements["expression"])
            case "IfStatement":
                execute_ifStatement(elements)
            case "SwitchStatement":
                execute_switchStatement(elements)
            case "Loop":
                execute_loop(elements)
            case "FunctionDefinition":
                execute_functionDefinition(elements)


    
def execute_statement(node):
    match node["type"]:
        case "VariableInitSection":
            execute_variableInit(node["declarations"])
        case "Input":
            execute_input(node["variable"])
        case "Output":
            execute_output(node["expressions"])
        case "Assignment":
            execute_assignment(node)
        case "Typecast":
            execute_typecast(node)
        case "TypecastExpression":
            execute_typecast(node)
        case "ExpressionStatement":
            execute_expressionStatement(node["expression"])
        case "IfStatement":
            execute_ifStatement(node)
        case "Loop":
            execute_loop(node)
        case "FunctionDefinition":
            execute_functionDefinition(node)
        case "FunctionCall":
            execute_functionCall(node)
        case "Return":
            raise ReturnException(resolve_value(node["value"]) if node["value"] else None)

        case _:
            raise TypeError(f"Unknown statement type '{node['type']}'")


def execute_variableInit(ast):
    for elements in ast:
        if elements["name"] not in symbolTable:
            if elements["value"] == None:
                symbolTable[elements["name"]] = "NOOB"
            else:
                val = elements["value"]
                
                if "value" in val:
                    symbolTable[elements["name"]] = val["value"]
                else:
                    if val["type"] == "Variable":
                        var_name = val["name"]
                        if var_name not in symbolTable:
                            raise NameError(f"Assigned value '{var_name}' does not exist")
                        symbolTable[elements["name"]] = symbolTable[var_name]
                    else:
                        symbolTable[elements["name"]] = resolve_value(val)
                
def execute_input(ast):
    if ast not in symbolTable:
        raise NameError(f"Variable {ast} is not declared")
    symbolTable[ast] = input()
    
def execute_output(ast):
    # print(symbolTable)
    message = ""
    for elements in ast:
        if elements["type"] == "Literal":
            message += str(elements["value"])
        elif elements["type"] == "BinaryOperation":
            message += str(resolve_value(elements))
        elif elements["type"] == "Variable":
            var_name = elements["name"]
            if var_name not in symbolTable:
                raise NameError(f"Assigned value '{var_name}' does not exist")
            message += str(symbolTable[var_name])
        elif elements["type"] == "Concatenation":
            message += str(execute_concatenation(elements["expressions"]))
        elif elements["type"] == "UnaryOperation":
            message += str(execute_unary(elements["operator"], elements["operand"]))
        elif elements["type"] == "MultiOperation":
            message += str(execute_multiOperation(elements["operator"], elements["operands"]))
            
    print(message)

def resolve_value(node):
    global symbolTable
    # NUMBR or NUMBAR literal
    if node["type"] in ("NUMBR", "NUMBAR"):
        return node["value"]

    if node["type"] == "Literal":
            
        value = node["value"]
        # If already int or float → return as-is
        if isinstance(value, (int, float)):
            return value

        # If still a string, parse it safely
        if isinstance(value, str):
            if bool(re.fullmatch(r"[+-]?\d+\.\d+", value)): 
                return float(value)
            elif value.isdigit(): 
                return int(value)
            else:
                return value
    
    # variable lookup
    if node["type"] == "Variable":
        name = node["name"]
        
        if name not in symbolTable:
            raise NameError(f"Variable '{name}' is not defined")

        value = symbolTable[name]

        # If already int or float → return as-is
        if isinstance(value, (int, float)):
            return value

        # If still a string, parse it safely
        if isinstance(value, str):
            if value == "WIN" or value == "FAIL":
                return value
            
            if bool(re.fullmatch(r"[+-]?\d+\.\d+", value)): 
                return float(value)
            elif value.isdigit(): 
                return int(value)
            else:
                return value

        raise TypeError(f"Invalid value stored for variable '{name}': {value}")

    # Binary operation node (recursive)
    if node["type"] == "BinaryOperation":
        return execute_binaryOperation(
            node["operator"],
            node["left"],
            node["right"],
        )
    if node["type"] == "UnaryOperation":
        return execute_unary(node["operator"], node["operand"])
    raise TypeError(f"Cannot resolve value for node type '{node['type']}'")

def convertTroof(troof):
    if troof == 'FAIL':
        return 0
    elif troof == "WIN":
        return 1
    else:
        return troof

def execute_binaryOperation(operation, left, right):
    global symbolTable
    # resolve both sides to numeric values
    left_val = resolve_value(left)
    right_val = resolve_value(right)
    # print(left_val,right_val, type(left_val),type(right_val))
    # print(symbolTable)
    # perform operation
    match operation:
        case "SUM":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return left_val + right_val
        case "DIFF":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return left_val - right_val
        case "PRODUKT":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return left_val * right_val
        case "QUOSHUNT":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return left_val / right_val
        case "MOD":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return left_val % right_val
        case "BIGGR":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return max(left_val, right_val)  # Return the bigger value
        case "SMALLR":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return min(left_val, right_val)  # Return the smaller value
        case "CONCATENATE":
            return str(left_val)+str(right_val)
        case "BOTH":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            if left_val == right_val == 1:
                return "WIN"
            return "FAIL"
        case "EITHER":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            if left_val or right_val:
                return "WIN"
            return "FAIL"
        case "WON":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            if left_val != right_val:
                return "WIN"
            return "FAIL"
        case "BOTH SAEM":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            if left_val == right_val:
                return "WIN"
            return "FAIL"
        case "DIFFRINT":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            if left_val != right_val:
                return "WIN"
            return "FAIL"
        
        case _:
            raise ValueError(f"Unknown binary operator '{operation}'")

def execute_concatenation(list):
    message = ""
    for elements in list:
        if elements["type"] == "Variable":
            if elements["name"] not in symbolTable:
                raise NameError(f"Variable '{elements["name"]}' is not defined")
            if symbolTable[elements["name"]] == "NOOB":
                raise TypeError(f'can only concatenate str (not "int") to NOOB')
            message += str(symbolTable[elements["name"]])
    return message

def execute_assignment(elements):
    var_name = elements["variable"]
    val = elements["value"]
    if var_name not in symbolTable:
        raise NameError(f"Variable '{var_name}' is not defined")
    
    if val["type"] == "Concatenation":
        symbolTable[var_name] = execute_concatenation(val["expressions"])
    elif val["type"] == "Literal":
        symbolTable[var_name] = val["value"]
    elif val["type"] == "TypecastExpression":
        symbolTable[var_name] = execute_typecast(val)
    
        
def execute_typecast(elements):
    var_name = elements["variable"]

    if var_name not in symbolTable:
        raise NameError(f"Variable '{var_name}' is not defined")
    if symbolTable[var_name] == "NOOB":
        raise ValueError(f"Variable '{var_name}' is uninitialized")

    value = symbolTable[var_name]

    # Convert target type
    match elements["targetType"]:

        # NUMBAR 
        case "NUMBAR":
            # string -> float?
            if isinstance(value, str):
                if re.fullmatch(r"[+-]?\d+\.\d+", value):
                    symbolTable[var_name] = float(value)
                elif re.fullmatch(r"[+-]?\d+", value):
                    symbolTable[var_name] = float(int(value))
                else:
                    raise ValueError(f"Cannot convert '{value}' to NUMBAR")
            # already number
            elif isinstance(value, (int, float)):
                symbolTable[var_name] = float(value)
            else:
                raise ValueError(f"Cannot convert type {type(value)} to NUMBAR")


        # NUMBR
        case "NUMBR":
            if isinstance(value, str):
                if re.fullmatch(r"[+-]?\d+", value):
                    symbolTable[var_name] = int(value)
                else:
                    raise ValueError(f"Cannot convert '{value}' to NUMBR")
            elif isinstance(value, float):
                symbolTable[var_name] = int(value)
            elif isinstance(value, int):
                pass  # already NUMBR
            else:
                raise ValueError(f"Cannot convert type {type(value)} to NUMBR")


        # TROOF
        case "TROOF":
            if value == 0 or value == "" or value is None:
                symbolTable[var_name] = "FAIL"
            else:
                symbolTable[var_name] = "WIN"


        # YARN
        case "YARN":
            symbolTable[var_name] = str(value)


        # Invalid target type
        case _:
            raise ValueError(f"Invalid typecast target: {elements['targetType']}")

    return symbolTable[var_name]

def execute_unary(operator, operand):
    var_name = operand["name"]
    if operator == "NOT":
        if operand["type"] == "Variable":
            if var_name not in symbolTable:
                raise NameError(f"Variable '{var_name}' is not defined")
            if symbolTable[var_name] == 0 or symbolTable[var_name] == "FAIL" or symbolTable[var_name] == "" or symbolTable[var_name] == "NOOB":
                return "WIN"
            else:
                return "FAIL"
        if operand["type"] == "Literal":
            if operand["value"] == "" or operand["value"] == 0 or operand["value"] == "FAIL":
                return "WIN"           
            else:
                return "FAIL"
            
def execute_multiOperation(operator, operands):
    if operator == "ALL":
        for elements in operands:
            # First resolve the value if it's a BinaryOperation or UnaryOperation
            if elements["type"] == "BinaryOperation":
                resolved = execute_binaryOperation(elements["operator"], elements["left"], elements["right"])
                if resolved == 0 or resolved == "FAIL" or resolved == "" or resolved == "NOOB":
                    return "FAIL"
            elif elements["type"] == "UnaryOperation":
                resolved = execute_unary(elements["operator"], elements["operand"])
                if resolved == 0 or resolved == "FAIL" or resolved == "" or resolved == "NOOB":
                    return "FAIL"
            elif elements["type"] == "Variable":
                var_name = elements["name"]
                if var_name not in symbolTable:
                    raise NameError(f"Variable '{var_name}' is not defined")
                if symbolTable[var_name] == 0 or symbolTable[var_name] == "FAIL" or symbolTable[var_name] == "" or symbolTable[var_name] == "NOOB":
                    return "FAIL"
            elif elements["type"] == "Literal":
                if elements["value"] == "" or elements["value"] == 0 or elements["value"] == "FAIL":
                    return "FAIL"
        return "WIN"
    elif operator == "ANY":
        for elements in operands:
            # First resolve the value if it's a BinaryOperation or UnaryOperation
            if elements["type"] == "BinaryOperation":
                resolved = execute_binaryOperation(elements["operator"], elements["left"], elements["right"])
                if resolved != 0 and resolved != "FAIL" and resolved != "" and resolved != "NOOB":
                    return "WIN"
            elif elements["type"] == "UnaryOperation":
                resolved = execute_unary(elements["operator"], elements["operand"])
                if resolved != 0 and resolved != "FAIL" and resolved != "" and resolved != "NOOB":
                    return "WIN"
            elif elements["type"] == "Variable":
                var_name = elements["name"]
                if var_name not in symbolTable:
                    raise NameError(f"Variable '{var_name}' is not defined")
                if symbolTable[var_name] != 0 and symbolTable[var_name] != "FAIL" and symbolTable[var_name] != "" and symbolTable[var_name] != "NOOB":
                    return "WIN"
            elif elements["type"] == "Literal":
                if elements["value"] != "" and elements["value"] != 0 and elements["value"] != "FAIL":
                    return "WIN"
        return "FAIL"

def execute_expressionStatement(node):
    if node["type"] == "FunctionCall":
        execute_functionCall(node)
    else:
        symbolTable["IT"] = resolve_value(node)


def execute_ifStatement(node):
    # O RLY? uses the previous expression result stored in IT
    if "IT" not in symbolTable:
        raise NameError("IT variable not set before O RLY?")
    
    cond_val = symbolTable["IT"]

    # AUTOCAST numeric strings ONLY inside IF
    if isinstance(cond_val, str):
        # integer
        if cond_val.lstrip("+-").isdigit():
            cond_val = int(cond_val)
        # float
        elif re.fullmatch(r"[+-]?\d+\.\d+", cond_val):
            cond_val = float(cond_val)

    # TROOF conversion
    troof_false = ("FAIL", "NOOB", "", 0)
    condition_result = "WIN" if cond_val not in troof_false else "FAIL"

    # YA RLY
    if condition_result == "WIN":
        for stmt in node["thenBranch"]:
            execute_statement(stmt)
        return

    # MEBBE
    for branch in node["elifBranches"]:
        branch_val = resolve_value(branch["condition"])
        symbolTable["IT"] = branch_val

        if isinstance(branch_val, str):
            if branch_val.lstrip("+-").isdigit():
                branch_val = int(branch_val)
            elif re.fullmatch(r"[+-]?\d+\.\d+", branch_val):
                branch_val = float(branch_val)

        branch_result = "WIN" if branch_val not in troof_false else "FAIL"

        if branch_result == "WIN":
            for stmt in branch["body"]:
                execute_statement(stmt)
            return

    # NO WAI
    if node["elseBranch"] is not None:
        for stmt in node["elseBranch"]:
            execute_statement(stmt)

def execute_switchStatement(cases):
    listCase = cases["cases"]
    for case in listCase:
        if convertTroof(case["value"]["value"]) == convertTroof(symbolTable["IT"]):
            executeProgram(case)
            return
        
    for statement in cases["default"]:
        execute_statement(statement)
        
def execute_loop(node):
    label = node["label"]
    operation = node["operation"]      # UPPIN or NERFIN
    var_name = node["variable"]        # loop variable name
    condition_node = node["condition"] # WILE/TIL node
    body = node["body"]

    # Ensure loop variable exists
    if var_name not in symbolTable:
        raise NameError(f"Variable '{var_name}' is not defined for loop")

    # Loop forever until condition fails
    while True:
        # Evaluate loop condition
        cond_type = condition_node["type"]  # WILE or TIL
        cond_expr = condition_node["expression"]
        cond_val = resolve_value(cond_expr)

        # TROOF conversion
        troof_false = ("FAIL", "NOOB", "", 0)
        cond_truth = "WIN" if cond_val not in troof_false else "FAIL"

        # WILE run while condition is WIN
        # TIL run while condition is FAIL
        if cond_type == "WILE":
            if cond_truth == "FAIL":
                break
        elif cond_type == "TIL":
            if cond_truth == "WIN":
                break
        else:
            raise ValueError(f"Unknown loop condition '{cond_type}'")

        # loop body
        for stmt in body:
            execute_statement(stmt)

        # Inc or dec
        if operation == "UPPIN":
            symbolTable[var_name] = resolve_value({"type": "Literal", "value": symbolTable[var_name]}) + 1
        elif operation == "NERFIN":
            symbolTable[var_name] = resolve_value({"type": "Literal", "value": symbolTable[var_name]}) - 1
        else:
            raise ValueError(f"Unknown loop operation '{operation}'")

def execute_functionDefinition(node):
    fname = node["name"]
    params = node["parameters"]
    body = node["body"]
    functionTable[fname] = {
        "params": params,
        "body": body
    }

     
def execute_functionCall(node):
    fname = node["name"]
    args = node["arguments"]

    if fname not in functionTable:
        raise NameError(f"Function '{fname}' not defined")

    func = functionTable[fname]
    params = func["params"]
    body = func["body"]

    if len(params) != len(args):
        raise TypeError(f"Function '{fname}' expects {len(params)} args but got {len(args)}")

    # Create local stack
    oldSymbolTable = dict(symbolTable)

    # Bind parameters
    for p, a in zip(params, args):
        symbolTable[p] = resolve_value(a)

    # Execute body
    try:
        for stmt in body:
            execute_statement(stmt)

        # No explicit return then IT = NOOB
        symbolTable["IT"] = "NOOB"

    except ReturnException as ret:
        # Set IT to the return value, or NOOB if no value
        symbolTable["IT"] = ret.value if ret.value is not None else "NOOB"

    # Restore global variables except IT
    for k in list(symbolTable.keys()):
        if k not in oldSymbolTable and k != "IT":
            del symbolTable[k]

    for k, v in oldSymbolTable.items():
        if k != "IT":
            symbolTable[k] = v
