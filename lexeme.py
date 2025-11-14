import re

#regex to follow while tokenizing
token_patterns = [
    # LITERALS
    (r'\"[^\"]*\"', 'YARN'),
    (r'-?[0-9]+\.[0-9]+', 'NUMBAR'),
    (r'-?[0-9]+', 'NUMBR'),
    (r'(WIN|FAIL)', 'TROOF'),
    (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB)', 'Type Literal'),
    
    # KEYWORDS
    (r'HAI\b', 'Code Start'),
    (r'KTHXBYE\b', 'Code End'),
    (r'WAZZUP\b', 'Start something'),
    (r'BUHBYE\b', 'End something'),
    (r'BTW\b', 'Single Comment Line'),
    (r'OBTW\b', 'Multi Comment Start'),
    (r'TLDR\b', 'Multi Comment End'),
    (r'I HAS A\b', 'Variable Declaration'),
    (r'ITZ\b', 'Variable Assignment on Declaration'),
    (r'R\b', 'Variable Assignment'),
    (r'AN\b', 'Parameter Delimiter'),
    (r'SUM OF\b', 'Add Operation'),
    (r'DIFF OF\b', 'Subtract Operation'),
    (r'PRODUKT OF\b', 'Multiply Operation'),
    (r'QUOSHUNT OF\b', 'Divide Operation'),
    (r'MOD OF\b', 'Modulo Operation'),
    (r'BIGGR OF\b', 'Greater Operation'),
    (r'SMALLR OF\b', 'Lesser Operation'),
    (r'BOTH OF\b', 'And Operation'),
    (r'EITHER OF\b', 'Or Operation'),
    (r'WON OF\b', 'Xor Operation'),
    (r'NOT\b', 'Not Operation'),
    (r'ANY OF\b', 'Multi Or Operation'),
    (r'ALL OF\b', 'Multi And Operation'),
    (r'BOTH SAEM\b', 'Equal Operation'),
    (r'DIFFRINT\b', 'Unequal Operation'),
    (r'SMOOSH\b', 'String Concatenation'),
    (r'MAEK\b', 'Typecasting Start Operation'),
    (r'A\b', 'Typecasting Value Operation'),
    (r'IS NOW A\b', 'Typecasting Operation'),
    (r'VISIBLE\b', 'Output Keyword'),
    (r'GIMMEH\b', 'Input Keyword'),
    (r'O RLY\?', 'If Else Start'), 
    (r'YA RLY\b', 'If Keyword'),
    (r'MEBBE\b', 'Else If Keyword'),
    (r'NO WAI\b', 'Else Keyword'),
    (r'OIC\b', 'If Else End'),
    (r'WTF\?', 'switch'),
    (r'OMG\b', 'Switch Case Keyword'),
    (r'OMGWTF\b', 'Switch Default Keyword'),
    (r'IM IN YR\b', 'Loop Start Keyword'),
    (r'UPPIN\b', 'Increment Operation'),
    (r'NERFIN\b', 'Decrement Operation'),
    (r'YR\b', 'Loop Variable Assignment'),
    (r'TIL\b', 'Loop Keyword'),
    (r'WILE\b', 'Loop Keyword'),
    (r'IM OUTTA YR\b', 'Loop End Keyword'),
    (r'HOW IZ I\b', 'Function Start'),
    (r'IF U SAY SO\b', 'Function End'),
    (r'GTFO\b', 'Return Keyword'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    (r'MKAY\b', 'Concatenation Delimiter'),
    (r'NOOB\b', 'Void Literal'),
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable'),
    (r'\n', 'Newline'),
    
    # SYMBOLS / OPERATORS
    #(r'\+', 'Concatenation Operator')      #nilagay lang to run file, will be edited in the future
    (r'[^ \t\n]+', 'INVALID'),                 #INVALID TOKEN, should catch everything not included in tokens until a whitespace or newline
]

#class tokenizer:
    # def __init__(self, input_code):
    #     self.input_code = input_code
    #     self.current = 0
    #     self.tokens = []

def match_regex(code, index):
    #print(index)
    #go thru all regex patterns and find match
    for pattern, token_type in token_patterns:
        regex = re.compile(pattern)
        match = re.match(regex, code[index:])
        if match:
            if match.group(0) == "\n":
                lexeme = "\\n"
            else:
                lexeme = match.group(0)
            #print(lexeme)
            #move current index after matched lexeme
            #index += len(match.group(0))
            print(lexeme, "+", token_type)
            return lexeme, token_type
    #no matches
    #index += 1
    return None, None

def tokenize(input_code):
    tokens = []
    index = 0
    #logic to check if currently inside a comment
    single_comment = False
    multi_comment = False
    while index < len(input_code):
        #end single comment
        if input_code[index] == "\n":
            single_comment = False
        #ignore white spaces
        if input_code[index] == " " or input_code[index] == "\t":
            index += 1
            continue
        #compare current with all regex
        token = match_regex(input_code, index)
        if token is None:
            # No match found, skip the current character
            print("none")
            index += 1
            continue
        #start of comment
        elif token[1] == "Single Comment Line" and not (single_comment or multi_comment):
            single_comment = True
            tokens.append((token[0], token[1]))
        elif token[1] == "Multi Comment Start" and not (single_comment or multi_comment):
            multi_comment = True
            tokens.append((token[0], token[1]))
        #end multi comment
        elif token[1] == "Multi Comment End": 
            multi_comment = False
            tokens.append((token[0], token[1]))
        #no comments
        elif not (single_comment or multi_comment):
            tokens.append((token[0], token[1]))
        if token[0] == "\\n":
            index += 1
        else:
            index += len(token[0])
    return tokens