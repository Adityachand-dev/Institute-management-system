from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import date, datetime
import database

database.create_tables()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


def configure_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="#ffffff",
        fieldbackground="#2b2b2b",
        rowheight=32,
        font=("Segoe UI", 11)
    )
    style.configure(
        "Treeview.Heading",
        background="#1f538d",
        foreground="#ffffff",
        font=("Segoe UI", 12, "bold")
    )
    style.map(
        "Treeview",
        background=[("selected", "#144870")],
        foreground=[("selected", "#ffffff")]
    )


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Institute Student Management System")
        self.geometry("520x460")
        self.resizable(False, False)
        self.attempts = 3

        ctk.CTkLabel(
            self,
            text="Institute Student Management System",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(35, 10))

        ctk.CTkLabel(
            self,
            text="Administrator Login",
            font=("Segoe UI", 18)
        ).pack(pady=5)

        self.username = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Username"
        )
        self.username.pack(pady=12)

        self.password = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=12)

        ctk.CTkButton(
            self,
            text="Login",
            width=320,
            height=42,
            font=("Segoe UI", 14, "bold"),
            command=self.login
        ).pack(pady=20)

        self.info = ctk.CTkLabel(
            self,
            text="Attempts Remaining : 3",
            text_color="red",
            font=("Segoe UI", 13)
        )
        self.info.pack()

        self.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        try:
            conn = database.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM admin WHERE username=? AND password=?",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                database.add_log("Administrator Logged In")
                messagebox.showinfo("Success", "Login Successful.")
                self.destroy()
                dashboard = Dashboard()
                dashboard.mainloop()
            else:
                self.attempts -= 1
                self.info.configure(text=f"Attempts Remaining : {self.attempts}")
                if self.attempts <= 0:
                    database.add_log("Login Failed (3 Attempts)")
                    messagebox.showerror("Access Denied", "Maximum login attempts reached.")
                    self.destroy()
                else:
                    messagebox.showerror("Login Failed", "Invalid Username or Password.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Institute Student Management System - Dashboard")
        self.minsize(1100, 700)
        
        # Open directly in maximized state cleanly
        self.after(10, lambda: self.state("zoomed"))

        configure_treeview_style()

        ctk.CTkLabel(
            self,
            text="Institute Student Management System",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Administrator Dashboard",
            font=("Segoe UI", 18)
        ).pack(pady=(0, 15))

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.menu = ctk.CTkFrame(self.main_frame, width=280)
        self.menu.pack(side="left", fill="y", padx=10, pady=10)
        self.menu.pack_propagate(False)

        ctk.CTkLabel(self.menu, text="Navigation Menu", font=("Segoe UI", 20, "bold")).pack(pady=15)

        self.content = ctk.CTkFrame(self.main_frame)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        button_width = 240
        menu_items = [
            ("Student Registration", lambda: StudentRegistration(self)),
            ("Display All Students", lambda: ViewStudents(self)),
            ("Search Student", lambda: SearchStudent(self)),
            ("Update Student", lambda: UpdateStudent(self)),
            ("Delete Student", lambda: DeleteStudent(self)),
            ("Course Management", lambda: CourseManagement(self)),
            ("Batch Management", lambda: BatchManagement(self)),
            ("Fee Management", lambda: FeeManagement(self)),
            ("Attendance", lambda: AttendanceWindow(self)),
            ("Reports", lambda: ReportsWindow(self)),
            ("Logout", self.logout),
        ]

        for text, cmd in menu_items:
            ctk.CTkButton(
                self.menu,
                text=text,
                width=button_width,
                height=38,
                font=("Segoe UI", 13),
                command=cmd
            ).pack(pady=5)

        self.show_welcome()

    def show_welcome(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        students, courses, batches, fees = database.dashboard_statistics()

        title = ctk.CTkLabel(self.content, text="System Overview", font=("Segoe UI", 26, "bold"))
        title.pack(pady=(25, 10))

        stats_frame = ctk.CTkFrame(self.content)
        stats_frame.pack(padx=20, pady=20, fill="x")
        stats_frame.grid_columnconfigure((0, 1), weight=1)

        metrics = [
            ("👨‍🎓 Total Students", f"{students}", 0, 0),
            ("📚 Active Courses", f"{courses}", 0, 1),
            ("🕒 Total Batches", f"{batches}", 1, 0),
            ("💰 Fees Collected", f"₹ {fees:,.2f}", 1, 1),
        ]

        for title_text, val_text, row, col in metrics:
            card = ctk.CTkFrame(stats_frame, corner_radius=12)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            ctk.CTkLabel(card, text=title_text, font=("Segoe UI", 16, "bold")).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=val_text, font=("Segoe UI", 26, "bold"), text_color="#3B8ED0").pack(pady=(0, 15))

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            database.add_log("Administrator Logged Out")
            self.destroy()
            LoginWindow().mainloop()


class ViewStudents(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Student Records")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=15)

        self.search = ctk.CTkEntry(top, width=350, height=38, placeholder_text="Search by Name, Mobile, or Course...")
        self.search.pack(side="left", padx=10)

        ctk.CTkButton(top, text="Search", width=120, height=38, command=self.search_student).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Refresh", width=120, height=38, fg_color="gray40", command=self.load_students).pack(side="left", padx=5)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("ID", "Name", "Gender", "Mobile", "Course", "Batch", "Course Fee", "Fee Paid", "Balance")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

        col_configs = [
            ("ID", 70), ("Name", 220), ("Gender", 90), ("Mobile", 130),
            ("Course", 160), ("Batch", 130), ("Course Fee", 110), ("Fee Paid", 110), ("Balance", 110)
        ]

        for col, width in col_configs:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center", stretch=True)

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

        self.search.bind("<KeyRelease>", lambda e: self.search_student())
        self.load_students()

    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        for student in database.get_all_students():
            self.tree.insert("", "end", values=(
                student["student_id"], student["full_name"], student["gender"],
                student["mobile"], student["course"], student["batch"],
                f"₹{student['course_fee']:.2f}", f"₹{student['fee_paid']:.2f}", f"₹{student['balance_fee']:.2f}"
            ))

    def search_student(self):
        kw = self.search.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for s in database.get_all_students():
            if kw in s["full_name"].lower() or kw in s["mobile"] or kw in s["course"].lower():
                self.tree.insert("", "end", values=(
                    s["student_id"], s["full_name"], s["gender"],
                    s["mobile"], s["course"], s["batch"],
                    f"₹{s['course_fee']:.2f}", f"₹{s['fee_paid']:.2f}", f"₹{s['balance_fee']:.2f}"
                ))


class StudentRegistration(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Student Registration")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(scroll, text="New Student Onboarding", font=("Segoe UI", 24, "bold")).pack(pady=20)

        self.name = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Full Name")
        self.name.pack(pady=8)

        self.gender = ctk.CTkComboBox(scroll, width=600, height=40, values=["Male", "Female", "Other"])
        self.gender.set("Male")
        self.gender.pack(pady=8)

        self.dob = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Date of Birth (DD/MM/YYYY)")
        self.dob.pack(pady=8)

        self.mobile = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="10-Digit Mobile Number")
        self.mobile.pack(pady=8)

        self.email = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Email Address")
        self.email.pack(pady=8)

        self.address = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Residential Address")
        self.address.pack(pady=8)

        self.course = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Enrolled Course")
        self.course.pack(pady=8)

        self.batch = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Assigned Batch")
        self.batch.pack(pady=8)

        self.fees = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Total Course Fee")
        self.fees.pack(pady=8)

        self.paid = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Initial Fee Paid")
        self.paid.insert(0, "0")
        self.paid.pack(pady=8)

        btn_frame = ctk.CTkFrame(scroll)
        btn_frame.pack(pady=25)

        ctk.CTkButton(btn_frame, text="Register Student", width=220, height=42, command=self.save_student).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Clear Form", width=220, height=42, fg_color="gray40", command=self.clear).grid(row=0, column=1, padx=10)

    def save_student(self):
        try:
            name = self.name.get().strip()
            mobile = self.mobile.get().strip()
            if not name:
                messagebox.showerror("Validation Error", "Student name is required.")
                return
            if not mobile.isdigit() or len(mobile) != 10:
                messagebox.showerror("Validation Error", "Enter a valid 10-digit mobile number.")
                return

            fee = float(self.fees.get() or 0)
            paid = float(self.paid.get() or 0)

            if fee < 0 or paid < 0:
                messagebox.showerror("Validation Error", "Fee values cannot be negative.")
                return
            if paid > fee:
                messagebox.showerror("Validation Error", "Initial paid fee cannot exceed total fee.")
                return

            balance = fee - paid
            student_data = (
                name, self.gender.get(), self.dob.get().strip(), mobile,
                self.email.get().strip(), self.address.get().strip(),
                self.course.get().strip(), self.batch.get().strip(),
                str(date.today()), fee, paid, balance
            )
            sid = database.add_student(student_data)
            messagebox.showinfo("Success", f"Student registered successfully!\nGenerated Student ID: {sid}")
            self.clear()
            if isinstance(self.master, Dashboard):
                self.master.show_welcome()
        except ValueError:
            messagebox.showerror("Error", "Fee amounts must be numeric.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear(self):
        for e in [self.name, self.dob, self.mobile, self.email, self.address, self.course, self.batch, self.fees, self.paid]:
            e.delete(0, "end")
        self.gender.set("Male")
        self.paid.insert(0, "0")


class SearchStudent(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Search Student")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Student Search Portal", font=("Segoe UI", 24, "bold")).pack(pady=20)

        top = ctk.CTkFrame(self)
        top.pack(pady=10)

        self.search = ctk.CTkEntry(top, width=420, height=40, placeholder_text="Enter Student ID or 10-Digit Mobile")
        self.search.pack(side="left", padx=10)
        ctk.CTkButton(top, text="Search Record", width=140, height=40, command=self.search_student).pack(side="left", padx=5)

        self.result = ctk.CTkTextbox(self, width=900, height=520, font=("Consolas", 14))
        self.result.pack(fill="both", expand=True, padx=40, pady=20)

    def search_student(self):
        val = self.search.get().strip()
        self.result.delete("1.0", "end")
        if not val:
            messagebox.showerror("Error", "Please provide a Student ID or Mobile Number.")
            return

        student = database.search_student(mobile=val) if len(val) == 10 and val.isdigit() else (
            database.search_student(student_id=int(val)) if val.isdigit() else None
        )

        if not student:
            self.result.insert("end", "\n   No record matching criteria.")
            return

        report = f"""
========================================================================================
                                 STUDENT RECORD PROFILE
========================================================================================
 Student ID      : {student['student_id']}
 Full Name       : {student['full_name']}
 Gender          : {student['gender']}
 Date of Birth   : {student['dob']}
 Mobile Number   : {student['mobile']}
 Email Address   : {student['email']}
 Address         : {student['address']}
 Enrolled Course : {student['course']}
 Batch Timing    : {student['batch']}
 Admission Date  : {student['admission_date']}
 ---------------------------------------------------------------------------------------
 Course Fee      : ₹{student['course_fee']:.2f}
 Total Paid      : ₹{student['fee_paid']:.2f}
 Balance Due     : ₹{student['balance_fee']:.2f}
========================================================================================
"""
        self.result.insert("end", report)


class UpdateStudent(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Update Student Details")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(scroll, text="Update Student Record", font=("Segoe UI", 24, "bold")).pack(pady=15)

        top = ctk.CTkFrame(scroll)
        top.pack(pady=10)
        self.search_id = ctk.CTkEntry(top, width=350, height=40, placeholder_text="Enter Student ID to Load")
        self.search_id.pack(side="left", padx=10)
        ctk.CTkButton(top, text="Fetch Record", width=140, height=40, command=self.load_student).pack(side="left", padx=5)

        self.name = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Full Name")
        self.name.pack(pady=6)
        self.gender = ctk.CTkComboBox(scroll, width=600, height=40, values=["Male", "Female", "Other"])
        self.gender.pack(pady=6)
        self.dob = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Date of Birth")
        self.dob.pack(pady=6)
        self.mobile = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Mobile Number")
        self.mobile.pack(pady=6)
        self.email = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Email Address")
        self.email.pack(pady=6)
        self.address = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Address")
        self.address.pack(pady=6)
        self.course = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Course")
        self.course.pack(pady=6)
        self.batch = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Batch")
        self.batch.pack(pady=6)
        self.fee = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Course Fee")
        self.fee.pack(pady=6)
        self.paid = ctk.CTkEntry(scroll, width=600, height=40, placeholder_text="Fee Paid")
        self.paid.pack(pady=6)

        ctk.CTkButton(scroll, text="Commit Updates", width=260, height=42, command=self.update_student).pack(pady=20)

    def load_student(self):
        sid = self.search_id.get().strip()
        if not sid.isdigit():
            messagebox.showerror("Error", "Enter a valid numeric Student ID.")
            return
        student = database.search_student(student_id=int(sid))
        if not student:
            messagebox.showerror("Error", "Student record not found.")
            return

        fields = [
            (self.name, student["full_name"]), (self.dob, student["dob"]),
            (self.mobile, student["mobile"]), (self.email, student["email"]),
            (self.address, student["address"]), (self.course, student["course"]),
            (self.batch, student["batch"]), (self.fee, str(student["course_fee"])),
            (self.paid, str(student["fee_paid"]))
        ]
        for entry, val in fields:
            entry.delete(0, "end")
            entry.insert(0, val)
        self.gender.set(student["gender"])

    def update_student(self):
        try:
            sid = self.search_id.get().strip()
            name = self.name.get().strip()
            mobile = self.mobile.get().strip()
            if not sid.isdigit() or not name or len(mobile) != 10:
                messagebox.showerror("Validation Error", "Ensure valid ID, non-empty Name, and 10-digit mobile.")
                return
            fee = float(self.fee.get() or 0)
            paid = float(self.paid.get() or 0)
            if paid > fee:
                messagebox.showerror("Error", "Paid fee cannot exceed Course Fee.")
                return

            data = (
                name, self.gender.get(), self.dob.get().strip(), mobile,
                self.email.get().strip(), self.address.get().strip(),
                self.course.get().strip(), self.batch.get().strip(),
                fee, paid, fee - paid, int(sid)
            )
            database.update_student(data)
            messagebox.showinfo("Success", "Student updated successfully.")
            if isinstance(self.master, Dashboard):
                self.master.show_welcome()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class DeleteStudent(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Delete Student")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Remove Student Record", font=("Segoe UI", 24, "bold")).pack(pady=20)
        top = ctk.CTkFrame(self)
        top.pack(pady=10)

        self.student_id = ctk.CTkEntry(top, width=320, height=40, placeholder_text="Enter Student ID")
        self.student_id.pack(side="left", padx=10)
        ctk.CTkButton(top, text="Verify Record", width=140, height=40, command=self.search_student).pack(side="left", padx=5)

        self.info = ctk.CTkTextbox(self, width=700, height=220, font=("Consolas", 14))
        self.info.pack(pady=20)

        ctk.CTkButton(
            self,
            text="Permanently Delete Student",
            width=260,
            height=42,
            fg_color="#A8282B",
            hover_color="#7A1D1F",
            command=self.delete_student
        ).pack(pady=10)

    def search_student(self):
        self.info.delete("1.0", "end")
        sid = self.student_id.get().strip()
        if not sid.isdigit():
            messagebox.showerror("Error", "Enter a valid numeric Student ID.")
            return
        student = database.search_student(student_id=int(sid))
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
        self.info.insert("end", f"ID: {student['student_id']}\nName: {student['full_name']}\nCourse: {student['course']}\nBatch: {student['batch']}\nMobile: {student['mobile']}")

    def delete_student(self):
        sid = self.student_id.get().strip()
        if not sid.isdigit():
            return
        student = database.search_student(student_id=int(sid))
        if not student:
            return
        if messagebox.askyesno("Confirm Deletion", f"Permanently delete student '{student['full_name']}'?"):
            database.delete_student(int(sid))
            messagebox.showinfo("Success", "Record deleted successfully.")
            if isinstance(self.master, Dashboard):
                self.master.show_welcome()
            self.destroy()


class CourseManagement(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Course Management")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Course Configuration", font=("Segoe UI", 24, "bold")).pack(pady=15)

        form = ctk.CTkFrame(self)
        form.pack(pady=10, padx=20, fill="x")

        self.course = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Course Name")
        self.course.grid(row=0, column=0, padx=10, pady=10)
        self.duration = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Duration (e.g. 6 Months)")
        self.duration.grid(row=0, column=1, padx=10, pady=10)
        self.fees = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Course Fees")
        self.fees.grid(row=0, column=2, padx=10, pady=10)

        btn_box = ctk.CTkFrame(self)
        btn_box.pack(pady=10)
        ctk.CTkButton(btn_box, text="Add Course", width=140, height=38, command=self.add_course).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_box, text="Update Course", width=140, height=38, command=self.update_course).grid(row=0, column=1, padx=8)
        ctk.CTkButton(btn_box, text="Refresh", width=140, height=38, fg_color="gray40", command=self.load_courses).grid(row=0, column=2, padx=8)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        columns = ("ID", "Course Name", "Duration", "Fees")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col, width in zip(columns, [90, 320, 220, 180]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_entries)
        self.load_courses()

    def load_courses(self):
        self.tree.delete(*self.tree.get_children())
        for row in database.get_courses():
            self.tree.insert("", "end", values=(row["course_id"], row["course_name"], row["duration"], f"₹{row['fees']:.2f}"))

    def add_course(self):
        try:
            name, dur = self.course.get().strip(), self.duration.get().strip()
            fees = float(self.fees.get())
            if not name:
                messagebox.showerror("Error", "Enter course name.")
                return
            database.add_course(name, dur, fees)
            messagebox.showinfo("Success", "Course added successfully.")
            self.clear()
            self.load_courses()
            if isinstance(self.master, Dashboard):
                self.master.show_welcome()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fill_entries(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        vals = self.tree.item(sel)["values"]
        for entry, val in [(self.course, vals[1]), (self.duration, vals[2]), (self.fees, str(vals[3]).replace("₹", ""))]:
            entry.delete(0, "end")
            entry.insert(0, val)

    def update_course(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showerror("Error", "Select a course.")
            return
        cid = self.tree.item(sel)["values"][0]
        try:
            database.update_course(cid, self.course.get().strip(), self.duration.get().strip(), float(self.fees.get()))
            messagebox.showinfo("Success", "Course updated.")
            self.load_courses()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear(self):
        for e in [self.course, self.duration, self.fees]:
            e.delete(0, "end")


class BatchManagement(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Batch Management")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Batch Scheduling", font=("Segoe UI", 24, "bold")).pack(pady=15)

        form = ctk.CTkFrame(self)
        form.pack(pady=10, padx=20, fill="x")

        self.batch = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Batch Name")
        self.batch.grid(row=0, column=0, padx=10, pady=10)
        self.timing = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Timing (e.g. 10 AM - 12 PM)")
        self.timing.grid(row=0, column=1, padx=10, pady=10)
        self.course = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Course Name")
        self.course.grid(row=0, column=2, padx=10, pady=10)

        btn_box = ctk.CTkFrame(self)
        btn_box.pack(pady=10)
        ctk.CTkButton(btn_box, text="Add Batch", width=140, height=38, command=self.add_batch).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_box, text="Refresh", width=140, height=38, fg_color="gray40", command=self.load_batches).grid(row=0, column=1, padx=8)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        columns = ("ID", "Batch Name", "Timing", "Associated Course")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col, width in zip(columns, [90, 260, 260, 280]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True)
        self.load_batches()

    def load_batches(self):
        self.tree.delete(*self.tree.get_children())
        for row in database.get_batches():
            self.tree.insert("", "end", values=(row["batch_id"], row["batch_name"], row["timing"], row["course_name"]))

    def add_batch(self):
        b, t, c = self.batch.get().strip(), self.timing.get().strip(), self.course.get().strip()
        if not b or not c:
            messagebox.showerror("Error", "Batch and Course Name are required.")
            return
        database.add_batch(b, t, c)
        messagebox.showinfo("Success", "Batch added.")
        for entry in [self.batch, self.timing, self.course]:
            entry.delete(0, "end")
        self.load_batches()
        if isinstance(self.master, Dashboard):
            self.master.show_welcome()


class FeeManagement(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Fee Management & Financial Ledger")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Fee Management & Installment Ledger", font=("Segoe UI", 24, "bold")).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(pady=10)

        self.student_id = ctk.CTkEntry(top, width=320, height=40, placeholder_text="Enter Student ID")
        self.student_id.pack(side="left", padx=10)
        ctk.CTkButton(top, text="Fetch Ledger", width=140, height=40, command=self.search_student).pack(side="left", padx=5)

        self.info = ctk.CTkTextbox(self, width=800, height=130, font=("Consolas", 13))
        self.info.pack(pady=10)

        pay_box = ctk.CTkFrame(self)
        pay_box.pack(pady=10)
        self.amount = ctk.CTkEntry(pay_box, width=300, height=40, placeholder_text="Payment Installment Amount (₹)")
        self.amount.pack(side="left", padx=10)
        ctk.CTkButton(pay_box, text="Collect Fee", width=140, height=40, command=self.collect_fee).pack(side="left", padx=5)

        ctk.CTkLabel(self, text="Historical Payment Ledger", font=("Segoe UI", 16, "bold")).pack(pady=(15, 5))
        self.history = ctk.CTkTextbox(self, width=800, height=220, font=("Consolas", 13))
        self.history.pack(fill="both", expand=True, padx=40, pady=10)

    def search_student(self):
        sid = self.student_id.get().strip()
        self.info.delete("1.0", "end")
        self.history.delete("1.0", "end")
        if not sid.isdigit():
            messagebox.showerror("Error", "Enter a valid numeric Student ID.")
            return
        student = database.search_student(student_id=int(sid))
        if not student:
            messagebox.showerror("Error", "Student record not found.")
            return

        self.info.insert("end", f"Student ID: {student['student_id']} | Name: {student['full_name']} | Course: {student['course']}\nTotal Fee: ₹{student['course_fee']:.2f} | Fee Paid: ₹{student['fee_paid']:.2f} | Balance Remaining: ₹{student['balance_fee']:.2f}")

        payments = database.payment_history(int(sid))
        if payments:
            self.history.insert("end", f"{'PAYMENT DATE & TIME':<30} {'AMOUNT PAID':<20}\n" + "-"*50 + "\n")
            for pay in payments:
                self.history.insert("end", f"{pay['payment_date']:<30} ₹{pay['amount']:,.2f}\n")
        else:
            self.history.insert("end", "No previous payments on file.")

    def collect_fee(self):
        sid = self.student_id.get().strip()
        if not sid.isdigit():
            return
        try:
            amt = float(self.amount.get())
            if amt <= 0:
                messagebox.showerror("Error", "Enter an amount greater than zero.")
                return
            if database.pay_fee(int(sid), amt):
                messagebox.showinfo("Success", "Fee collected successfully.")
                self.amount.delete(0, "end")
                self.search_student()
                if isinstance(self.master, Dashboard):
                    self.master.show_welcome()
            else:
                messagebox.showerror("Error", "Payment exceeds total balance or student does not exist.")
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric amount.")


class AttendanceWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Attendance Management")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Daily Attendance System", font=("Segoe UI", 24, "bold")).pack(pady=15)

        form = ctk.CTkFrame(self)
        form.pack(pady=10)

        self.student_id = ctk.CTkEntry(form, width=280, height=40, placeholder_text="Student ID")
        self.student_id.grid(row=0, column=0, padx=10)
        self.status = ctk.CTkComboBox(form, width=160, height=40, values=["Present", "Absent"])
        self.status.set("Present")
        self.status.grid(row=0, column=1, padx=10)

        ctk.CTkButton(form, text="Mark Attendance", width=160, height=40, command=self.mark_attendance).grid(row=0, column=2, padx=10)
        ctk.CTkButton(form, text="Load Records", width=140, height=40, fg_color="gray40", command=self.load_attendance).grid(row=0, column=3, padx=10)

        self.records = ctk.CTkTextbox(self, width=800, height=450, font=("Consolas", 14))
        self.records.pack(fill="both", expand=True, padx=40, pady=20)

    def mark_attendance(self):
        sid = self.student_id.get().strip()
        if not sid.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Student ID.")
            return
        if database.mark_attendance(int(sid), self.status.get()):
            messagebox.showinfo("Success", "Attendance registered.")
            self.load_attendance()
        else:
            messagebox.showerror("Error", "Attendance already recorded for today or student does not exist.")

    def load_attendance(self):
        self.records.delete("1.0", "end")
        sid = self.student_id.get().strip()
        if not sid.isdigit():
            return
        rows = database.get_attendance(int(sid))
        if not rows:
            self.records.insert("end", "No attendance records found.")
            return
        pct = database.attendance_percentage(int(sid))
        self.records.insert("end", f"Overall Attendance: {pct}%\n" + "="*40 + "\n\n")
        for r in rows:
            self.records.insert("end", f"{r['date']:<20} {r['status']:<15}\n")


class ReportsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Institutional Reports")
        self.after(10, lambda: self.state("zoomed"))
        self.grab_set()

        ctk.CTkLabel(self, text="Analytical System Reports", font=("Segoe UI", 24, "bold")).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=40, pady=10)

        ctk.CTkButton(top, text="Student Directory", width=180, height=38, command=self.student_report).pack(side="left", padx=8)
        ctk.CTkButton(top, text="Financial Report", width=180, height=38, command=self.fee_report).pack(side="left", padx=8)
        ctk.CTkButton(top, text="Attendance Audit", width=180, height=38, command=self.attendance_report).pack(side="left", padx=8)

        self.report = ctk.CTkTextbox(self, width=900, height=520, font=("Consolas", 13))
        self.report.pack(fill="both", expand=True, padx=40, pady=20)

    def student_report(self):
        self.report.delete("1.0", "end")
        rows = database.student_report()
        self.report.insert("end", f"{'ID':<6} {'FULL NAME':<25} {'COURSE':<18} {'BATCH':<15} {'MOBILE':<15}\n" + "="*80 + "\n")
        for r in rows:
            self.report.insert("end", f"{r['student_id']:<6} {r['full_name']:<25} {r['course']:<18} {r['batch']:<15} {r['mobile']:<15}\n")

    def fee_report(self):
        self.report.delete("1.0", "end")
        rows = database.fee_report()
        self.report.insert("end", f"{'ID':<6} {'NAME':<25} {'COURSE FEE':<15} {'PAID':<15} {'BALANCE':<15}\n" + "="*80 + "\n")
        for r in rows:
            self.report.insert("end", f"{r['student_id']:<6} {r['full_name']:<25} ₹{r['course_fee']:<14.2f} ₹{r['fee_paid']:<14.2f} ₹{r['balance_fee']:<14.2f}\n")

    def attendance_report(self):
        self.report.delete("1.0", "end")
        rows = database.attendance_report()
        self.report.insert("end", f"{'ID':<6} {'STUDENT NAME':<25} {'RECORD DATE':<20} {'STATUS':<15}\n" + "="*70 + "\n")
        for r in rows:
            self.report.insert("end", f"{r['student_id']:<6} {r['full_name']:<25} {r['date']:<20} {r['status']:<15}\n")


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
