import re
symbolTable = {}

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
        
    
    print(f"\n{symbolTable}")
    


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
    print(symbolTable)
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
            else: 
                return int(value)

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
            return max(left_val, right_val)
        case "SMALLR":
            left_val = convertTroof(left_val)
            right_val = convertTroof(right_val)
            return min(left_val, right_val)
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
        # case ""
        
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
            
            if elements["type"] == "Variable":
                var_name = elements["name"]
                if var_name not in symbolTable:
                    raise NameError(f"Variable '{var_name}' is not defined")
                if symbolTable[var_name] == 0 or symbolTable[var_name] == "FAIL" or symbolTable[var_name] == "" or symbolTable[var_name] == "NOOB":
                    return "FAIL"
            if elements["type"] == "Literal":
                if elements["value"] == "" or elements["value"] == 0 or elements["value"] == "FAIL":
                    return "FAIL"
        return "WIN"
    elif operator == "ANY":
        for elements in operands:
            if elements["type"] == "Variable":
                var_name = elements["name"]
                if var_name not in symbolTable:
                    raise NameError(f"Variable '{var_name}' is not defined")
                if symbolTable[var_name] != 0 or symbolTable[var_name] == "WIN" or symbolTable[var_name] != "":
                    return "WIN"
            if elements["type"] == "Literal":
                if elements["value"] != "" or elements["value"] != 0 or elements["value"] == "WIN":
                    return "WIN"
        return "FAIL"
