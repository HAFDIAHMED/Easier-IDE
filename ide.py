import os
from tkinter import Tk, Text, Scrollbar, Menu, filedialog, StringVar, ttk, Listbox, END, SINGLE

class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Easier IDE")

        self.documents_listbox = Listbox(root, selectmode=SINGLE)
        self.documents_listbox.pack(side="left", fill="y")

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

        self.current_file = None

        # Bind double-click event on the documents listbox to open the selected file
        self.documents_listbox.bind("<Double-1>", lambda event: self.open_selected_file())

    def set_window_title(self, name=None):
        title = "Simple IDE"
        if name:
            title += f" - {name}"
        self.root.title(title)

    def new_file(self):
        self.text.delete(1.0, "end")
        self.current_file = None
        self.set_window_title()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.text.delete(1.0, "end")
            with open(file_path, "r") as file:
                self.text.insert("insert", file.read())
            self.current_file = file_path
            self.update_documents_list()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text.get(1.0, "end-1c"))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get(1.0, "end-1c"))
            self.current_file = file_path
            self.update_documents_list()

    def open_selected_file(self):
        selected_index = self.documents_listbox.curselection()
        if selected_index:
            selected_file = self.documents_listbox.get(selected_index)
            if selected_file and os.path.exists(selected_file):
                with open(selected_file, "r") as file:
                    self.text.delete(1.0, "end")
                    self.text.insert("insert", file.read())
                self.current_file = selected_file
                self.set_window_title(os.path.basename(selected_file))

    def update_documents_list(self):
        self.documents_listbox.delete(0, END)
        if self.current_file:
            self.documents_listbox.insert(END, self.current_file)

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = SimpleIDE(root)
    root.mainloop()
