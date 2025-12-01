import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from lexeme import tokenize  
from parser import parse_program 
from semantic import executeProgram, symbolTable
from collections import deque
import builtins
import sys

# GLOBALS 
user_input_queue = deque()
input_active = False
input_buffer = ""

# CONSOLE REDIRECT 
class ConsoleRedirect:
    def __init__(self, console_widget):
        self.console = console_widget

    def write(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.config(state="disabled")

    def flush(self):
        pass

# GUI SYMBOL TABLE UPDATE
def update_symbol_table():
    symbols_table.delete(*symbols_table.get_children())
    for ident, val in symbolTable.items():
        symbols_table.insert("", "end", values=(ident, val))
    root.update_idletasks()

# CONSOLE INPUT HANDLING
def gui_input(prompt=""):
    global input_active, input_buffer
    print(prompt, end="")
    update_symbol_table()
    input_active = True
    input_buffer = ""
    while not user_input_queue:
        root.update()
    input_active = False
    val = user_input_queue.popleft()
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

# FILE AND EXECUTION 
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

    try:
        tokens = tokenize(code)
    except Exception as e:
        print(f"LEXER ERROR: {str(e)}")
        sys.stdout = original_stdout
        builtins.input = original_input
        return

    lexemes_table.delete(*lexemes_table.get_children())
    for token, token_type in tokens:
        if token_type != "Newline":
            lexemes_table.insert("", "end", values=(token, token_type))

    try:
        ast = parse_program(tokens)
    except Exception as e:
        print(f"PARSER ERROR: {str(e)}")
        sys.stdout = original_stdout
        builtins.input = original_input
        return

    try:
        symbolTable.clear()
        executeProgram(ast)
        update_symbol_table()
    except Exception as e:
        print(f"SEMANTICS ERROR: {str(e)}")
        update_symbol_table()
    finally:
        sys.stdout = original_stdout
        builtins.input = original_input

# --- GUI SETUP ---
root = tk.Tk()
root.title("LOLCODE INTERPRETER")
root.state("zoomed")
root.geometry("1200x750")
root.configure(bg="#1a1a1a")

style = ttk.Style()
style.theme_use("clam")

style.configure("Dark.Treeview",
    background="#2b2b2b",
    foreground="#e0e0e0",
    fieldbackground="#2b2b2b",
    borderwidth=0,
    rowheight=25
)
style.configure("Dark.Treeview.Heading",
    background="#1e1e1e",
    foreground="#ffffff",
    borderwidth=0,
    relief="flat",
    font=("Consolas", 10, "bold")
)
style.map("Dark.Treeview",
    background=[("selected", "#0d7377")],
    foreground=[("selected", "#ffffff")]
)
style.map("Dark.Treeview.Heading",
    background=[("active", "#2d2d2d")]
)

top_bar = tk.Frame(root, bg="#252525", height=60)
top_bar.pack(fill="x", side="top")
top_bar.pack_propagate(False)

file_section = tk.Frame(top_bar, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1)
file_section.pack(side="left", padx=15, pady=10, fill="y")

folder_button = tk.Button(
    file_section, text="📁", font=("Segoe UI Emoji", 10),
    bg="#3d3d3d", fg="#ffffff", bd=0, relief="flat",
    activebackground="#4d4d4d", cursor="hand2",
    command=open_file, padx=12, pady=8
)
folder_button.pack(side="left", padx=8, pady=5)

file_label = tk.Label(
    file_section, text="No file opened",
    font=("Segoe UI", 11), bg="#2d2d2d", fg="#b0b0b0"
)
file_label.pack(side="left", padx=(5, 12), pady=5)

execute_button = tk.Button(
    top_bar, text="▶ EXECUTE",
    font=("Segoe UI", 11, "bold"),
    bg="#2ecc71", fg="#ffffff",
    activebackground="#27ae60", activeforeground="#ffffff",
    bd=0, relief="flat", cursor="hand2",
    command=execute_code, padx=25, pady=12
)
execute_button.pack(side="right", padx=15, pady=10)

def on_enter_execute(e):
    execute_button.config(bg="#27ae60")
def on_leave_execute(e):
    execute_button.config(bg="#2ecc71")
execute_button.bind("<Enter>", on_enter_execute)
execute_button.bind("<Leave>", on_leave_execute)

def on_enter_folder(e):
    folder_button.config(bg="#4d4d4d")
def on_leave_folder(e):
    folder_button.config(bg="#3d3d3d")
folder_button.bind("<Enter>", on_enter_folder)
folder_button.bind("<Leave>", on_leave_folder)

container = tk.Frame(root, bg="#1a1a1a")
container.pack(fill="both", expand=True, padx=15, pady=(10, 5))

editor_container = tk.Frame(container, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1)
editor_container.pack(side="left", fill="both", expand=True, padx=(0, 8))

editor_header = tk.Label(
    editor_container, text="CODE EDITOR",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e1e", fg="#ffffff",
    anchor="w", padx=10, pady=8
)
editor_header.pack(fill="x")

editor = scrolledtext.ScrolledText(
    editor_container, font=("Consolas", 11), bg="#1e1e1e", fg="#d4d4d4",
    insertbackground="#ffffff", selectbackground="#264f78",
    bd=0, relief="flat", padx=10, pady=5
)
editor.pack(fill="both", expand=True, padx=3, pady=(0, 3))

tables_container = tk.Frame(container, bg="#1a1a1a")
tables_container.pack(side="right", fill="both", expand=True)

lexemes_container = tk.Frame(tables_container, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1)
lexemes_container.pack(fill="both", expand=True, pady=(0, 8))

lexemes_header = tk.Label(
    lexemes_container, text="LEXEMES",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e1e", fg="#ffffff",
    anchor="w", padx=10, pady=8
)
lexemes_header.pack(fill="x")

lexemes_table = ttk.Treeview(
    lexemes_container, columns=("lexeme", "classification"),
    show="headings", style="Dark.Treeview", height=8
)
lexemes_table.heading("lexeme", text="Lexeme")
lexemes_table.heading("classification", text="Classification")
lexemes_table.column("lexeme", width=140, anchor="w")
lexemes_table.column("classification", width=140, anchor="w")
lexemes_table.pack(fill="both", expand=True, padx=3, pady=(0, 3))

lexemes_table.tag_configure("oddrow", background="#2b2b2b")
lexemes_table.tag_configure("evenrow", background="#323232")

symbols_container = tk.Frame(tables_container, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1)
symbols_container.pack(fill="both", expand=True)

symbols_header = tk.Label(
    symbols_container, text="SYMBOL TABLE",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e1e", fg="#ffffff",
    anchor="w", padx=10, pady=8
)
symbols_header.pack(fill="x")

symbols_table = ttk.Treeview(
    symbols_container, columns=("identifier", "value"),
    show="headings", style="Dark.Treeview", height=8
)
symbols_table.heading("identifier", text="Identifier")
symbols_table.heading("value", text="Value")
symbols_table.column("identifier", width=140, anchor="w")
symbols_table.column("value", width=140, anchor="w")
symbols_table.pack(fill="both", expand=True, padx=3, pady=(0, 3))

symbols_table.tag_configure("oddrow", background="#2b2b2b")
symbols_table.tag_configure("evenrow", background="#323232")

bottom_frame = tk.Frame(root, bg="#1a1a1a")
bottom_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

terminal_container = tk.Frame(bottom_frame, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1)
terminal_container.pack(side="left", fill="both", expand=True, padx=(0, 8))

terminal_header = tk.Label(
    terminal_container, text="TERMINAL",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e1e", fg="#ffffff",
    anchor="w", padx=10, pady=8
)
terminal_header.pack(fill="x")

console = tk.Text(
    terminal_container, bg="#0a0a0a", fg="#00ff41",
    font=("Consolas", 10), insertbackground="#00ff41",
    selectbackground="#264f78", bd=0, relief="flat",
    padx=10, pady=5
)
console.pack(fill="both", expand=True, padx=3, pady=(0, 3))
console.config(state="disabled")
console.bind("<Key>", on_console_key)

input_container = tk.Frame(bottom_frame, bg="#2d2d2d", highlightbackground="#404040", highlightthickness=1, width=300)
input_container.pack(side="right", fill="y")
input_container.pack_propagate(False)

input_header = tk.Label(
    input_container, text="INPUT",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e1e", fg="#ffffff",
    anchor="w", padx=10, pady=8
)
input_header.pack(fill="x")

input_inner = tk.Frame(input_container, bg="#2d2d2d")
input_inner.pack(fill="both", expand=True, padx=10, pady=10)

input_entry = tk.Entry(
    input_inner, font=("Consolas", 11),
    bg="#1e1e1e", fg="#d4d4d4",
    insertbackground="#ffffff", selectbackground="#264f78",
    bd=1, relief="solid", highlightthickness=0
)
input_entry.pack(fill="x", ipady=8, pady=(0, 10))

submit_btn = tk.Button(
    input_inner, text="SUBMIT",
    font=("Segoe UI", 10, "bold"),
    bg="#3498db", fg="#ffffff",
    activebackground="#2980b9", activeforeground="#ffffff",
    bd=0, relief="flat", cursor="hand2",
    command=submit_user_input, pady=10
)
submit_btn.pack(fill="x")

def on_enter_submit(e):
    submit_btn.config(bg="#2980b9")
def on_leave_submit(e):
    submit_btn.config(bg="#3498db")
submit_btn.bind("<Enter>", on_enter_submit)
submit_btn.bind("<Leave>", on_leave_submit)

status_bar = tk.Frame(root, bg="#252525", height=25)
status_bar.pack(fill="x", side="bottom")

status_label = tk.Label(
    status_bar, text="Ready",
    font=("Segoe UI", 9), bg="#252525", fg="#b0b0b0",
    anchor="w", padx=15
)
status_label.pack(side="left", fill="x")

root.mainloop()