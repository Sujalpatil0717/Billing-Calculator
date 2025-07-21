import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Create a table for billing records if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    date TEXT
)
''')
conn.commit()

# Function to calculate total and store in database
def generate_bill():
    item = entry_item.get()
    quantity = entry_qty.get()
    price = entry_price.get()

    if item == "" or quantity == "" or price == "":
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        qty = int(quantity)
        prc = float(price)
        total = qty * prc
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into database
        cursor.execute('INSERT INTO bills (item, quantity, price, total, date) VALUES (?, ?, ?, ?, ?)',
                       (item, qty, prc, total, date))
        conn.commit()

        # Update output label
        label_output.config(text=f"Bill Generated!\nTotal = ₹{total:.2f}")

    except ValueError:
        messagebox.showerror("Type Error", "Enter valid numbers for Quantity and Price.")

# Export bill records to a text file
def export_report():
    cursor.execute("SELECT * FROM bills")
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", "No bills to export.")
        return

    with open("bill_report.txt", "w",encoding='utf-8') as f:
        f.write("=== BILL REPORT ===\n")
        for rec in records:
            f.write(f"ID: {rec[0]} | Item: {rec[1]} | Qty: {rec[2]} | Price: ₹{rec[3]} | Total: ₹{rec[4]} | Date: {rec[5]}\n")
        f.write("\n--- End of Report ---")

    messagebox.showinfo("Exported", "Report saved as 'bill_report.txt'")

# GUI Setup
window = tk.Tk()
window.title("Billing Calculator")
window.geometry("400x300")

tk.Label(window, text="Item Name:").pack()
entry_item = tk.Entry(window)
entry_item.pack()

tk.Label(window, text="Quantity:").pack()
entry_qty = tk.Entry(window)
entry_qty.pack()

tk.Label(window, text="Price (₹):").pack()
entry_price = tk.Entry(window)
entry_price.pack()

tk.Button(window, text="Generate Bill", command=generate_bill).pack(pady=10)
tk.Button(window, text="Export Report", command=export_report).pack(pady=5)

label_output = tk.Label(window, text="")
label_output.pack()

window.mainloop()

# Close DB when app closes
conn.close()
