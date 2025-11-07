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
    (r'HAI\b', 'Code Delimiter'),
    (r'KTHXBYE\b', 'Code Delimiter'),
    (r'BTW\b', 'Single Comment Line'),
    (r'OBTW\b', 'Multi Comment Start'),
    (r'TLDR\b', 'Multi Comment End'),
    (r'I HAS A\b', 'Variable Declaration'),
    (r'ITZ\b', 'Variable Assignment'),
    (r'R\b', 'Variable Assignment'),
    (r'AN\b', 'Parameter Delimiter'),
    (r'SUM OF\b', 'Arithmetic Operation'),
    (r'DIFF OF\b', 'Arithmetic Operation'),
    (r'PRODUKT OF\b', 'Arithmetic Operation'),
    (r'QUOSHUNT OF\b', 'Arithmetic Operation'),
    (r'MOD OF\b', 'Arithmetic Operation'),
    (r'BIGGR OF\b', 'Arithmetic Operation'),
    (r'SMALLR OF\b', 'Arithmetic Operation'),
    (r'BOTH OF\b', 'Boolean Operation'),
    (r'EITHER OF\b', 'Boolean Operation'),
    (r'WON OF\b', 'Boolean Operation'),
    (r'NOT\b', 'Boolean Operation'),
    (r'ANY OF\b', 'Boolean Operation'),
    (r'ALL OF\b', 'Boolean Operation'),
    (r'BOTH SAEM\b', 'Comparison Operation'),
    (r'DIFFRINT\b', 'Comparison Operation'),
    (r'SMOOSH\b', 'String Concatenation'),
    (r'MAEK A\b', 'Typecasting Operation'),
    (r'A\b', 'Typecasting Operation'),
    (r'IS NOW A\b', 'Typecasting Operation'),
    (r'VISIBLE\b', 'Output Keyword'),
    (r'GIMMEH\b', 'Input Keyword'),
    (r'O RLY\?', 'if else'), 
    (r'YA RLY\b', 'If-then Keyword'),
    (r'MEBBE\b', 'If-then Keyword'),
    (r'NO WAI\b', 'If-then Keyword'),
    (r'OIC\b', 'Exit Keyword'),
    (r'WTF\?', 'switch'),
    (r'OMG\b', 'Switch-Case Keyword'),
    (r'OMGWTF\b', 'Switch-Case Keyword'),
    (r'IM IN YR\b', 'Loop Keyword'),
    (r'UPPIN\b', 'Loop Operation'),
    (r'NERFIN\b', 'Loop Operation'),
    (r'YR\b', 'Loop Variable Assignment'),
    (r'TIL\b', 'Loop Keyword'),
    (r'WILE\b', 'Loop Keyword'),
    (r'IM OUTTA YR\b', 'Loop Keyword'),
    (r'HOW IZ I\b', 'Function Keyword'),
    (r'IF U SAY SO\b', 'Function Keyword'),
    (r'GTFO\b', 'Return Keyword'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    (r'MKAY\b', 'Concatenation Delimiter'),
    (r'NOOB\b', 'Void Literal'),
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable'),
    
    # SYMBOLS / OPERATORS
    (r'\+', 'Concatenation Operator'),
    (r'-', 'Subtraction Operator'),
    (r'\*', 'Multiplication Operator'),
    (r'/', 'Division Operator'),
    (r'%', 'Modulo Operator'),
    (r'=', 'Assignment or Comparison Operator'),
    (r'\(', 'Left Parenthesis'),
    (r'\)', 'Right Parenthesis'),

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