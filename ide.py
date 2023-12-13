import os
from tkinter import Tk, Text, Scrollbar, Menu, filedialog, StringVar, ttk, Listbox, END, SINGLE, messagebox

class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Easier IDE")

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "easier.png")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.documents_listbox = Listbox(root, selectmode=SINGLE)
        self.documents_listbox.pack(side="left", fill="y")

        self.documents_scroll = Scrollbar(root, orient="vertical", command=self.documents_listbox.yview)
        self.documents_scroll.pack(side="left", fill="y")
        self.documents_listbox.configure(yscrollcommand=self.documents_scroll.set)

        self.text = Text(root, wrap="word", undo=True)
        self.text.pack(expand="yes", fill="both")

        self.scroll = Scrollbar(root, orient="vertical", command=self.text.yview)
        self.scroll.pack(side="right", fill="y")

        self.text.configure(yscrollcommand=self.scroll.set)

        self.menu = Menu(root)
        root.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        self.help_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.open_files = []  # List to store open file paths
        self.current_file = None

        # Bind double-click event on the documents listbox to open the selected file
        self.documents_listbox.bind("<Double-1>", lambda event: self.open_selected_file())

        # Bind Ctrl+S to save_file
        self.root.bind('<Control-s>', lambda event: self.save_file())

    def set_window_title(self, name=None):
        title = "Easier IDE"
        if name:
            title += f" - {name}"
        self.root.title(title)

    def new_file(self):
        self.text.delete(1.0, "end")
        self.current_file = None
        self.set_window_title()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text.delete(1.0, "end")
            with open(file_path, "r") as file:
                self.text.insert("insert", file.read())
            self.current_file = file_path
            self.open_files.append(file_path)
            self.update_documents_list()

    def save_file(self, event=None):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text.get(1.0, "end-1c"))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get(1.0, "end-1c"))
            self.current_file = file_path
            self.open_files.append(file_path)
            self.update_documents_list()

    def open_selected_file(self):
        selected_index = self.documents_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_file = self.open_files[selected_index]
            if selected_file and os.path.exists(selected_file):
                with open(selected_file, "r") as file:
                    self.text.delete(1.0, "end")
                    self.text.insert("insert", file.read())
                self.current_file = selected_file
                self.set_window_title(os.path.basename(selected_file))

    def update_documents_list(self):
        self.documents_listbox.delete(0, END)
        for file_path in self.open_files:
            self.documents_listbox.insert(END, os.path.basename(file_path))

    def exit_app(self):
        self.root.destroy()

    def show_about(self):
        about_text = "Easier IDE\n\nA simple text editor with basic functionality.\nVersion: 1.0\n\nDeveloped by WebSolvus for debugging code with machine learning."
        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    root = Tk()
    app = SimpleIDE(root)
    root.mainloop()
