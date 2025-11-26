import sqlite3

DB_NAME = "pengeluaran.db"

def init_db():
    """Membuat tabel jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_expense(date, category, amount, description):
    """Menambahkan data baru."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    conn.close()

def fetch_expenses():
    """Mengambil semua data untuk ditampilkan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    """Menghapus data berdasarkan ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()