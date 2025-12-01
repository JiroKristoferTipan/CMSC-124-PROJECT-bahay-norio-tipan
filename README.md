# CMSC-124-PROJECT-bahay-norio-tipan

## Files

1. main.py
- main file to run the program. Properly executes all files in the right order and without conflicts.

2. lexeme.py
- tokenizes input string into an array of tuples, containing the type of token currently detected(eg. and operator) and the actual value found(eg. SUM OF).

3. parser.py
- splits array of tokens by line of code then catches proper syntax per line, returns a json formatted parse tree that properly sorts each token of the especified code for the semantics to read.

4. semantics.py
- reads the json format to read and properly implements the specified instructions, based on the type of instruction(initialization, conditionals, functions, etc.), operator(add, multiply, or, etc.) or variable(initialized variable, literal). A symbol table and function table is also made to be able to properly save veriables and functions.

5. gui.py
- Implements the gui for the program, allowing you to choose your desired lolcode file from your file system then shows the determined lexemes and symbol table upon execution. An input section and terminal for output is also displayed at the bottom.

# Authors
- Bahay, Kent Benedick
- Norio, Yshihero
- Tipan, Jiro Kristofer