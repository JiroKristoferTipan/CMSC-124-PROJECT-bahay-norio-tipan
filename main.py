import parser
import parser2
import lexeme
import os

# Main
def main():
    fileCounter = 1
    filePath = os.path.dirname("project-testcases/")
    with open("project-testcases/jirotest.lol", "r") as file:
        content = file.read()
        #tokenizer_instance = lexeme.tokenizer(content)
        tokens = lexeme.tokenize(content)
    #     #print(f'\n--- FILE {fileCounter} ---')
    #     f.write(f'--- FILE {fileCounter} ---\n')
    #     #print(f'{"Lexeme":20} -> Token Type')
    #     f.write(f'{"Lexeme":20} -> Token Type\n')
    #     #print("-----------------------------------------")
    #     f.write("-----------------------------------------\n")
    #     for token in tokens:
    #         #print(f'{token[0]:20} -> {token[1]}')
    #         f.write(f'{token[0]:20} -> {token[1]}\n')
    #     f.write("\n")
    # print(f'\n--- FILE {fileCounter} ---')
    # fileCounter += 1
    #print(tokens)
    parser2.parse_program(tokens)
    #with open("output.txt", "w") as f:
        # # List the files
        # for file in os.listdir(filePath):
        #     filename = os.fsdecode(file)
        #     # Read file
            
        #     with open(os.path.join(filePath, filename), "r") as file:
        #         content = file.read()
        #         #tokenizer_instance = lexeme.tokenizer(content)
        #         tokens = lexeme.tokenize(content)
        #         #print(f'\n--- FILE {fileCounter} ---')
        #         f.write(f'--- FILE {fileCounter} ---\n')
        #         #print(f'{"Lexeme":20} -> Token Type')
        #         f.write(f'{"Lexeme":20} -> Token Type\n')
        #         #print("-----------------------------------------")
        #         f.write("-----------------------------------------\n")
        #         for token in tokens:
        #             #print(f'{token[0]:20} -> {token[1]}')
        #             f.write(f'{token[0]:20} -> {token[1]}\n')
        #         f.write("\n")
        #     print(f'\n--- FILE {fileCounter} ---')
        #     fileCounter += 1
        #     #print(tokens)
        #     parser.parse_program(tokens)
    
    parser.parse_program(tokens)
            
# if __name__ == "__main__":
#     main()
#     run_gui()
