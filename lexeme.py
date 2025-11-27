import re

# Regex patterns for tokenizing (ORDER MATTERS!)
token_patterns = [
    # LITERALS (must come before some keywords)
    (r'\"[^\"]*\"', 'YARN'),
    (r'-?[0-9]+\.[0-9]+', 'NUMBAR'),
    (r'-?[0-9]+', 'NUMBR'),
    (r'(WIN|FAIL)', 'TROOF'),
    (r'NOOB', 'NOOB'),
    
    # MULTI-WORD KEYWORDS (must come before single-word versions)
    (r'I HAS A\b', 'Variable Declaration'),
    (r'ITZ\b', 'Variable Assignment on Declaration'),
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
    (r'ANY OF\b', 'Multi Or Operation'),
    (r'ALL OF\b', 'Multi And Operation'),
    (r'BOTH SAEM\b', 'Equal Operation'),
    (r'IS NOW A\b', 'Typecasting Operation'),
    (r'O RLY\?', 'If Else Start'), 
    (r'YA RLY\b', 'If Keyword'),
    (r'NO WAI\b', 'Else Keyword'),
    (r'WTF\?', 'switch'),
    (r'IM IN YR\b', 'Loop Start Keyword'),
    (r'IM OUTTA YR\b', 'Loop End Keyword'),
    (r'HOW IZ I\b', 'Function Start'),
    (r'IF U SAY SO\b', 'Function End'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    
    # SINGLE-WORD KEYWORDS
    (r'HAI\b', 'Code Start'),
    (r'KTHXBYE\b', 'Code End'),
    (r'WAZZUP\b', 'Start something'),
    (r'BUHBYE\b', 'End something'),
    (r'BTW\b', 'Single Comment Line'),
    (r'OBTW\b', 'Multi Comment Start'),
    (r'TLDR\b', 'Multi Comment End'),
    (r'R\b', 'Variable Assignment'),
    (r'AN\b', 'Parameter Delimiter'),  # MUST come before 'A'
    (r'NOT\b', 'Not Operation'),
    (r'DIFFRINT\b', 'Unequal Operation'),
    (r'SMOOSH\b', 'String Concatenation'),
    (r'MAEK\b', 'Typecasting Start Operation'),
    (r'A\b', 'Typecasting Value Operation'),  # AFTER 'AN'
    (r'VISIBLE\b', 'Output Keyword'),
    (r'GIMMEH\b', 'Input Keyword'),
    (r'MEBBE\b', 'Else If Keyword'),
    (r'OIC\b', 'If Else End'),
    (r'OMG\b', 'Switch Case Keyword'),
    (r'OMGWTF\b', 'Switch Default Keyword'),
    (r'UPPIN\b', 'Increment Operation'),
    (r'NERFIN\b', 'Decrement Operation'),
    (r'YR\b', 'Loop Variable Assignment'),
    (r'TIL\b', 'Loop Keyword'),
    (r'WILE\b', 'Loop Keyword'),
    (r'GTFO\b', 'Break Keyword'),
    (r'MKAY\b', 'Concatenation Delimiter'),
    
    # TYPE LITERALS
    (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB)\b', 'Type Literal'),
    
    # VARIABLES (must come after all keywords)
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable'),
    
    # NEWLINE
    (r'\n', 'Newline'),
    
    # OPERATORS
    (r'\+', 'Concatenation Operator'),
    
    # INVALID (MUST BE LAST)
    (r'[^ \t\n]', 'INVALID'),
]

def match_regex(code, index):
    """Match token patterns against code starting at index."""
    for pattern, token_type in token_patterns:
        regex = re.compile(pattern)
        match = re.match(regex, code[index:])
        if match:
            lexeme = match.group(0)
            return lexeme, token_type
    return None, None

def tokenize(input_code):
    """Tokenize LOLCODE input."""
    tokens = []
    index = 0
    single_comment = False
    multi_comment = False
    
    while index < len(input_code):
        # Handle newline (ends single-line comments)
        if input_code[index] == "\n":
            if single_comment:
                single_comment = False
            if not multi_comment:  # Only add newline token if not in multi-comment
                tokens.append(("\n", "Newline"))
            index += 1
            continue
        
        # Skip whitespace
        if input_code[index] in (' ', '\t'):
            index += 1
            continue
        
        # If inside a comment, skip characters
        if single_comment or multi_comment:
            # Still need to check for comment end
            token = match_regex(input_code, index)
            if token[0] and token[1] == "Multi Comment End":
                multi_comment = False
                tokens.append(token)
                index += len(token[0])
            else:
                index += 1
            continue
        
        # Match token
        lexeme, token_type = match_regex(input_code, index)
        
        if lexeme is None:
            # This shouldn't happen with INVALID pattern, but just in case
            print(f"Warning: Unrecognized character at position {index}: '{input_code[index]}'")
            index += 1
            continue
        
        # Handle comment starts
        if token_type == "Single Comment Line":
            single_comment = True
            tokens.append((lexeme, token_type))
        elif token_type == "Multi Comment Start":
            multi_comment = True
            tokens.append((lexeme, token_type))
        else:
            # Add token (convert newline for display)
            if lexeme == "\n":
                tokens.append(("\n", token_type))
            else:
                try:
                    tokens.append((int(lexeme), token_type))
                except ValueError:
                    try:
                        tokens.append((float(lexeme), token_type))
                    except ValueError:
                        tokens.append((re.sub('"', "", lexeme), token_type))
        
        # Advance index
        index += len(lexeme)
    
    return tokens