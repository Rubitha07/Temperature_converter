import tkinter as tk
from tkinter import messagebox
import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rubitha@2004",
        database="temperature_app"
    )

# === Create Table If Not Exists ===
def setup_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            input_temp FLOAT,
            input_unit VARCHAR(20),
            output_temp FLOAT,
            output_unit VARCHAR(20),
            converted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# === Insert Conversion ===
def save_conversion(input_temp, input_unit, output_temp, output_unit):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversions (input_temp, input_unit, output_temp, output_unit)
        VALUES (%s, %s, %s, %s)
    """, (input_temp, input_unit, output_temp, output_unit))
    conn.commit()
    cursor.close()
    conn.close()

# === Fetch All Records ===
def fetch_all_conversions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversions ORDER BY converted_at DESC")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# === Convert Temperature ===
def convert():
    try:
        input_temp = float(entry_input.get())
        from_unit = var_from.get()
        to_unit = var_to.get()

        if from_unit == to_unit:
            result = input_temp
        elif from_unit == "Celsius":
            result = (input_temp * 9/5) + 32 if to_unit == "Fahrenheit" else input_temp + 273.15
        elif from_unit == "Fahrenheit":
            result = (input_temp - 32) * 5/9 if to_unit == "Celsius" else ((input_temp - 32) * 5/9) + 273.15
        elif from_unit == "Kelvin":
            result = input_temp - 273.15 if to_unit == "Celsius" else ((input_temp - 273.15) * 9/5) + 32

        entry_result.delete(0, tk.END)
        entry_result.insert(0, f"{result:.2f}")

        save_conversion(input_temp, from_unit, result, to_unit)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

# === Show Conversion History ===
def show_history():
    records = fetch_all_conversions()
    history_window = tk.Toplevel(root)
    history_window.title("Conversion History")
    for i, row in enumerate(records):
        tk.Label(history_window, text=str(row)).grid(row=i, column=0)

# === Clear Fields ===
def clear():
    entry_input.delete(0, tk.END)
    entry_result.delete(0, tk.END)

# === GUI Setup ===
root = tk.Tk()
root.title("Temperature Converter")
root.geometry("400x300")

tk.Label(root, text="Input Temperature").grid(row=0, column=0, padx=10, pady=5)
entry_input = tk.Entry(root)
entry_input.grid(row=0, column=1)

tk.Label(root, text="From Unit").grid(row=1, column=0, padx=10)
var_from = tk.StringVar(value="Celsius")
tk.OptionMenu(root, var_from, "Celsius", "Fahrenheit", "Kelvin").grid(row=1, column=1)

tk.Label(root, text="To Unit").grid(row=2, column=0, padx=10)
var_to = tk.StringVar(value="Fahrenheit")
tk.OptionMenu(root, var_to, "Celsius", "Fahrenheit", "Kelvin").grid(row=2, column=1)

tk.Label(root, text="Result").grid(row=3, column=0, padx=10, pady=5)
entry_result = tk.Entry(root)
entry_result.grid(row=3, column=1)

tk.Button(root, text="Convert", command=convert).grid(row=4, column=0, pady=10)
tk.Button(root, text="Clear", command=clear).grid(row=4, column=1)
tk.Button(root, text="View History", command=show_history).grid(row=5, column=0, columnspan=2, pady=10)

# === Initialize Table and Run GUI ===
setup_table()
root.mainloop()
