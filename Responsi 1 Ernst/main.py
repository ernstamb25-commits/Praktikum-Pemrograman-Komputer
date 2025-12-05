import tkinter as tk
from ui import ExpenseTrackerApp
import database

if __name__ == "__main__":
    database.init_db()
    
    root = tk.Tk()
    
    try:
        root.tk.call("source", "azure.tcl") 
        root.tk.call("set_theme", "light")
    except:
        pass
        
    app = ExpenseTrackerApp(root)
    root.mainloop()