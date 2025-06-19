from tkinter import filedialog, Tk

def pick_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select Document",
                                      filetypes=[("Text files","*.txt"),("PDF files", "*.pdf"), ("All files", "*.*")])