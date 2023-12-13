import os
from tkinter import Tk, Text, Scrollbar, Menu, filedialog, StringVar, ttk, Listbox, END, SINGLE, messagebox
import openai
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
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

        self.debug_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Debug", menu=self.debug_menu)
        # self.debug_menu.add_command(label="Debug with ChatGPT", command=self.debug_with_chatgpt)
        self.debug_menu.add_command(label="Debug with AI", command=self.debug_code)

        self.help_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.open_files = []  # List to store open file paths
        self.current_file = None

        # Bind double-click event on the documents listbox to open the selected file
        self.documents_listbox.bind("<Double-1>", lambda event: self.open_selected_file())

        # Bind Ctrl+S to save_file
        self.root.bind('<Control-s>', lambda event: self.save_file())
        # Set your OpenAI API key
        openai.api_key = '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'

        # Add a menu item for debugging with ChatGPT
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    def debug_code(self):
            # Fit the model with data before calling predict
            if self.open_files:
                training_data = [self.get_file_content(file) for file in self.open_files]
                labels = [1 if "error" in content.lower() else 0 for content in training_data]
                self.model.fit(training_data, labels)

                # Now you can call predict
                code_text = self.text.get(1.0, "end-1c")
                prediction = self.model.predict([code_text])
                messagebox.showinfo("Debugging Result", f"Is there a syntax error? {'Yes' if prediction[0] == 1 else 'No'}")
            else:
                messagebox.showinfo("Debugging Result", "No training data available.")

    def get_file_content(self, file_path):
        with open(file_path, "r") as file:
            return file.read()
    def debug_with_chatgpt(self):
        if self.current_file:
            with open(self.current_file, "r") as file:
                file_content = file.read()
                debug_output = self.call_chatgpt(file_content)

                # Display the ChatGPT debug output in a messagebox
                messagebox.showinfo("Debug Output", debug_output)

    def call_chatgpt(self, code):
        # Call OpenAI API for debugging
        response = openai.Completion.create(
            engine="text-davinci-002",  # You can use other engines
            prompt=code,
            max_tokens=100
        )

        # Extract the generated text from ChatGPT response
        debug_output = response.choices[0].text.strip()

        return debug_output

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
