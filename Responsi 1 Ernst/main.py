import tkinter as tk
from ui import ExpenseTrackerApp
import database

if __name__ == "__main__":
    # 1. Inisialisasi Database
    database.init_db()
    
    # 2. Jalankan Aplikasi GUI
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()