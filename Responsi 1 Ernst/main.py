import tkinter as tk
from ui import ExpenseTrackerApp
import database

if __name__ == "__main__":
    database.init_db()
    
    root = tk.Tk()
    # Mengatur tema agar sedikit lebih modern (opsional)
    try:
        root.tk.call("source", "azure.tcl") # Baris ini abaikan jika tidak punya tema eksternal
        root.tk.call("set_theme", "light")
    except:
        pass
        
    app = ExpenseTrackerApp(root)
    root.mainloop()