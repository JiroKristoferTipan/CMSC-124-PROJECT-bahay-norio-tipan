import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from lexeme import tokenize  
from parser import parse_program  

# window setup
root = tk.Tk()
root.title("LOLCODE INTERPRETER")
root.state("zoomed")
root.geometry("1200x600")
root.configure(bg="#f0f0f0")

# file explorer frame
file_frame = tk.Frame(root, bg="#dcdcdc", height=50)
file_frame.place(x=20, y=20, width=550)

file_label = tk.Label(
    file_frame,
    text="No file opened",
    font=("Consolas", 14, "bold"),
    bg="#dcdcdc",
    fg="black"
)
file_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)

# symbol table extractor
def extract_symbols_from_ast(ast_node):
    symbols = []
    if not isinstance(ast_node, dict):
        return symbols

    if ast_node.get("type") == "VariableInitSection":
        for decl in ast_node.get("declarations", []):
            name = decl["name"]
            value_node = decl.get("value")
            if value_node and value_node["type"] == "Literal":
                val = value_node.get("value", "UNKNOWN")
                symbols.append((name, val))
            elif value_node is None:
                # variable declared but no value assigned
                symbols.append((name, "NO VALUE"))
            # skip other types like BinaryOperation

    # recursively check body nodes
    for child in ast_node.get("body", []):
        symbols.extend(extract_symbols_from_ast(child))

    return symbols


# open file function
def open_file():
    filepath = filedialog.askopenfilename(
        title="Open LOLCode File",
        filetypes=[("LOL files", "*.lol"), ("All files", "*.*")]
    )
    if not filepath:
        return

    # read file content
    with open(filepath, "r") as f:
        content = f.read()
        editor.delete("1.0", "end")
        editor.insert("1.0", content)

    # Update filename label
    filename = filepath.split("/")[-1]
    file_label.config(text=filename)

    # run lexer
    try:
        tokens = tokenize(content)
    except Exception as e:
        tokens = []
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", f"LEXER ERROR: {str(e)}\n")
        console.config(state="disabled")

    # update lexeme table
    lexemes_table.delete(*lexemes_table.get_children())
    for token, token_type in tokens:
        lexemes_table.insert("", "end", values=(token, token_type))

    # run parser and update symbol table
    symbols_table.delete(*symbols_table.get_children())
    try:
        ast = parse_program(tokens)
        symbols = extract_symbols_from_ast(ast)
        for ident, val in symbols:
            symbols_table.insert("", "end", values=(ident, val))
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", "Parsing successful.\n")
        console.config(state="disabled")
    except Exception as e:
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", f"PARSER ERROR: {str(e)}\n")
        console.config(state="disabled")


# folder button
folder_button = tk.Button(
    root,
    text="📂",
    font=("Consolas", 20),
    bg="#dcdcdc",
    fg="black",
    activebackground="#bfbfbf",
    command=open_file
)
folder_button.place(x=600, y=20, width=50, height=50)


# execute code function
def execute_code():
    code = editor.get("1.0", "end-1c")

    # Run lexer
    try:
        tokens = tokenize(code)
    except Exception as e:
        tokens = []
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", f"LEXER ERROR: {str(e)}\n")
        console.config(state="disabled")

    # Update lexeme table
    lexemes_table.delete(*lexemes_table.get_children())
    for token, token_type in tokens:
        lexemes_table.insert("", "end", values=(token, token_type))

    # Run parser
    symbols_table.delete(*symbols_table.get_children())
    try:
        ast = parse_program(tokens)
        symbols = extract_symbols_from_ast(ast)
        for ident, val in symbols:
            symbols_table.insert("", "end", values=(ident, val))
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", "Parsing successful.\n")
        console.config(state="disabled")
    except Exception as e:
        console.config(state="normal")
        console.delete("1.0", "end")
        console.insert("1.0", f"PARSER ERROR: {str(e)}\n")
        console.config(state="disabled")

# text editor and tables container
container = tk.Frame(root, bg="#f0f0f0")
container.pack(fill="both", expand=True, padx=20, pady=(80, 20))

editor = scrolledtext.ScrolledText(
    container,
    width=70,
    font=("Consolas", 12),
    bg="white",
    fg="black",
    insertbackground="black"
)
editor.pack(side="left", fill="both", expand=True, padx=(0,10))

sidebar = tk.Frame(container, bg="#f0f0f0")
sidebar.pack(side="right", fill="both", expand=False)

header_frame = tk.Frame(sidebar, bg="#d3d3d3", height=40)
header_frame.pack(fill="x", pady=(0,10))
header_label = tk.Label(
    header_frame,
    text="LOL CODE Interpreter",
    font=("Consolas", 14, "bold"),
    bg="#d3d3d3",
    fg="black"
)
header_label.pack(expand=True, fill="both")

# lexeme table
lexemes_frame = tk.Frame(sidebar, bg="#e6e6e6", width=200)
lexemes_frame.pack(side="left", fill="both", expand=True, padx=(0,10))
lexemes_label = tk.Label(lexemes_frame, text="Lexemes", font=("Consolas", 14, "bold"), bg="#e6e6e6")
lexemes_label.pack(padx=10, pady=(10,0))
lexemes_table = ttk.Treeview(lexemes_frame, columns=("lexeme","classification"), show="headings")
lexemes_table.heading("lexeme", text="Lexeme")
lexemes_table.heading("classification", text="Classification")
lexemes_table.pack(fill="both", expand=True, padx=10, pady=10)

# symbol table
symbols_frame = tk.Frame(sidebar, bg="#e6e6e6", width=200)
symbols_frame.pack(side="left", fill="both", expand=True)
symbols_label = tk.Label(symbols_frame, text="Symbol Table", font=("Consolas", 14, "bold"), bg="#e6e6e6")
symbols_label.pack(padx=10, pady=(10,0))
symbols_table = ttk.Treeview(symbols_frame, columns=("identifier","value"), show="headings")
symbols_table.heading("identifier", text="Identifier")
symbols_table.heading("value", text="Value")
symbols_table.pack(fill="both", expand=True, padx=10, pady=10)

# execute button and console
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

execute_button = tk.Button(
    bottom_frame,
    text="EXECUTE",
    font=("Consolas", 12, "bold"),
    command=execute_code
)
execute_button.grid(row=0, column=0, sticky="ew", pady=(0,10))

console_label = tk.Label(bottom_frame, text="Terminal Area", font=("Consolas",12,"bold"))
console_label.grid(row=1, column=0, sticky="w")

console = tk.Text(bottom_frame, bg="#1e1e1e", fg="white", insertbackground="white", height=10, wrap="word")
console.grid(row=2, column=0, sticky="ew", pady=(5,0))
console.config(state="disabled")

bottom_frame.grid_rowconfigure(2, weight=0)
bottom_frame.grid_columnconfigure(0, weight=1)

# run app
root.mainloop()
