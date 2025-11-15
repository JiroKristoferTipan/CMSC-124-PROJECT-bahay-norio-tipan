import parser
import lexeme
import os

# Main
def main():
    fileCounter = 1
    filePath = os.path.dirname("project-testcases/")
    with open("output.txt", "w") as f:
        # List the files
        with open("project-testcases/04_smoosh_assign.lol", "r") as file:
            content = file.read()
            #tokenizer_instance = lexeme.tokenizer(content)
            tokens = lexeme.tokenize(content)
            # print(f'{"Lexeme":20} -> Token Type')
            # f.write(f'{"Lexeme":20} -> Token Type\n')
            # print("-----------------------------------------")
            # f.write("-----------------------------------------\n")
            # for token in tokens:
            #     print(f'{token[0]:20} -> {token[1]}')
            #     f.write(f'{token[0]:20} -> {token[1]}\n')
            # f.write("\n")

    parser.parse_program(tokens)
            
if __name__ == "__main__":
    main()