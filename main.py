import parser
import lexeme
import os
import json
# import gui

# Main
def main():
    fileCounter = 1
    filePath = os.path.dirname("project-testcases/")
    
    # # List the files
    # for file in os.listdir(filePath):
    #     filename = os.fsdecode(file)
    #     # Read file
    #     with open(os.path.join(filePath, filename), "r") as file:
    #         content = file.read()
    #         #tokenizer_instance = lexeme.tokenizer(content)
    #         tokens = lexeme.tokenize(content)
    #         print(f'\n--- FILE {fileCounter} ---')
    #         parser.parse_program(tokens)
    #         # f.write(f'--- FILE {fileCounter} ---\n')
    #         # print(f'{"Lexeme":20} -> Token Type')
    #         # f.write(f'{"Lexeme":20} -> Token Type\n')
    #         # print("-----------------------------------------")
    #         # f.write("-----------------------------------------\n")
    #         # for token in tokens:
    #         #     print(f'{token[0]:20} -> {token[1]}')
    #         #     f.write(f'{token[0]:20} -> {token[1]}\n')
    #         # f.write("\n")
    #     fileCounter += 1
    
    with open("project-testcases/01_variables.lol", "r") as file:
            content = file.read()
            #tokenizer_instance = lexeme.tokenizer(content)
            tokens = lexeme.tokenize(content)
            print(f'\n--- FILE {fileCounter} ---')
            print(tokens)
            # parser.parse_program(tokens)
            # f.write(f'--- FILE {fileCounter} ---\n')
            # print(f'{"Lexeme":20} -> Token Type')
            # f.write(f'{"Lexeme":20} -> Token Type\n')
            # print("-----------------------------------------")
            # f.write("-----------------------------------------\n")
            # for token in tokens:
            #     print(f'{token[0]:20} -> {token[1]}')
            #     f.write(f'{token[0]:20} -> {token[1]}\n')
            # f.write("\n")
    
            
if __name__ == "__main__":
    main()
    # gui