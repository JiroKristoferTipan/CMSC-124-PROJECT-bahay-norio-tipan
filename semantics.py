import json
import re

symbol_table = {}

def run_program(ast):
    #print(json.dumps(ast["body"][0], indent=2))
    if ast["body"][0]["type"] == "VariableInitSection":
        node = ast["body"][0]
        for dec in node["declarations"]:
            initialize_var(dec)
            #print(symbol_table)
    #print(symbol_table)
    for line in ast["body"]:
        run_line(line, symbol_table)

    return symbol_table

def run_line(ast, vars):
    match ast["type"]:
        case "VariableInitSection":
            return
        case "Output":
            x = ""
            for expr in ast["expressions"]:
                value = typecast_to_yarn(eval_expression(expr, vars))
                x = x + value
            print(x)
        case "Input":
            var = input()
            symbol_table[ast["variable"]] = var
            #print(symbol_table)
        case "Concatenation":
            x = ""
            for expr in ast["expressions"]:
                value = typecast_to_yarn(eval_expression(expr, vars))
                x = x + value
        case "Assignment":
            value = eval_expression(ast["value"], vars)
            symbol_table[ast["variable"]] = value
            #set_variable(ast["variable"], value, vars)

        

def initialize_var(dec):
    #print(json.dumps(dec, indent=2))
    #print(dec["name"])
    symbol_table[dec["name"]] = None
    if ("value" in dec.keys() or "BinaryOperation" in dec.keys()) and dec["value"] is not None:
        temp = dec["value"]
        if temp["type"] == "Literal":
            if temp["value"] in ["WIN", "FAIL"]:
                symbol_table[dec["name"]] = typecast_to_troof(temp["value"])
            elif type(temp["value"]).__name__ == "int":
                symbol_table[dec["name"]] = typecast_to_numbr(temp["value"])
            elif type(temp["value"]).__name__ == "float":
                symbol_table[dec["name"]] = typecast_to_numbar(temp["value"])
        elif temp["type"] == "BinaryOperation":
            #print(json.dumps(temp["left"], indent=2))
            #print(json.dumps(temp["right"], indent=2))
            result = evaluate_binary(temp["operator"], symbol_table, temp)
            if temp["value"] in ["WIN", "FAIL"]:
                symbol_table[dec["name"]] = typecast_to_troof(result)
            elif type(result).__name__ == "int":
                symbol_table[dec["name"]] = typecast_to_numbr(result)
            elif type(result).__name__ == "float":
                symbol_table[dec["name"]] = typecast_to_numbar(result)
            
            symbol_table[dec["name"]] == result

def get_variable(name, vars):
    for var in vars:
        if var["name"] == name:
            return var["value"]
    raise ValueError(f"Variable {name} not yet initialized")

def eval_expression(expr, vars):
    match expr["type"]:

        case "Literal":
            return expr["value"]

        case "Variable":
            return symbol_table[expr["name"]]
            #return get_variable(expr["name"], vars)
        
        case "Concatenation":
            x = ""
            for exp in expr["expressions"]:
                value = typecast_to_yarn(eval_expression(exp, vars))
                x = x + value
            return x
        
        case "UnaryOperation":
            if expr["operator"] == "NOT":
                x = typecast_to_troof(symbol_table[expr["operand"]])
                return not x

        case "BinaryOperation":
            return evaluate_binary(expr["operator"], vars, expr)
        
        case "TypecastExpression":
            var = expr["variable"]
            varType = expr["targetType"]
            value = symbol_table[expr["variable"]]
            match varType:
                case "TROOF":
                    varValue = typecast_to_troof(value)
                    #set_variable(var, varValue, vars)
                    symbol_table[var] = varValue
                case "NUMBR":
                    varValue = typecast_to_numbr(value)
                    #set_variable(var, varValue, vars)
                    symbol_table[var] = varValue
                case "NUMBAR":
                    varValue = typecast_to_numbar(value)
                    #set_variable(var, varValue, vars)
                    symbol_table[var] = varValue
                case "YARN":
                    varValue = typecast_to_yarn(value)
                    #set_variable(var, varValue, vars)
                    symbol_table[var] = varValue
            return varValue
        
        case None:
            return None

        case _:
            raise Exception(f"Unknown expression type {expr}.")
        
def evaluate_binary(operator, vars, expr):
    if expr["left"]["type"] == "Literal":
        left = eval_expression(expr["left"], vars)
    elif expr["left"]["type"] == "Variable":
        left = symbol_table[expr["left"]["name"]]
    elif expr["left"]["type"] == "BinaryOperation":
        left = evaluate_binary(expr["operator"], vars, expr["left"])

    if expr["right"]["type"] == "Literal":
        right = eval_expression(expr["right"], vars)
    elif expr["right"]["type"] == "Variable":
        right = symbol_table[expr["right"]["name"]]
    elif expr["right"]["type"] == "BinaryOperation":
        right = evaluate_binary(expr["operator"], vars, expr["right"])

    datatype = find_highest_datattype(left, right)
    match operator:
        case "SUM":
            return typecast_to_numbr(left) + typecast_to_numbr(right)
        case "DIFF":
            return typecast_to_numbr(left) - typecast_to_numbr(right)
        case "PRODUKT":
            return typecast_to_numbr(left) * typecast_to_numbr(right)
        case "QUOSHUNT":
            return typecast_to_numbr(left) / typecast_to_numbr(right)
        case "MOD":
            return typecast_to_numbr(left) % typecast_to_numbr(right)
        case "BIGGR":
            match datatype:
                case "bool":
                    return max(typecast_to_troof(left), typecast_to_troof(right))
                case "int":
                    return max(typecast_to_numbr(left), typecast_to_numbr(right))
                case "float":
                    return max(typecast_to_numbr(left), typecast_to_numbr(right))
                case "str":
                    return max(typecast_to_numbr(left), typecast_to_numbr(right))
        case "SMALLR":
            match datatype:
                case "bool":
                    return min(typecast_to_troof(left), typecast_to_troof(right))
                case "int":
                    return min(typecast_to_numbr(left), typecast_to_numbr(right))
                case "float":
                    return min(typecast_to_numbr(left), typecast_to_numbr(right))
                case "str":
                    return min(typecast_to_numbr(left), typecast_to_numbr(right))
        case "BOTH SAEM":
            match datatype:
                case "bool":
                    return typecast_to_troof(left) == typecast_to_troof(right)
                case "int":
                    return typecast_to_numbr(left) == typecast_to_numbr(right)
                case "float":
                    return typecast_to_numbar(left) == typecast_to_numbar(right)
                case "str":
                    return typecast_to_yarn(left) == typecast_to_yarn(right)
        case "DIFFRINT":
            match datatype:
                case "bool":
                    return typecast_to_troof(left) != typecast_to_troof(right)
                case "int":
                    return typecast_to_numbr(left) != typecast_to_numbr(right)
                case "float":
                    return typecast_to_numbar(left) != typecast_to_numbar(right)
                case "str":
                    return typecast_to_yarn(left) != typecast_to_yarn(right)
        case "BOTH":
            match datatype:
                case "bool":
                    return typecast_to_troof(left) and typecast_to_troof(right)
                case "int":
                    return typecast_to_numbr(left) and typecast_to_numbr(right)
                case "float":
                    return typecast_to_numbar(left) and typecast_to_numbar(right)
                case "str":
                    return typecast_to_yarn(left) and typecast_to_yarn(right)
        case "EITHER":
            match datatype:
                case "bool":
                    return typecast_to_troof(left) or typecast_to_troof(right)
                case "int":
                    return typecast_to_numbr(left) or typecast_to_numbr(right)
                case "float":
                    return typecast_to_numbar(left) or typecast_to_numbar(right)
                case "str":
                    return typecast_to_yarn(left) or typecast_to_yarn(right)
        case "WON":
            match datatype:
                case "bool":
                    return (not typecast_to_troof(left) and typecast_to_troof(right)) or (typecast_to_troof(left) and not typecast_to_troof(right))
                case "int":
                    return (not typecast_to_numbr(left) and typecast_to_numbr(right)) or (typecast_to_numbr(left) and not typecast_to_numbr(right))
                case "float":
                    return (not typecast_to_numbar(left) and typecast_to_numbar(right)) or (typecast_to_numbar(left) and not typecast_to_numbar(right))
                case "str":
                    return (not typecast_to_yarn(left) and typecast_to_yarn(right)) or (typecast_to_yarn(left) and not typecast_to_yarn(right))
        case "CONCATENATE":
            return typecast_to_yarn(left) + typecast_to_yarn(right)
        case _:
            raise SyntaxError(f"Unexpected binary operation {operator}.")
        
def find_highest_datattype(operand1, operand2):
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
        
def typecast_to_troof(operand):
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
        
def typecast_to_numbr(operand):
    operand = re.sub('"', "", operand )
    operandtype = type(operand).__name__
    if operand == "FAIL" or operand == "WIN":
        operandtype = "bool"
    print(operand)
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
        
def typecast_to_numbar(operand):
    operandtype = type(operand).__name__
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
        
def typecast_to_yarn(operand):
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
            return  str(operand)
        
        case "str":
            return operand

        case _:
            raise SyntaxError(f"Unexpected data type {operand} when typecasting to string.")
        
# def check_type(value):
#     try:
#         bool(value)
#         return bool
#     except ValueError:
        
    