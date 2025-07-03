from tkinter import Tk
from editor_app import TextEditorApp
from utils import center_window

if __name__ == "__main__":
    root = Tk()
    app = TextEditorApp(root)
    center_window(root, 800, 600)
    root.mainloop()
