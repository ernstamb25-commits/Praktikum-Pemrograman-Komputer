import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import csv # Library untuk export data
import database

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengeluaran Pro")
        self.root.geometry("700x550") # Sedikit lebih lebar

        # Variabel untuk mode Edit
        self.editing_id = None 

        # --- Frame Input ---
        self.input_frame = ttk.LabelFrame(root, text="Form Input")
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Baris 1: Tanggal & Kategori
        ttk.Label(self.input_frame, text="Tanggal (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.insert(0, datetime.date.today())
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Kategori:").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.input_frame, textvariable=self.category_var, state="readonly")
        self.category_combo['values'] = ("Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan", "Kesehatan", "Lainnya")
        self.category_combo.current(0)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)

        # Baris 2: Jumlah & Keterangan
        ttk.Label(self.input_frame, text="Jumlah (Rp):").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Keterangan:").grid(row=1, column=2, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        # Baris 3: Tombol Simpan & Batal Edit
        self.btn_frame = ttk.Frame(self.input_frame)
        self.btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.save_btn = ttk.Button(self.btn_frame, text="Simpan Data", command=self.save_data)
        self.save_btn.pack(side="left", padx=5)

        self.cancel_btn = ttk.Button(self.btn_frame, text="Batal Edit", command=self.reset_form, state="disabled")
        self.cancel_btn.pack(side="left", padx=5)

        # --- Frame Tabel ---
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Tanggal", "Kategori", "Jumlah", "Keterangan")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=12)
        
        headers = ["ID", "Tanggal", "Kategori", "Jumlah (Rp)", "Keterangan"]
        widths = [30, 90, 100, 120, 200]
        
        for col, title, w in zip(columns, headers, widths):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=w)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- Frame Tombol Aksi (Bawah) ---
        self.action_frame = ttk.Frame(root)
        self.action_frame.pack(fill="x", padx=10, pady=10)

        # Tombol-tombol aksi
        self.edit_btn = ttk.Button(self.action_frame, text="Edit Data Terpilih", command=self.load_edit_data)
        self.edit_btn.pack(side="left", padx=5)

        self.del_btn = ttk.Button(self.action_frame, text="Hapus Data", command=self.delete_data)
        self.del_btn.pack(side="left", padx=5)

        self.export_btn = ttk.Button(self.action_frame, text="Export ke Excel (CSV)", command=self.export_csv)
        self.export_btn.pack(side="left", padx=5)

        self.total_label = ttk.Label(self.action_frame, text="Total: Rp 0", font=("Arial", 11, "bold"))
        self.total_label.pack(side="right", padx=5)

        # Load data awal
        self.refresh_table()

    def save_data(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()

        if not date or not amount:
            messagebox.showerror("Error", "Tanggal dan Jumlah wajib diisi!")
            return

        try:
            amount = float(amount)
            
            if self.editing_id: 
                # Jika sedang mode edit (Update)
                database.update_expense(self.editing_id, date, category, amount, desc)
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
            else:
                # Jika mode tambah baru (Insert)
                database.add_expense(date, category, amount, desc)
                messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
            
            self.reset_form()
            self.refresh_table()
            
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")

    def load_edit_data(self):
        """Mengambil data dari tabel ke form input untuk diedit"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit!")
            return

        # Ambil data dari baris yang dipilih
        item_data = self.tree.item(selected_item[0])['values']
        
        # Simpan ID yang sedang diedit
        self.editing_id = item_data[0]

        # Masukkan data ke form input
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, item_data[1])
        
        self.category_combo.set(item_data[2])
        
        # Bersihkan 'Rp ' dan koma sebelum dimasukkan ke entry
        clean_amount = str(item_data[3]).replace("Rp ", "").replace(",", "")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, clean_amount)
        
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, item_data[4])

        # Ubah tampilan tombol
        self.save_btn.config(text="Update Data")
        self.cancel_btn.config(state="normal")
        self.input_frame.config(text=f"Sedang Mengedit ID: {self.editing_id}")

    def reset_form(self):
        """Mengembalikan form ke kondisi awal (Reset)"""
        self.editing_id = None
        self.save_btn.config(text="Simpan Data")
        self.cancel_btn.config(state="disabled")
        self.input_frame.config(text="Form Input")
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.date.today())
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.category_combo.current(0)

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            for item in selected_item:
                item_id = self.tree.item(item)['values'][0]
                database.delete_expense(item_id)
            self.refresh_table()
            self.reset_form() # Reset jika user menghapus data yang sedang diedit

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = database.fetch_expenses()
        total_expense = 0
        
        for row in rows:
            # Format Rupiah
            formatted_amount = f"{row[3]:,.0f}"
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], formatted_amount, row[4]))
            total_expense += row[3]

        self.total_label.config(text=f"Total: Rp {total_expense:,.0f}")

    def export_csv(self):
        """Menyimpan data ke file CSV"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return # User membatalkan penyimpanan

        rows = database.fetch_expenses()
        
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Tulis Header
                writer.writerow(["ID", "Tanggal", "Kategori", "Jumlah", "Keterangan"])
                # Tulis Data
                writer.writerows(rows)
            messagebox.showinfo("Sukses", "Data berhasil diexport!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {e}")