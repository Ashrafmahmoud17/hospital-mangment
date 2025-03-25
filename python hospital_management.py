import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# قاعدة البيانات
class HospitalDB:
    def __init__(self):
        self.conn = sqlite3.connect("hospital.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )""")

        self.conn.commit()

    def add_doctor(self, name, specialization):
        self.cursor.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)", (name, specialization))
        self.conn.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")

    def add_patient(self, name, age):
        self.cursor.execute("INSERT INTO patients (name, age) VALUES (?, ?)", (name, age))
        self.conn.commit()
        messagebox.showinfo("Success", "Patient added successfully!")

    def schedule_appointment(self, patient_id, doctor_id, date):
        self.cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)", (patient_id, doctor_id, date))
        self.conn.commit()
        messagebox.showinfo("Success", "Appointment scheduled successfully!")

    def view_doctors(self):
        self.cursor.execute("SELECT * FROM doctors")
        return self.cursor.fetchall()

    def view_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        return self.cursor.fetchall()

    def view_appointments(self):
        self.cursor.execute("SELECT * FROM appointments")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


# الواجهة الرسومية المحسنة
class HospitalGUI:
    def __init__(self, root):
        self.db = HospitalDB()
        self.root = root
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("500x500")
        self.root.configure(bg="#f2f2f2")

        # عنوان
        title_label = tk.Label(root, text="Hospital Management System", font=("Arial", 16, "bold"), bg="#007BFF", fg="white", pady=10)
        title_label.pack(fill=tk.X)

        # إطار الأزرار
        button_frame = ttk.Frame(root, padding=20)
        button_frame.pack(pady=10)

        buttons = [
            ("➕ Add Doctor", self.add_doctor),
            ("➕ Add Patient", self.add_patient),
            ("📅 Schedule Appointment", self.schedule_appointment),
            ("👨‍⚕️ View Doctors", self.view_doctors),
            ("🧑‍⚕️ View Patients", self.view_patients),
            ("📋 View Appointments", self.view_appointments),
            ("❌ Exit", root.quit)
        ]

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=25)
            btn.pack(pady=5)

    def add_doctor(self):
        self.create_form("Add Doctor", [("Name", ""), ("Specialization", "")], self.db.add_doctor)

    def add_patient(self):
        self.create_form("Add Patient", [("Name", ""), ("Age", "")], self.db.add_patient)

    def schedule_appointment(self):
        self.create_form("Schedule Appointment", [("Patient ID", ""), ("Doctor ID", ""), ("Date (YYYY-MM-DD)", "")], self.db.schedule_appointment)

    def create_form(self, title, fields, submit_callback):
        def save():
            values = [entry.get() for entry in entries]
            if all(values):
                submit_callback(*values)
                form_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required!")

        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.configure(bg="#f2f2f2")
        form_window.geometry("300x250")

        entries = []
        for field, value in fields:
            ttk.Label(form_window, text=field + ":").pack(pady=5)
            entry = ttk.Entry(form_window)
            entry.insert(0, value)
            entry.pack(pady=5)
            entries.append(entry)

        ttk.Button(form_window, text="Save", command=save).pack(pady=10)

    def view_doctors(self):
        self.show_data("Doctors", self.db.view_doctors(), ["ID", "Name", "Specialization"])

    def view_patients(self):
        self.show_data("Patients", self.db.view_patients(), ["ID", "Name", "Age"])

    def view_appointments(self):
        self.show_data("Appointments", self.db.view_appointments(), ["ID", "Patient ID", "Doctor ID", "Date"])

    def show_data(self, title, data, columns):
        view_window = tk.Toplevel(self.root)
        view_window.title(title)
        view_window.geometry("400x300")
        view_window.configure(bg="white")

        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()
