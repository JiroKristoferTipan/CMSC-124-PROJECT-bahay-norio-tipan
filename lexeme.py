import re
import os

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
    (r'HOW IZ I\b', 'Function Keyword'),
    (r'IF U SAY SO\b', 'Function Keyword'),
    (r'GTFO\b', 'Return Keyword'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    (r'MKAY\b', 'Concatenation Delimiter'),
    (r'NOOB\b', 'Void Literal'),
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable'),
    
    # SYMBOLS / OPERATORS
    #(r'\+', 'Concatenation Operator')      #nilagay lang to run file, will be edited in the future
    (r'[^ ]* ', 'INVALID'),                 #INVALID TOKEN, should catch everything not included in tokens until a whitespace or newline
]

class tokenizer:
    def __init__(self, input_code):
        self.input_code = input_code
        self.current = 0
        self.tokens = []

    def match_regex(self, code, index):
        #print(index)
        #go thru all regex patterns and find match
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = re.match(regex, code[index:])
            if match:
                lexeme = match.group(0)
                #print(lexeme)
                #move current index after matched lexeme
                self.current += len(lexeme)
                return lexeme, token_type
        #no matches
        self.current += 1
        return None, None

    def tokenize(self):
        #logic to check if currently inside a comment
        single_comment = False
        multi_comment = False
        code = self.input_code
        while self.current < len(self.input_code):
            #end single comment
            if code[self.current] == '\n':
                single_comment = False
            #ignore white spaces
            if code[self.current].isspace():
                self.current += 1
                continue
            #compare current with all regex
            token = self.match_regex(code, self.current)
            if token is None:
                # No match found, skip the current character
                print("none")
                self.current += 1
                continue
            #start of comment
            elif token[1] == "Single Comment Line" and not (single_comment or multi_comment):
                single_comment = True
                self.tokens.append((token[0], token[1]))
            elif token[1] == "Multi Comment Start" and not (single_comment or multi_comment):
                multi_comment = True
                self.tokens.append((token[0], token[1]))
            #end multi comment
            elif token[1] == "Multi Comment End": 
                multi_comment = False
                self.tokens.append((token[0], token[1]))
            #no comments
            elif not (single_comment or multi_comment):
                self.tokens.append((token[0], token[1]))
        return self.tokens

# Main
def main():
    fileCounter = 1
    filePath = os.path.dirname("project-testcases/")
    with open("output.txt", "w") as f:
        # List the files
        for file in os.listdir(filePath):
            filename = os.fsdecode(file)
            # Read file
            with open(os.path.join(filePath, filename), "r") as file:
                content = file.read()
                tokenizer_instance = tokenizer(content)
                tokens = tokenizer_instance.tokenize()
                print(f'\n--- FILE {fileCounter} ---')
                f.write(f'--- FILE {fileCounter} ---\n')
                print(f'{"Lexeme":20} -> Token Type')
                f.write(f'{"Lexeme":20} -> Token Type\n')
                print("-----------------------------------------")
                f.write("-----------------------------------------\n")
                for token in tokens:
                    print(f'{token[0]:20} -> {token[1]}')
                    f.write(f'{token[0]:20} -> {token[1]}\n')
                f.write("\n")
            fileCounter += 1
            
if __name__ == "__main__":
    main()