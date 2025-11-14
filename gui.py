import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk

# main window
root = tk.Tk()
root.title("LOLCODE INTERPRETER")
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

# folder button
def open_file():
    file_path = filedialog.askopenfilename(
        title="Open LOLCode File",
        filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
    )
    if not file_path:
        return
    with open(file_path, "r") as f:
        content = f.read()
    filename = file_path.split("/")[-1]
    file_label.config(text=f"{filename}")
    editor.delete("1.0", "end")
    editor.insert("1.0", content)

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

# text editor + lexemes + symbol table container
container = tk.Frame(root, bg="#f0f0f0")
container.pack(fill="both", expand=True, padx=20, pady=(80, 20))

# text editor
editor = scrolledtext.ScrolledText(container, width=70, font=("Consolas", 12), bg="white", fg="black", insertbackground="black")
editor.pack(side="left", fill="both", expand=True, padx=(0,10))

# lexemes and symbol table 
sidebar = tk.Frame(container, bg="#f0f0f0")
sidebar.pack(side="right", fill="both", expand=False)


# title header for lexeme and symbol table
header_frame = tk.Frame(sidebar, bg="#d3d3d3", height=40)  
header_frame.pack(fill="x", pady=(0, 10))  

header_label = tk.Label(
    header_frame,
    text="LOL CODE Interpreter",
    font=("Consolas", 14, "bold"),
    bg="#d3d3d3",
    fg="black"
)
header_label.pack(expand=True, fill="both")


# lexemes frame
lexemes_frame = tk.Frame(sidebar, bg="#e6e6e6", width=200)
lexemes_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

lexemes_label = tk.Label(lexemes_frame, text="Lexemes", font=("Consolas", 14, "bold"), bg="#e6e6e6")
lexemes_label.pack(padx=10, pady=(10,0))

lexemes_table = ttk.Treeview(lexemes_frame, columns=("lexeme", "classification"), show="headings")
lexemes_table.heading("lexeme", text="Lexeme")
lexemes_table.heading("classification", text="Classification")
lexemes_table.pack(fill="both", expand=True, padx=10, pady=10)

# symbol table frame
symbols_frame = tk.Frame(sidebar, bg="#e6e6e6", width=200)
symbols_frame.pack(side="left", fill="both", expand=True)

symbols_label = tk.Label(symbols_frame, text="Symbol Table", font=("Consolas", 14, "bold"), bg="#e6e6e6")
symbols_label.pack(padx=10, pady=(10,0))

symbols_table = ttk.Treeview(symbols_frame, columns=("identifier", "value"), show="headings")
symbols_table.heading("identifier", text="Identifier")
symbols_table.heading("value", text="Value")
symbols_table.pack(fill="both", expand=True, padx=10, pady=10)

# execute button and console section
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# execute button
execute_button = tk.Button(
    bottom_frame,
    text="Execute",
    font=("Consolas", 12, "bold")
)
execute_button.grid(row=0, column=0, sticky="ew", pady=(0, 10))

# terminal area
console_label = tk.Label(
    bottom_frame,
    text="Terminal Area",
    font=("Consolas", 12, "bold")
)
console_label.grid(row=1, column=0, sticky="w")

console = tk.Text(
    bottom_frame,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    height=10,
    wrap="word"
)
console.grid(row=2, column=0, sticky="ew", pady=(5, 0))

console.config(state="disabled") # console can't be editable

bottom_frame.grid_rowconfigure(2, weight=0)
bottom_frame.grid_columnconfigure(0, weight=1)

# run app
root.mainloop()
