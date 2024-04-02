import ctypes, tkinter as tk
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    root.iconbitmap("images/logo.ico")
    
    app = GUI(root)
    root.mainloop()