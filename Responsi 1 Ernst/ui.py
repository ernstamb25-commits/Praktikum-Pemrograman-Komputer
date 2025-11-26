import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import database  # <-- Kita import file database.py yang tadi dibuat

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pelacak Pengeluaran Pribadi")
        self.root.geometry("600x480")

        # --- Frame Input ---
        self.input_frame = ttk.LabelFrame(root, text="Tambah Pengeluaran Baru")
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Input Components
        ttk.Label(self.input_frame, text="Tanggal (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.insert(0, datetime.date.today())
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Kategori:").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.input_frame, textvariable=self.category_var)
        self.category_combo['values'] = ("Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan", "Lainnya")
        self.category_combo.current(0)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Jumlah (Rp):").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Keterangan:").grid(row=1, column=2, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        # Tombol Tambah
        self.add_btn = ttk.Button(self.input_frame, text="Simpan Data", command=self.add_data)
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

        # --- Frame Tabel ---
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Tanggal", "Kategori", "Jumlah", "Keterangan")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)
        
        headers = ["ID", "Tanggal", "Kategori", "Jumlah (Rp)", "Keterangan"]
        widths = [30, 80, 80, 100, 150]
        
        for col, title, w in zip(columns, headers, widths):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=w)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- Frame Bawah ---
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

        self.del_btn = ttk.Button(self.bottom_frame, text="Hapus Data Terpilih", command=self.delete_data)
        self.del_btn.pack(side="left")

        self.total_label = ttk.Label(self.bottom_frame, text="Total: Rp 0", font=("Arial", 10, "bold"))
        self.total_label.pack(side="right")

        # Load data awal
        self.refresh_table()

    def add_data(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()

        if not date or not amount:
            messagebox.showerror("Error", "Tanggal dan Jumlah wajib diisi!")
            return

        try:
            amount = float(amount)
            # Panggil fungsi dari database.py
            database.add_expense(date, category, amount, desc)
            
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.refresh_table()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database.py
        rows = database.fetch_expenses()
        
        total_expense = 0
        for row in rows:
            formatted_amount = f"Rp {row[3]:,.0f}"
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], formatted_amount, row[4]))
            total_expense += row[3]

        self.total_label.config(text=f"Total Pengeluaran: Rp {total_expense:,.0f}")

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            for item in selected_item:
                item_id = self.tree.item(item)['values'][0]
                # Panggil fungsi hapus dari database.py
                database.delete_expense(item_id)
            
            self.refresh_table()