from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import date, datetime
import database


database.create_tables()


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Institute Student Management System")
        self.geometry("500x420")
        self.resizable(False, False)

        self.attempts = 3

        ctk.CTkLabel(
            self,
            text="Institute Student Management System",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text="Administrator Login",
            font=("Arial", 18)
        ).pack(pady=5)

        self.username = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Username"
        )
        self.username.pack(pady=15)

        self.password = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Login",
            width=300,
            command=self.login
        ).pack(pady=20)

        self.info = ctk.CTkLabel(
            self,
            text="Attempts Remaining : 3",
            text_color="red"
        )
        self.info.pack()

        self.bind("<Return>", lambda event: self.login())

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )
            return

        try:

            conn = database.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM admin
                WHERE username=? AND password=?
                """,
                (username, password)
            )

            user = cursor.fetchone()

            conn.close()

            if user:

                database.add_log("Administrator Logged In")

                messagebox.showinfo(
                    "Success",
                    "Login Successful."
                )

                self.destroy()

                dashboard = Dashboard()
                dashboard.mainloop()

            else:

                self.attempts -= 1

                self.info.configure(
                    text=f"Attempts Remaining : {self.attempts}"
                )

                if self.attempts <= 0:

                    database.add_log("Login Failed (3 Attempts)")

                    messagebox.showerror(
                        "Access Denied",
                        "Maximum login attempts reached."
                    )

                    self.destroy()

                else:

                    messagebox.showerror(
                        "Login Failed",
                        "Invalid Username or Password."
                    )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Institute Student Management System")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        ctk.CTkLabel(
            self,
            text="Institute Student Management System",
            font=("Arial", 28, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Administrator Dashboard",
            font=("Arial", 18)
        ).pack(pady=(0, 20))

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.menu = ctk.CTkFrame(
            self.main_frame,
            width=280
        )

        self.menu.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        self.menu.pack_propagate(False)

        ctk.CTkLabel(
            self.menu,
            text="Menu",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        self.content = ctk.CTkFrame(self.main_frame)

        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        students, courses, batches, fees = database.dashboard_statistics()

        stats_frame = ctk.CTkFrame(self.content)
        stats_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            stats_frame,
            text=f"👨‍🎓 Students : {students}",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, padx=25, pady=20)

        ctk.CTkLabel(
            stats_frame,
            text=f"📚 Courses : {courses}",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=1, padx=25)

        ctk.CTkLabel(
            stats_frame,
            text=f"🕒 Batches : {batches}",
            font=("Arial", 18, "bold")
        ).grid(row=1, column=0, padx=25, pady=20)

        ctk.CTkLabel(
            stats_frame,
            text=f"💰 Fees Collected : ₹{fees}",
            font=("Arial", 18, "bold")
        ).grid(row=1, column=1, padx=25)

        ctk.CTkLabel(
            self.content,
            text="Welcome Administrator",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.content,
            text="Select an option from the left menu.",
            font=("Arial", 16)
        ).pack()

        button_width = 220

        ctk.CTkButton(
            self.menu,
            text="Student Registration",
            width=button_width,
            command=lambda: StudentRegistration(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Display All Students",
            width=button_width,
            command=lambda: ViewStudents(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Search Student",
            width=button_width,
            command=lambda: SearchStudent(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Update Student",
            width=button_width,
            command=lambda: UpdateStudent(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Delete Student",
            width=button_width,
            command=lambda: DeleteStudent(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Course Management",
            width=button_width,
            command=lambda: CourseManagement(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Batch Management",
            width=button_width,
            command=lambda: BatchManagement(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Fee Management",
            width=button_width,
            command=lambda: FeeManagement(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Attendance",
            width=button_width,
            command=lambda: AttendanceWindow(self)
        ).pack(pady=5)

        ctk.CTkButton(
            self.menu,
            text="Reports",
            width=button_width,
            command=lambda: ReportsWindow(self)
        ).pack(pady=5)


    def refresh_dashboard(self):

        students, courses, batches, fees = database.dashboard_statistics()

        try:
            self.students_value.configure(text=str(students))
            self.courses_value.configure(text=str(courses))
            self.batches_value.configure(text=str(batches))
            self.fees_value.configure(text=f"₹ {fees:.2f}")
        except:
            pass

    def show_welcome(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.content,
            text="Welcome Administrator",
            font=("Arial",28,"bold")
        )

        title.pack(pady=(30,10))

        subtitle = ctk.CTkLabel(
            self.content,
            text="Institute Student Management System",
            font=("Arial",18)
        )

        subtitle.pack(pady=(0,30))

        stats_frame = ctk.CTkFrame(self.content)

        stats_frame.pack(
            padx=20,
            pady=20,
            fill="x"
        )

        card1 = ctk.CTkFrame(stats_frame)

        card1.grid(row=0,column=0,padx=15,pady=15)

        ctk.CTkLabel(
            card1,
            text="Students",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.students_value = ctk.CTkLabel(
            card1,
            text="0",
            font=("Arial",30,"bold")
        )

        self.students_value.pack(pady=(0,15))

        card2 = ctk.CTkFrame(stats_frame)

        card2.grid(row=0,column=1,padx=15,pady=15)

        ctk.CTkLabel(
            card2,
            text="Courses",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.courses_value = ctk.CTkLabel(
            card2,
            text="0",
            font=("Arial",30,"bold")
        )

        self.courses_value.pack(pady=(0,15))


        card3 = ctk.CTkFrame(stats_frame)

        card3.grid(row=1,column=0,padx=15,pady=15)

        ctk.CTkLabel(
            card3,
            text="Batches",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.batches_value = ctk.CTkLabel(
            card3,
            text="0",
            font=("Arial",30,"bold")
        )

        self.batches_value.pack(pady=(0,15))

        card4 = ctk.CTkFrame(stats_frame)

        card4.grid(row=1,column=1,padx=15,pady=15)

        ctk.CTkLabel(
            card4,
            text="Fees Collected",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.fees_value = ctk.CTkLabel(
            card4,
            text="₹ 0",
            font=("Arial",30,"bold")
        )

        self.fees_value.pack(pady=(0,15))

        self.refresh_dashboard()

class StudentRegistration(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Student Registration")
        self.geometry("700x760")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Student Registration",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.name = ctk.CTkEntry(self, width=500, placeholder_text="Full Name")
        self.name.pack(pady=8)

        self.gender = ctk.CTkComboBox(
            self,
            values=["Male", "Female", "Other"]
        )
        self.gender.set("Male")
        self.gender.pack(pady=8)

        self.dob = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="DD/MM/YYYY"
        )
        self.dob.pack(pady=8)

        self.mobile = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Mobile Number"
        )
        self.mobile.pack(pady=8)

        self.email = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Email Address"
        )
        self.email.pack(pady=8)

        self.address = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Address"
        )
        self.address.pack(pady=8)

        self.course = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Course"
        )
        self.course.pack(pady=8)

        self.batch = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Batch"
        )
        self.batch.pack(pady=8)

        self.fees = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Course Fee"
        )
        self.fees.pack(pady=8)

        self.paid = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Fee Paid"
        )
        self.paid.insert(0, "0")
        self.paid.pack(pady=8)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Register Student",
            width=180,
            command=self.save_student
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Clear",
            width=180,
            fg_color="gray40",
            command=self.clear
        ).grid(row=0, column=1, padx=10)

    def save_student(self):

        try:

            name = self.name.get().strip()
            mobile = self.mobile.get().strip()

            if not name:
                messagebox.showerror("Error", "Enter student name.")
                return

            if not mobile.isdigit() or len(mobile) != 10:
                messagebox.showerror(
                    "Error",
                    "Enter a valid 10-digit mobile number."
                )
                return

            fee = float(self.fees.get() or 0)
            paid = float(self.paid.get() or 0)

            if fee < 0 or paid < 0:
                messagebox.showerror(
                    "Error",
                    "Fees cannot be negative."
                )
                return

            if paid > fee:
                messagebox.showerror(
                    "Error",
                    "Paid fee cannot exceed total fee."
                )
                return

            balance = fee - paid

            student = (

                name,
                self.gender.get(),
                self.dob.get().strip(),
                mobile,
                self.email.get().strip(),
                self.address.get().strip(),
                self.course.get().strip(),
                self.batch.get().strip(),
                str(date.today()),
                fee,
                paid,
                balance

            )

            student_id = database.add_student(student)

            database.add_log(
                f"Student Registered : {student_id}"
            )

            messagebox.showinfo(
                "Success",
                f"Student Registered Successfully.\n\nStudent ID : {student_id}"
            )

            self.clear()
            
            if isinstance(self.master, Dashboard):
                self.master.show_welcome()
            

        except ValueError:

            messagebox.showerror(
                "Error",
                "Fee fields must contain valid numbers."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def clear(self):

        entries = [

            self.name,
            self.dob,
            self.mobile,
            self.email,
            self.address,
            self.course,
            self.batch,
            self.fees,
            self.paid

        ]

        for entry in entries:
            entry.delete(0, "end")

        self.gender.set("Male")
        self.paid.insert(0, "0")

class SearchStudent(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Search Student")
        self.geometry("700x650")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Search Student",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.search = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Enter Student ID or Mobile Number"
        )

        self.search.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Search",
            width=180,
            command=self.search_student
        ).pack(pady=10)

        self.result = ctk.CTkTextbox(
            self,
            width=620,
            height=420,
            font=("Consolas", 14)
        )

        self.result.pack(pady=20)

    def search_student(self):

        value = self.search.get().strip()

        self.result.delete("1.0", "end")

        if value == "":
            messagebox.showerror(
                "Error",
                "Please enter Student ID or Mobile Number."
            )
            return

        try:

            if value.isdigit():

                if len(value) == 10:
                    student = database.search_student(mobile=value)
                else:
                    student = database.search_student(
                        student_id=int(value)
                    )

            else:

                messagebox.showerror(
                    "Error",
                    "Student ID must be numeric."
                )
                return

            if not student:

                self.result.insert(
                    "end",
                    "No Student Found."
                )
                return

            report = f"""
========================================================

                STUDENT DETAILS

========================================================

Student ID      : {student["student_id"]}

Full Name       : {student["full_name"]}

Gender          : {student["gender"]}

Date of Birth   : {student["dob"]}

Mobile Number   : {student["mobile"]}

Email           : {student["email"]}

Address         : {student["address"]}

Course          : {student["course"]}

Batch           : {student["batch"]}

Admission Date  : {student["admission_date"]}

Course Fee      : ₹{student["course_fee"]:.2f}

Fees Paid       : ₹{student["fee_paid"]:.2f}

Balance Fee     : ₹{student["balance_fee"]:.2f}

========================================================
"""

            self.result.insert(
                "end",
                report
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )
    def update_student(self):

        try:

            sid = self.search_id.get().strip()

            if sid == "":
                messagebox.showerror(
                    "Error",
                    "Enter Student ID."
                )
                return

            if not sid.isdigit():
                messagebox.showerror(
                    "Error",
                    "Student ID must be numeric."
                )
                return

            name = self.name.get().strip()

            mobile = self.mobile.get().strip()

            if name == "":
                messagebox.showerror(
                    "Error",
                    "Student name is required."
                )
                return

            if not mobile.isdigit() or len(mobile) != 10:
                messagebox.showerror(
                    "Error",
                    "Enter a valid 10-digit mobile number."
                )
                return

            fee = float(self.fee.get() or 0)
            paid = float(self.paid.get() or 0)

            if paid > fee:
                messagebox.showerror(
                    "Error",
                    "Paid fee cannot exceed course fee."
                )
                return

            balance = fee - paid

            data = (

                name,
                self.gender.get(),
                self.dob.get().strip(),
                mobile,
                self.email.get().strip(),
                self.address.get().strip(),
                self.course.get().strip(),
                self.batch.get().strip(),
                fee,
                paid,
                balance,
                int(sid)

            )

            database.update_student(data)

            database.add_log(
                f"Student Updated : {sid}"
            )

            messagebox.showinfo(
                "Success",
                "Student details updated successfully."
            )

            if isinstance(self.master, Dashboard):
                self.master.show_welcome()

            self.destroy()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Fee fields must contain valid numbers."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

class DeleteStudent(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Delete Student")
        self.geometry("550x450")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Delete Student",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.student_id = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Enter Student ID"
        )

        self.student_id.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Search",
            width=180,
            command=self.search_student
        ).pack(pady=10)

        self.info = ctk.CTkTextbox(
            self,
            width=450,
            height=150
        )

        self.info.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Delete Student",
            width=180,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_student
        ).pack(pady=15)

    def search_student(self):

        self.info.delete("1.0", "end")

        sid = self.student_id.get().strip()

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter a valid Student ID."
            )
            return

        student = database.search_student(
            student_id=int(sid)
        )

        if not student:

            messagebox.showerror(
                "Error",
                "Student not found."
            )
            return

        text = f"""
Student ID : {student['student_id']}

Name       : {student['full_name']}

Course     : {student['course']}

Batch      : {student['batch']}

Mobile     : {student['mobile']}
"""

        self.info.insert("end", text)

    def delete_student(self):

        sid = self.student_id.get().strip()

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter a valid Student ID."
            )
            return

        student = database.search_student(
            student_id=int(sid)
        )

        if not student:

            messagebox.showerror(
                "Error",
                "Student not found."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student\n\n{student['full_name']} ?"
        )

        if not confirm:
            return

        try:

            database.delete_student(
                int(sid)
            )

            database.add_log(
                f"Student Deleted : {sid}"
            )

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )

            if isinstance(self.master, Dashboard):
                self.master.show_welcome()

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

class ViewStudents(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Student Records")
        self.geometry("1250x650")
        self.grab_set()

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.search = ctk.CTkEntry(
            top,
            width=300,
            placeholder_text="Search Name / Mobile / Course"
        )

        self.search.pack(side="left", padx=10)

        ctk.CTkButton(
            top,
            text="Search",
            command=self.search_student
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            top,
            text="Refresh",
            command=self.load_students
        ).pack(side="left", padx=5)

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (

            "ID",
            "Name",
            "Gender",
            "Mobile",
            "Course",
            "Batch",
            "Fee",
            "Paid",
            "Balance"

        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        widths = [

            70,
            200,
            90,
            130,
            150,
            120,
            100,
            100,
            100

        ]

        for col, width in zip(columns, widths):

            self.tree.heading(col, text=col)

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        yscroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tree.yview
        )

        xscroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        yscroll.pack(
            side="right",
            fill="y"
        )

        xscroll.pack(
            side="bottom",
            fill="x"
        )

        self.tree.bind(
            "<Double-1>",
            self.show_details
        )

        self.load_students()

    def load_students(self):

        self.tree.delete(*self.tree.get_children())

        students = database.get_all_students()

        for student in students:

            self.tree.insert(
                "",
                "end",
                values=(

                    student["student_id"],
                    student["full_name"],
                    student["gender"],
                    student["mobile"],
                    student["course"],
                    student["batch"],
                    student["course_fee"],
                    student["fee_paid"],
                    student["balance_fee"]

                )
            )

    def search_student(self):

        keyword = self.search.get().strip().lower()

        self.tree.delete(*self.tree.get_children())

        students = database.get_all_students()

        for student in students:

            if (

                keyword in student["full_name"].lower()

                or keyword in student["mobile"]

                or keyword in student["course"].lower()

            ):

                self.tree.insert(
                    "",
                    "end",
                    values=(

                        student["student_id"],
                        student["full_name"],
                        student["gender"],
                        student["mobile"],
                        student["course"],
                        student["batch"],
                        student["course_fee"],
                        student["fee_paid"],
                        student["balance_fee"]

                    )
                )

    def show_details(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        student = database.search_student(
            student_id=int(values[0])
        )

        messagebox.showinfo(
            "Student Details",
            f"""
Student ID : {student['student_id']}

Name : {student['full_name']}

Gender : {student['gender']}

DOB : {student['dob']}

Mobile : {student['mobile']}

Email : {student['email']}

Address : {student['address']}

Course : {student['course']}

Batch : {student['batch']}

Course Fee : ₹{student['course_fee']}

Paid : ₹{student['fee_paid']}

Balance : ₹{student['balance_fee']}
"""
        )

class UpdateStudent(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Update Student")
        self.geometry("700x760")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Update Student",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        self.search_id = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Enter Student ID"
        )
        self.search_id.pack(pady=8)

        ctk.CTkButton(
            self,
            text="Load Student",
            command=self.load_student
        ).pack(pady=8)

        self.name = ctk.CTkEntry(self,width=500,placeholder_text="Full Name")
        self.name.pack(pady=6)

        self.gender = ctk.CTkComboBox(
            self,
            values=["Male","Female","Other"]
        )
        self.gender.pack(pady=6)

        self.dob = ctk.CTkEntry(self,width=500,placeholder_text="Date of Birth")
        self.dob.pack(pady=6)

        self.mobile = ctk.CTkEntry(self,width=500,placeholder_text="Mobile")
        self.mobile.pack(pady=6)

        self.email = ctk.CTkEntry(self,width=500,placeholder_text="Email")
        self.email.pack(pady=6)

        self.address = ctk.CTkEntry(self,width=500,placeholder_text="Address")
        self.address.pack(pady=6)

        self.course = ctk.CTkEntry(self,width=500,placeholder_text="Course")
        self.course.pack(pady=6)

        self.batch = ctk.CTkEntry(self,width=500,placeholder_text="Batch")
        self.batch.pack(pady=6)

        self.fee = ctk.CTkEntry(self,width=500,placeholder_text="Course Fee")
        self.fee.pack(pady=6)

        self.paid = ctk.CTkEntry(self,width=500,placeholder_text="Fee Paid")
        self.paid.pack(pady=6)

        ctk.CTkButton(
            self,
            text="Update Student",
            width=220,
            command=self.update_student
        ).pack(pady=20)

    def load_student(self):

        sid = self.search_id.get().strip()

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter a valid Student ID."
            )
            return

        student = database.search_student(
            student_id=int(sid)
        )

        if not student:

            messagebox.showerror(
                "Error",
                "Student not found."
            )
            return

        self.name.delete(0,"end")
        self.name.insert(0,student["full_name"])

        self.gender.set(student["gender"])

        self.dob.delete(0,"end")
        self.dob.insert(0,student["dob"])

        self.mobile.delete(0,"end")
        self.mobile.insert(0,student["mobile"])

        self.email.delete(0,"end")
        self.email.insert(0,student["email"])

        self.address.delete(0,"end")
        self.address.insert(0,student["address"])

        self.course.delete(0,"end")
        self.course.insert(0,student["course"])

        self.batch.delete(0,"end")
        self.batch.insert(0,student["batch"])

        self.fee.delete(0,"end")
        self.fee.insert(0,str(student["course_fee"]))

        self.paid.delete(0,"end")
        self.paid.insert(0,str(student["fee_paid"]))

    def update_student(self):

        try:

            sid = self.search_id.get().strip()

            if sid == "":
                messagebox.showerror(
                    "Error",
                    "Enter Student ID."
                )
                return

            if not sid.isdigit():
                messagebox.showerror(
                    "Error",
                    "Student ID must be numeric."
                )
                return

            name = self.name.get().strip()
            mobile = self.mobile.get().strip()

            if name == "":
                messagebox.showerror(
                    "Error",
                    "Student name is required."
                )
                return

            if not mobile.isdigit() or len(mobile) != 10:
                messagebox.showerror(
                    "Error",
                    "Enter a valid 10-digit mobile number."
                )
                return

            fee = float(self.fee.get() or 0)
            paid = float(self.paid.get() or 0)

            if paid > fee:
                messagebox.showerror(
                    "Error",
                    "Paid fee cannot exceed Course Fee."
                )
                return

            balance = fee - paid

            data = (

                name,
                self.gender.get(),
                self.dob.get().strip(),
                mobile,
                self.email.get().strip(),
                self.address.get().strip(),
                self.course.get().strip(),
                self.batch.get().strip(),
                fee,
                paid,
                balance,
                int(sid)

            )

            database.update_student(data)

            messagebox.showinfo(
                "Success",
                "Student Updated Successfully."
            )

            if isinstance(self.master, Dashboard):
                self.master.show_welcome()

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

class CourseManagement(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Course Management")
        self.geometry("750x550")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Course Management",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        self.course = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Course Name"
        )
        self.course.pack(pady=8)

        self.duration = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Duration (e.g. 6 Months)"
        )
        self.duration.pack(pady=8)

        self.fees = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Course Fees"
        )
        self.fees.pack(pady=8)

        btn = ctk.CTkFrame(self)
        btn.pack(pady=10)

        ctk.CTkButton(
            btn,
            text="Add Course",
            command=self.add_course
        ).grid(row=0,column=0,padx=5)

        ctk.CTkButton(
            btn,
            text="Update Selected",
            command=self.update_course
        ).grid(row=0,column=1,padx=5)

        ctk.CTkButton(
            btn,
            text="Refresh",
            command=self.load_courses
        ).grid(row=0,column=2,padx=5)

        columns=("ID","Course","Duration","Fees")

        self.tree=ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )

        for col,width in zip(columns,[70,220,180,120]):
            self.tree.heading(col,text=col)
            self.tree.column(col,width=width,anchor="center")

        self.tree.pack(fill="both",expand=True,padx=10,pady=10)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.fill_entries
        )

        self.load_courses()

    def load_courses(self):

        self.tree.delete(*self.tree.get_children())

        for row in database.get_courses():

            self.tree.insert(
                "",
                "end",
                values=(
                    row["course_id"],
                    row["course_name"],
                    row["duration"],
                    row["fees"]
                )
            )

    def add_course(self):

        try:

            name=self.course.get().strip()
            duration=self.duration.get().strip()
            fees=float(self.fees.get())

            if name=="":

                messagebox.showerror(
                    "Error",
                    "Enter course name."
                )
                return

            database.add_course(
                name,
                duration,
                fees
            )

            messagebox.showinfo(
                "Success",
                "Course Added Successfully."
            )

            self.clear()
            self.load_courses()

            if isinstance(self.master, Dashboard):
                self.master.show_welcome()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def fill_entries(self,event):

        selected=self.tree.focus()

        if not selected:
            return

        values=self.tree.item(selected)["values"]

        self.course.delete(0,"end")
        self.course.insert(0,values[1])

        self.duration.delete(0,"end")
        self.duration.insert(0,values[2])

        self.fees.delete(0,"end")
        self.fees.insert(0,values[3])

    def update_course(self):

        selected=self.tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a course."
            )
            return

        values=self.tree.item(selected)["values"]

        try:

            database.update_course(

                values[0],
                self.course.get().strip(),
                self.duration.get().strip(),
                float(self.fees.get())

            )

            messagebox.showinfo(
                "Success",
                "Course Updated Successfully."
            )

            self.load_courses()
            self.clear()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def clear(self):

        self.course.delete(0,"end")
        self.duration.delete(0,"end")
        self.fees.delete(0,"end")


class FeeManagement(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Fee Management")
        self.geometry("750x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Fee Management",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        self.student_id = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Student ID"
        )
        self.student_id.pack(pady=8)

        ctk.CTkButton(
            self,
            text="Search",
            command=self.search_student
        ).pack(pady=5)

        self.info = ctk.CTkTextbox(
            self,
            width=650,
            height=180
        )
        self.info.pack(pady=10)

        self.amount = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Payment Amount"
        )
        self.amount.pack(pady=8)

        ctk.CTkButton(
            self,
            text="Collect Fee",
            command=self.collect_fee
        ).pack(pady=10)

        ctk.CTkLabel(
            self,
            text="Payment History",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.history = ctk.CTkTextbox(
            self,
            width=650,
            height=220
        )
        self.history.pack(pady=5)

    def search_student(self):

        sid = self.student_id.get().strip()

        self.info.delete("1.0","end")
        self.history.delete("1.0","end")

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter a valid Student ID."
            )
            return

        student = database.search_student(
            student_id=int(sid)
        )

        if not student:

            messagebox.showerror(
                "Error",
                "Student not found."
            )
            return

        details = f"""
Student ID : {student['student_id']}
Name       : {student['full_name']}
Course     : {student['course']}

Course Fee : ₹{student['course_fee']}
Fee Paid   : ₹{student['fee_paid']}
Balance    : ₹{student['balance_fee']}
"""

        self.info.insert("end", details)

        payments = database.payment_history(int(sid))

        if payments:

            for pay in payments:

                self.history.insert(
                    "end",
                    f"{pay['payment_date']}    ₹{pay['amount']}\n"
                )

        else:

            self.history.insert(
                "end",
                "No payment history found."
            )

    def collect_fee(self):

        sid = self.student_id.get().strip()

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter Student ID."
            )
            return

        try:

            amount = float(self.amount.get())

            if amount <= 0:

                messagebox.showerror(
                    "Error",
                    "Enter a valid amount."
                )
                return

            success = database.pay_fee(
                int(sid),
                amount
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Fee Collected Successfully."
                )

                self.amount.delete(0,"end")

                self.search_student()

                if isinstance(self.master, Dashboard):
                    self.master.show_welcome()

            else:
    
                messagebox.showerror(
                    "Error",
                    "Payment failed."
                )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Amount must be numeric."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )
class AttendanceWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Attendance")
        self.geometry("700x600")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Attendance Management",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        self.student_id = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Student ID"
        )
        self.student_id.pack(pady=8)

        self.status = ctk.CTkComboBox(
            self,
            values=["Present","Absent"]
        )
        self.status.set("Present")
        self.status.pack(pady=8)

        ctk.CTkButton(
            self,
            text="Mark Attendance",
            command=self.mark_attendance
        ).pack(pady=10)

        ctk.CTkLabel(
            self,
            text="Attendance Records",
            font=("Arial",18,"bold")
        ).pack(pady=(15,5))

        self.records = ctk.CTkTextbox(
            self,
            width=620,
            height=320
        )

        self.records.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Load Attendance",
            command=self.load_attendance
        ).pack()

    def mark_attendance(self):

        sid = self.student_id.get().strip()

        if not sid.isdigit():

            messagebox.showerror(
                "Error",
                "Enter Student ID."
            )
            return

        success = database.mark_attendance(
            int(sid),
            self.status.get()
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Attendance Marked."
            )

            self.load_attendance()

        else:

            messagebox.showerror(
                "Error",
                "Attendance already marked or student not found."
            )

    def load_attendance(self):

        self.records.delete("1.0","end")

        sid = self.student_id.get().strip()

        if not sid.isdigit():
            return

        rows = database.get_attendance(
            int(sid)
        )

        if not rows:

            self.records.insert(
                "end",
                "No attendance records."
            )
            return

        percent = database.attendance_percentage(
            int(sid)
        )

        self.records.insert(
            "end",
            f"Attendance Percentage : {percent}%\n\n"
        )

        for row in rows:

            self.records.insert(
                "end",
                f"{row['date']}      {row['status']}\n"
            )


class ReportsWindow(ctk.CTkToplevel):

    def __init__(self,parent):

        super().__init__(parent)

        self.title("Reports")
        self.geometry("900x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Reports",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(fill="x",padx=10,pady=10)

        ctk.CTkButton(
            top,
            text="Student Report",
            command=self.student_report
        ).pack(side="left",padx=5)

        ctk.CTkButton(
            top,
            text="Fee Report",
            command=self.fee_report
        ).pack(side="left",padx=5)

        ctk.CTkButton(
            top,
            text="Attendance Report",
            command=self.attendance_report
        ).pack(side="left",padx=5)

        self.report = ctk.CTkTextbox(
            self,
            width=850,
            height=520,
            font=("Consolas",13)
        )

        self.report.pack(padx=10,pady=10)

    def student_report(self):

        self.report.delete("1.0","end")

        rows = database.student_report()

        self.report.insert(
            "end",
            "ID\tNAME\tCOURSE\tBATCH\tMOBILE\n"
        )

        self.report.insert(
            "end",
            "-"*80+"\n"
        )

        for row in rows:

            self.report.insert(
                "end",
                f"{row['student_id']}\t"
                f"{row['full_name']}\t"
                f"{row['course']}\t"
                f"{row['batch']}\t"
                f"{row['mobile']}\n"
            )

    def fee_report(self):

        self.report.delete("1.0","end")

        rows = database.fee_report()

        self.report.insert(
            "end",
            "ID\tNAME\tTOTAL\tPAID\tBALANCE\n"
        )

        self.report.insert(
            "end",
            "-"*80+"\n"
        )

        for row in rows:

            self.report.insert(
                "end",
                f"{row['student_id']}\t"
                f"{row['full_name']}\t"
                f"{row['course_fee']}\t"
                f"{row['fee_paid']}\t"
                f"{row['balance_fee']}\n"
            )

    def attendance_report(self):

        self.report.delete("1.0","end")

        rows = database.attendance_report()

        self.report.insert(
            "end",
            "ID\tNAME\tDATE\tSTATUS\n"
        )

        self.report.insert(
            "end",
            "-"*80+"\n"
        )

        for row in rows:

            self.report.insert(
                "end",
                f"{row['student_id']}\t"
                f"{row['full_name']}\t"
                f"{row['date']}\t"
                f"{row['status']}\n"
            )

    def logout(self):

        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        ):

            database.add_log("Administrator Logged Out")

            self.destroy()

            LoginWindow().mainloop()
class BatchManagement(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Batch Management")
        self.geometry("750x550")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Batch Management",
            font=("Arial",24,"bold")
        ).pack(pady=15)

        self.batch = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Batch Name"
        )
        self.batch.pack(pady=8)

        self.timing = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Timing (e.g. 10 AM - 12 PM)"
        )
        self.timing.pack(pady=8)

        self.course = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Course Name"
        )
        self.course.pack(pady=8)

        btn = ctk.CTkFrame(self)
        btn.pack(pady=10)

        ctk.CTkButton(
            btn,
            text="Add Batch",
            command=self.add_batch
        ).grid(row=0,column=0,padx=5)

        ctk.CTkButton(
            btn,
            text="Refresh",
            command=self.load_batches
        ).grid(row=0,column=1,padx=5)

        columns = ("ID","Batch","Timing","Course")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )

        widths = [70,180,220,200]

        for col,width in zip(columns,widths):

            self.tree.heading(col,text=col)
            self.tree.column(col,width=width,anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.fill_entries
        )

        self.load_batches()

    def load_batches(self):

        self.tree.delete(*self.tree.get_children())

        rows = database.get_batches()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["batch_id"],
                    row["batch_name"],
                    row["timing"],
                    row["course_name"]
                )
            )

    def add_batch(self):

        batch = self.batch.get().strip()
        timing = self.timing.get().strip()
        course = self.course.get().strip()

        if batch == "" or course == "":

            messagebox.showerror(
                "Error",
                "Batch Name and Course Name are required."
            )
            return

        try:

            database.add_batch(
                batch,
                timing,
                course
            )

            messagebox.showinfo(
                "Success",
                "Batch Added Successfully."
            )

            self.clear()
            self.load_batches()

            if isinstance(self.master, Dashboard):
                self.master.show_welcome()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def fill_entries(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.batch.delete(0,"end")
        self.batch.insert(0,values[1])

        self.timing.delete(0,"end")
        self.timing.insert(0,values[2])

        self.course.delete(0,"end")
        self.course.insert(0,values[3])

    def clear(self):

        self.batch.delete(0,"end")
        self.timing.delete(0,"end")
        self.course.delete(0,"end")
        

if __name__ == "__main__":

    app = LoginWindow()

    app.mainloop()
