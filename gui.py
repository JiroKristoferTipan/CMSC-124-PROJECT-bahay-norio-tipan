import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from lexeme import tokenize  
from parser import parse_program 
from semantic import executeProgram, symbolTable
from collections import deque
import builtins
import sys

# --- GLOBALS ---
user_input_queue = deque()
input_active = False
input_buffer = ""

# --- CONSOLE REDIRECT ---
class ConsoleRedirect:
    def __init__(self, console_widget):
        self.console = console_widget

    def write(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text)
        self.console.see("end")  # auto-scroll
        self.console.config(state="disabled")

    def flush(self):
        pass

# --- GUI SYMBOL TABLE UPDATE ---
def update_symbol_table():
    """Refresh the GUI symbol table from semantic.symbolTable"""
    symbols_table.delete(*symbols_table.get_children())
    for ident, val in symbolTable.items():
        symbols_table.insert("", "end", values=(ident, val))
    # Force GUI to update immediately
    root.update_idletasks()

# --- CONSOLE INPUT HANDLING ---
def gui_input(prompt=""):
    """Replaces built-in input() during execution"""
    global input_active, input_buffer
    print(prompt, end="")
    
    # Update symbol table BEFORE waiting for input
    update_symbol_table()
    
    input_active = True
    input_buffer = ""

    while not user_input_queue:
        root.update()  # wait for user input

    input_active = False
    val = user_input_queue.popleft()

    # Update symbol table again after input
    update_symbol_table()
    return val

def on_console_key(event):
    global input_active, input_buffer
    if not input_active:
        return "break"

    if event.keysym == "Return":
        user_input_queue.append(input_buffer)
        input_buffer = ""
        console.config(state="normal")
        console.insert("end", "\n")
        console.config(state="disabled")
        return "break"

    elif event.keysym == "BackSpace":
        if input_buffer:
            input_buffer = input_buffer[:-1]
            console.config(state="normal")
            console.delete("end-2c")
            console.config(state="disabled")
        return "break"

    else:
        input_buffer += event.char
        console.config(state="normal")
        console.insert("end", event.char)
        console.config(state="disabled")
        return "break"

# --- FILE AND EXECUTION ---
def open_file():
    filepath = filedialog.askopenfilename(
        title="Open LOLCode File",
        filetypes=[("LOL files", "*.lol"), ("All files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "r") as f:
        content = f.read()
        editor.delete("1.0", "end")
        editor.insert("1.0", content)
    filename = filepath.split("/")[-1]
    file_label.config(text=filename)
    console.config(state="normal")
    console.delete("1.0", "end")
    console.insert("1.0", "File loaded. Click EXECUTE to run lexer/parser.\n")
    console.config(state="disabled")

def submit_user_input():
    """Submit input from GUI input box"""
    value = input_entry.get()
    if value.strip():
        user_input_queue.append(value)
        input_entry.delete(0, "end")

def execute_code():
    code = editor.get("1.0", "end-1c")

    console.config(state="normal")
    console.delete("1.0", "end")
    console.config(state="disabled")

    original_stdout = sys.stdout
    sys.stdout = ConsoleRedirect(console)
    original_input = builtins.input
    builtins.input = gui_input

    # Tokenize
    try:
        tokens = tokenize(code)
    except Exception as e:
        print(f"LEXER ERROR: {str(e)}")
        sys.stdout = original_stdout
        builtins.input = original_input
        return

    # Update lexeme table (exclude newlines)
    lexemes_table.delete(*lexemes_table.get_children())
    for token, token_type in tokens:
        if token_type != "Newline":
            lexemes_table.insert("", "end", values=(token, token_type))

    # Parse
    try:
        ast = parse_program(tokens)
    except Exception as e:
        print(f"PARSER ERROR: {str(e)}")
        sys.stdout = original_stdout
        builtins.input = original_input
        return

    # Semantics
    try:
        symbolTable.clear()
        executeProgram(ast)
        # Update symbol table immediately after execution completes
        update_symbol_table()
    except Exception as e:
        print(f"SEMANTICS ERROR: {str(e)}")
        # Update symbol table even on error to show any variables that were created
        update_symbol_table()
    finally:
        sys.stdout = original_stdout
        builtins.input = original_input

# --- GUI SETUP ---
root = tk.Tk()
root.title("LOLCODE INTERPRETER")
root.state("zoomed")
root.geometry("1200x600")
root.configure(bg="#f0f0f0")

# File Header
file_frame = tk.Frame(root, bg="#dcdcdc", height=50)
file_frame.place(x=20, y=20, width=550)
file_label = tk.Label(file_frame, text="No file opened", font=("Consolas", 14, "bold"), bg="#dcdcdc")
file_label.pack(side="left", padx=10, pady=10)

folder_button = tk.Button(root, text="📂", font=("Consolas", 20), bg="#dcdcdc", command=open_file)
folder_button.place(x=600, y=20, width=50, height=50)

# Main container
container = tk.Frame(root, bg="#f0f0f0")
container.pack(fill="both", expand=True, padx=20, pady=(80, 20))

editor = scrolledtext.ScrolledText(container, width=70, font=("Consolas", 12), bg="white")
editor.pack(side="left", fill="both", expand=True, padx=(0,10))

sidebar = tk.Frame(container, bg="#f0f0f0")
sidebar.pack(side="right", fill="both")

# Lexeme table
lexemes_frame = tk.Frame(sidebar, bg="#e6e6e6")
lexemes_frame.pack(fill="both", expand=True, padx=(0,10))
lexemes_label = tk.Label(lexemes_frame, text="Lexemes", font=("Consolas", 14))
lexemes_label.pack(pady=5)
lexemes_table = ttk.Treeview(lexemes_frame, columns=("lexeme","classification"), show="headings")
lexemes_table.heading("lexeme", text="Lexeme")
lexemes_table.heading("classification", text="Classification")
lexemes_table.pack(fill="both", expand=True, padx=10, pady=10)

# Symbol table
symbols_frame = tk.Frame(sidebar, bg="#e6e6e6")
symbols_frame.pack(fill="both", expand=True)
symbols_label = tk.Label(symbols_frame, text="Symbol Table", font=("Consolas", 14))
symbols_label.pack(pady=5)
symbols_table = ttk.Treeview(symbols_frame, columns=("identifier","value"), show="headings")
symbols_table.heading("identifier", text="Identifier")
symbols_table.heading("value", text="Value")
symbols_table.pack(fill="both", expand=True, padx=10, pady=10)

# Bottom terminal + input
bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.pack(fill="both", expand=False, padx=20, pady=10)

# Terminal left
terminal_frame = tk.Frame(bottom_frame)
terminal_frame.pack(side="left", fill="both", expand=True)
console_label = tk.Label(terminal_frame, text="Terminal Output:", font=("Consolas", 12, "bold"))
console_label.pack(anchor="w")
console = tk.Text(terminal_frame, bg="#1e1e1e", fg="white", height=10, insertbackground="white")
console.pack(fill="both", expand=True, pady=(5,5))
console.config(state="disabled")
console.bind("<Key>", on_console_key)

# Input right
input_frame = tk.Frame(bottom_frame, bg="#e0e0e0", width=250)
input_frame.pack(side="right", fill="y", padx=10)
input_label = tk.Label(input_frame, text="Input:", font=("Consolas", 12))
input_label.pack(pady=(10,5))
input_entry = tk.Entry(input_frame, font=("Consolas", 12))
input_entry.pack(fill="x", padx=10)
submit_btn = tk.Button(input_frame, text="Submit", font=("Consolas", 12), command=submit_user_input)
submit_btn.pack(pady=10, padx=10, fill="x")

# EXECUTE button
execute_button = tk.Button(
    root,
    text="EXECUTE",
    font=("Consolas", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    command=execute_code
)
execute_button.place(relx=0.85, y=25, width=150, height=50)

root.mainloop()