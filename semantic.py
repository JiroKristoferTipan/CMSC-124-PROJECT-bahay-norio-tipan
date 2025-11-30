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
            case "Literal":
                symbolTable["IT"] = elements["value"]
            case "Variable":
                symbolTable["IT"] = symbolTable[elements["name"]]
            case "VariableInitSection":
                execute_variableInit(elements["declarations"])
            case "Input":
                execute_input(elements["variable"])
            case "Output":
                execute_output(elements["expressions"])
            case "Assignment":
                execute_assignment(elements)
            case "Typecast":
                symbolTable[elements["variable"]] = execute_typecast(elements)
            case "TypecastExpression":
                symbolTable["IT"] = execute_typecast(elements)
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
            case "FunctionCall":
                symbolTable["IT"] = execute_functionCall(elements)
            case "Break":
                pass
            case _:
                raise TypeError(f"Unknown statement type '{elements['type']}'")

    # see symbols/functions saved
    #print("Final Symbol Table:", symbolTable)
    # print("Final Function Table:", functionTable)

    return True



    
def execute_statement(node):
    match node["type"]:
        case "Literal":
            symbolTable["IT"] = node["value"]
        case "Variable":
            symbolTable["IT"] = symbolTable[node["name"]]
        case "VariableInitSection":
            execute_variableInit(node["declarations"])
        case "Input":
            execute_input(node["variable"])
        case "Output":
            execute_output(node["expressions"])
        case "Assignment":
            execute_assignment(node)
        case "Typecast":
            symbolTable[node["variable"]] = execute_typecast(node)
            return symbolTable[node["variable"]]
        case "TypecastExpression":
            return execute_typecast(node)
        case "ExpressionStatement":
            execute_expressionStatement(node["expression"])
        case "IfStatement":
            return execute_ifStatement(node)                # kinda looks ugly ngl
        case "Loop":
            execute_loop(node)
        case "FunctionDefinition":
            execute_functionDefinition(node)
        case "FunctionCall":
            return execute_functionCall(node)
        case "Return":
            return resolve_value(node["value"])
        case "Break":
            return False

        case _:
            raise TypeError(f"Unknown statement type '{node['type']}'")
        
    return True


def execute_variableInit(ast):
    for elements in ast:
        if elements["name"] not in symbolTable:
            if elements["name"] in ["IT", "NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB", "WIN", "FAIL", "+"
                                    "HAI", "KTHXBYE", "I HAS A", "ITZ", "R", "IS NOW A", "MAEK", "A", "AN", 
                                    "VISIBLE", "GIMMEH", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", 
                                    "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", 
                                    "NOT", "ALL OF", "ANY OF", "MKAY", "BOTH SAEM", "DIFFRINT", "O RLY?", 
                                    "YA RLY", "MEBBE", "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", 
                                    "UPPIN", "NERFIN", "WILE", "TIL", "YR", "OUTTA YR", "HOW IZ I", "I IZ", 
                                    "IF U SAY SO", "GTFO", "FOUND YR", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR"]:
                raise SyntaxError(f"Cannot declare variable with reserved name {elements['name']}")
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
        # should not declare same varname twice
        else:
            raise SyntaxError(f"Variable '{elements['name']}' already declared")
                
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
        elif elements["type"] == "FunctionCall":
            message += str(execute_functionCall(elements))
            
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
    datatype = find_highest_datatype(left_val, right_val)
    numtype = get_num_datatype(left_val, right_val)
    # perform operation
    match operation:
        case "SUM":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return left_val + right_val
        case "DIFF":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return left_val - right_val
        case "PRODUKT":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return left_val * right_val
        case "QUOSHUNT":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            # fix python division always converting to float
            if left_val % right_val == 0:
                return int(left_val / right_val)
            # if dividing actually is a float return this
            return left_val / right_val
        case "MOD":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return left_val % right_val
        case "BIGGR":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return max(left_val, right_val)  # Return the bigger value
        case "SMALLR":
            left_val = typecast(left_val, numtype)
            right_val = typecast(right_val, numtype)
            return min(left_val, right_val)  # Return the smaller value
        case "CONCATENATE":
            return str(left_val)+str(right_val)
        case "BOTH":
            left_val = typecast(left_val, datatype)
            right_val = typecast(right_val, datatype)
            if left_val == right_val == 1:
                return "WIN"
            return "FAIL"
        case "EITHER":
            left_val = typecast(left_val, datatype)
            right_val = typecast(right_val, datatype)
            if left_val or right_val:
                return "WIN"
            return "FAIL"
        case "WON":
            left_val = typecast(left_val, datatype)
            right_val = typecast(right_val, datatype)
            if left_val != right_val:
                return "WIN"
            return "FAIL"
        case "BOTH SAEM":
            left_val = typecast(left_val, datatype)
            right_val = typecast(right_val, datatype)
            if left_val == right_val:
                return "WIN"
            return "FAIL"
        case "DIFFRINT":
            left_val = typecast(left_val, datatype)
            right_val = typecast(right_val, datatype)
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
                raise NameError(f"Variable '{elements['name']}' is not defined")
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
    elif val["type"] == "Variable":
        name = val["name"]
        
        if name not in symbolTable:
            raise NameError(f"Variable '{name}' is not defined")

        symbolTable[var_name] = symbolTable[name]
    elif val["type"] == "TypecastExpression":
        symbolTable[var_name] = execute_typecast(val)
    elif val["type"] == "BinaryOperation":
        symbolTable[var_name] = execute_binaryOperation(val["operator"], val["left"], val["right"])
    elif val["type"] == "FunctionCall":
        symbolTable[var_name] = execute_functionCall(val)
    else:
        raise TypeError(f"Cannot assign value of type '{val['type']}' to variable '{var_name}'")
    
        
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
                    value = float(value)
                elif re.fullmatch(r"[+-]?\d+", value):
                    value = float(int(value))
                else:
                    raise ValueError(f"Cannot convert '{value}' to NUMBAR")
            # already number
            elif isinstance(value, (int, float)):
                value = float(value)
            else:
                raise ValueError(f"Cannot convert type {type(value)} to NUMBAR")


        # NUMBR
        case "NUMBR":
            if isinstance(value, str):
                if re.fullmatch(r"[+-]?\d+", value):
                    value = int(value)
                else:
                    raise ValueError(f"Cannot convert '{value}' to NUMBR")
            elif isinstance(value, float):
                value = int(value)
            elif isinstance(value, int):
                pass  # already NUMBR
            else:
                raise ValueError(f"Cannot convert type {type(value)} to NUMBR")


        # TROOF
        case "TROOF":
            if value == 0 or value == "" or value is None:
                value = "FAIL"
            else:
                value = "WIN"


        # YARN
        case "YARN":
            value = str(value)


        # Invalid target type
        case _:
            raise ValueError(f"Invalid typecast target: {elements['targetType']}")

    return value

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
        symbolTable["IT"] = execute_functionCall(node)
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
            if not execute_statement(stmt):
                return False
        return True

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
                if not execute_statement(stmt):
                    return False
            return True

    # NO WAI
    if node["elseBranch"] is not None:
        for stmt in node["elseBranch"]:
            if not execute_statement(stmt):
                return False
    return True

def execute_switchStatement(cases):
    listCase = cases["cases"]
    found = False

    # search for matching case
    for case in listCase:
        if convertTroof(case["value"]["value"]) == convertTroof(symbolTable["IT"]):
            # found value, run everything under it
            found = True
        
        if found:
            # Execute case body
            for statement in case["body"]:
                result = execute_statement(statement)
                # Check for Break statement
                if statement["type"] == "Break":
                    return  # Exit the entire switch
                if result == False:  # Other break condition
                    return
    
    # Only execute default if no case was found
    if not found and cases["default"] is not None:
        for statement in cases["default"]:
            result = execute_statement(statement)
            if result == False:
                return
        
def execute_loop(node):
    label = node["label"]
    operation = node["operation"]      # UPPIN or NERFIN
    var_name = node["variable"]        # loop variable name
    condition_node = node["condition"] # WILE/TIL node
    body = node["body"]
    stop = False

    # Ensure loop variable exists
    if var_name not in symbolTable:
        raise NameError(f"Variable '{var_name}' is not defined for loop")

    # Loop forever until condition fails
    while not stop:
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
        # if not executeProgram(node):
        #     stop = True
        for stmt in body:
            if not execute_statement(stmt):
                # check for break
                stop = True
                break

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

    # Create local symbol table copy
    oldSymbolTable = dict(symbolTable)

    # Bind parameters
    for p, a in zip(params, args):
        symbolTable[p] = resolve_value(a)

    # Execute body
    for stmt in body:
        returnval = execute_statement(stmt)
        if stmt["type"] == "Return":
            break

    # # If returnval is None, set IT to NOOB, otherwise set to result
    # if returnval is None:
    #     symbolTable["IT"] = "NOOB"
    # else:
    #     symbolTable["IT"] = returnval

    # Restore global variables except IT
    for k in list(symbolTable.keys()):
        if k not in oldSymbolTable and k != "IT":
            del symbolTable[k]

    for k, v in oldSymbolTable.items():
        if k != "IT":
            symbolTable[k] = v

    #return val to check if need to assign to var or IT
    return returnval

def find_highest_datatype(operand1, operand2):
    operand1 = type(operand1).__name__
    operand2 = type(operand2).__name__
    if operand1 == "str" or operand2 == "str":
        return "str"
    elif operand1 == "float" or operand2 == "float":
        return "float"
    elif operand1 == "int" or operand2 == "int":
        return "int"
    elif operand1 == "bool" or operand2 == "bool":
        return "bool"
    return None

def get_num_datatype(op1, op2):
    operand1 = type(op1).__name__
    operand2 = type(op2).__name__
    #if there isnt at least 1 float, u can always get int from arithmetic operations, typecast func will handle null typecasting errors
    if operand1 == "float" or operand2 == "float":
        return "float"
    return "int"
        
# for implicit typecasting
def typecast(operand, datatype):
    if datatype == "bool":
        operandtype = type(operand).__name__
        match operandtype:
            case None:
                return False
            
            case "bool":
                return operand
            
            case "int":
                if operand == 0:
                    return False
                return True
            
            case "float":
                if operand == 0:
                    return False
                return True
            
            case "str":
                if operand in ["", "0"]:
                    return False
                return True

            case _:
                raise ValueError(f"Unexpected data type {operand} when typecasting to bool.")
    elif datatype == "int":
        operandtype = type(operand).__name__
        if operandtype == "str":
            operand = re.sub('"', "", operand )
        if operand == "FAIL" or operand == "WIN":
            operandtype = "bool"
            #print("\n")
        #print(operand)
        match operandtype:
            case None:
                raise ValueError(f"{operand} cannot be typecasted to int.")
            
            case "bool":
                if operand == False:
                    return 0
                return 1
            
            case "int":
                return operand
            
            case "float":
                return int(operand)
            
            case "str":
                try:
                    string = int(operand)
                    return string
                except ValueError:
                    raise SyntaxError(f"Cannot typecast int to string {operand}.")

            case _:
                raise ValueError(f"Unexpected data type {operand} when typecasting to int.")
    elif datatype == "float":
        operandtype = type(operand).__name__
        if operandtype == "str":
            operand = re.sub('"', "", operand )
        if operand == "FAIL" or operand == "WIN":
            operandtype = "bool"
        match operandtype:
            case None:
                raise ValueError(f"{operand} cannot be typecasted to float.")
            
            case "bool":
                if operand == False:
                    return 0
                return 1.0
            
            case "int":
                return float(operand)
            
            case "float":
                return operand
            
            case "str":
                try:
                    string = float(operand)
                    return string
                except ValueError:
                    raise SyntaxError(f"Cannot typecast float to string {operand}.")

            case _:
                raise ValueError(f"Unexpected data type {operand} when typecasting to float.")
    elif datatype == "str":
        operandtype = type(operand).__name__
        match operandtype:
            case None:
                raise ValueError(f"{operand} cannot be typecasted to string.")
            
            case "bool":
                if operand:
                    return "WIN"
                return "FAIL"
            
            case "int":
                return str(operand)
            
            case "float":
                return str(operand)
            
            case "str":
                return operand

            case _:
                raise SyntaxError(f"Unexpected data type {operand} when typecasting to string.")
    else:
        raise ValueError(f"Unknown datatype {datatype} for typecasting.")
        