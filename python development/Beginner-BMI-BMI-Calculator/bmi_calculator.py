import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


# ---------------- DATABASE SETUP ----------------

try:
    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT
        recorded_at TEXT
    )
    """)

    conn.commit()
    
    try:
        cursor.execute(
            "ALTER TABLE bmi_records ADD COLUMN recorded_at TEXT"
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass

except sqlite3.Error as e:
    print("Database error:", e)


# ---------------- GUI SETUP ----------------

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x500")


tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 20, "bold")
).pack(pady=15)


tk.Label(
    root,
    text="User Name"
).pack()

name_entry = tk.Entry(root)
name_entry.pack(pady=5)


tk.Label(
    root,
    text="Weight (kg)"
).pack()

weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)


tk.Label(
    root,
    text="Height (m)"
).pack()

height_entry = tk.Entry(root)
height_entry.pack(pady=5)


# ---------------- BMI CALCULATION ----------------

def calculate_bmi():

    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        # Check empty name
        if not name:
            result_label.config(
                text="Please enter your name.",
                fg="red"
            )
            return

        # Check positive values
        if weight <= 0 or height <= 0:
            result_label.config(
                text="Weight and height must be positive.",
                fg="red"
            )
            return

        # BMI calculation
        bmi = round(weight / (height ** 2), 2)
        recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # BMI category
        if bmi < 18.5:
            category = "Underweight"
            result_color = "orange"

        elif bmi < 25:
            category = "Normal"
            result_color = "green"

        elif bmi < 30:
            category = "Overweight"
            result_color = "orange"

        else:
            category = "Obese"
            result_color = "red"

        # Display result
        result_label.config(
            text=f"{name}\nBMI: {bmi}\nCategory: {category}",
            fg=result_color
        )

        # Save record to database
        try:
            cursor.execute(
                """
                INSERT INTO bmi_records
                (name, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, weight, height, bmi, category, recorded_at)
         )

            conn.commit()

        except sqlite3.Error as e:
            result_label.config(
                text=f"BMI: {bmi}\nCategory: {category}\nDatabase error!",
                fg="red"
            )
            print("Database error:", e)

    except ValueError:
        result_label.config(
            text="Please enter valid numbers.",
            fg="red"
        )


# ---------------- VIEW HISTORY ----------------

def view_history():

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("600x400")

    tk.Label(
        history_window,
        text="BMI History",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    history_text = tk.Text(
        history_window,
        width=70,
        height=18
    )
    history_text.pack(pady=10)

    try:
        cursor.execute("""
            SELECT name, weight, height, bmi, category
            FROM bmi_records
            ORDER BY id DESC
        """)

        records = cursor.fetchall()

        if not records:
            history_text.insert(
                tk.END,
                "No BMI records found."
            )

        else:
            for record in records:

                name, weight, height, bmi, category = record

                history_text.insert(
                    tk.END,
                    f"Name: {name}\n"
                    f"Weight: {weight} kg\n"
                    f"Height: {height} m\n"
                    f"BMI: {bmi}\n"
                    f"Category: {category}\n"
                    f"{'-' * 50}\n"
                )

    except sqlite3.Error as e:
        history_text.insert(
            tk.END,
            f"Database error: {e}"
        )
# ---------------- BMI TREND CHART ----------------

def show_bmi_trend():

    name = name_entry.get().strip()

    if not name:
        result_label.config(
            text="Please enter a user name first.",
            fg="red"
        )
        return

    try:
        cursor.execute(
            """
            SELECT recorded_at, bmi
            FROM bmi_records
            WHERE name = ?
            ORDER BY recorded_at
            """,
            (name,)
        )

        records = cursor.fetchall()

        if not records:
            result_label.config(
                text="No BMI history found for this user.",
                fg="red"
            )
            return

        dates = [record[0] for record in records]
        bmi_values = [record[1] for record in records]

        plt.figure(figsize=(8, 5))
        plt.plot(dates, bmi_values, marker="o")

        plt.title(f"BMI Trend - {name}")
        plt.xlabel("Date and Time")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        plt.show()

    except sqlite3.Error as e:
        result_label.config(
            text="Database error while loading BMI trend.",
            fg="red"
        )
        print("Database error:", e)

# ---------------- BUTTONS ----------------

calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 12, "bold")
)

calculate_button.pack(pady=10)


history_button = tk.Button(
    root,
    text="View History",
    command=view_history,
    font=("Arial", 12, "bold")    
)

history_button.pack(pady=10)

trend_button = tk.Button(
    root,
    text="View BMI Trend",
    command=show_bmi_trend,
    font=("Arial", 12, "bold")
)

trend_button.pack(pady=10)


# ---------------- RESULT ----------------

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold")
)

result_label.pack(pady=10)


# ---------------- START APPLICATION ----------------

root.mainloop()

# Close database connection
conn.close()