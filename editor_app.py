import tkinter as tk
from tkinter import filedialog, messagebox
from file_manager import open_txt_file, save_txt_file, save_as_pdf

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto")
        self.filename = None
        self.is_modified = False

        self.text_area = tk.Text(self.root, wrap="word", font=("Arial", 12), undo=True)
        self.text_area.pack(expand=1, fill="both")
        self.text_area.bind("<<Modified>>", self.on_modified)

        self._create_menu()

    def _create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como PDF", command=self.save_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.exit_editor)
        menu.add_cascade(label="Archivo", menu=file_menu)

    def on_modified(self, event=None):
        self.is_modified = True
        self.text_area.edit_modified(False)

    def ask_to_save_changes(self):
        if self.is_modified:
            response = messagebox.askyesnocancel("Guardar cambios",
                "¿Deseas guardar los cambios antes de continuar?")
            if response:  # Sí
                self.save_file()
                return True
            elif response is False:  # No
                return True
            else:  # Cancelar
                return False
        return True

    def new_file(self):
        if self.ask_to_save_changes():
            self.text_area.delete("1.0", tk.END)
            self.filename = None
            self.is_modified = False
            self.root.title("Editor de Texto - Nuevo archivo")

    def open_file(self):
        if not self.ask_to_save_changes():
            return
        filepath = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if filepath:
            content = open_txt_file(filepath)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)
            self.filename = filepath
            self.is_modified = False
            self.root.title(f"Editor de Texto - {self.filename}")

    def save_file(self):
        if self.filename:
            save_txt_file(self.filename, self.text_area.get("1.0", tk.END))
            self.is_modified = False
        else:
            self.save_file_as()

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Archivos de texto", "*.txt")])
        if filepath:
            save_txt_file(filepath, self.text_area.get("1.0", tk.END))
            self.filename = filepath
            self.is_modified = False
            self.root.title(f"Editor de Texto - {self.filename}")

    def save_pdf(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("Archivo PDF", "*.pdf")])
        if filepath:
            content = self.text_area.get("1.0", tk.END)
            save_as_pdf(filepath, content)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado como: {filepath}")

    def exit_editor(self):
        if self.ask_to_save_changes():
            self.root.quit()
