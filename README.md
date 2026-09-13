# Institute-management-system

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![UI Library](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A desktop Enterprise Resource Planning (ERP) application engineered in **Python** using **CustomTkinter** for modern desktop interfaces and **SQLite3** for persistent relational data management[cite: 3, 4]. The software centralizes admissions, course configurations, batch timetables, installment billing, and attendance tracking into an administrative platform[cite: 3, 4].
---
## 📸 Screenshots

| Administrator Dashboard | Student Records View |
| :---: | :---: |
| *(Add your dashboard screenshot here)* | *(Add your student treeview screenshot here)* |
---
## ✨ Features

### 🔐 Administrative Authentication
* Single-entry admin login with attempt limiting (locks after 3 failed attempts)[cite: 4].
* System audit logging capturing login timestamps and failures[cite: 3, 4].

### 👨‍🎓 Student Information Management
* Comprehensive student onboarding: capture contact details, course selection, batch allocations, and fee commitments[cite: 3, 4].
* Real-time search by Student ID or 10-digit mobile number[cite: 3, 4].
* Interactive `Treeview` interface with live filtering by name, mobile, or course[cite: 4].
* Update and delete workflows with defensive dialog confirmations[cite: 4].

### 📚 Course & Batch Scheduling
* Course catalog management (duration and base fee structure)[cite: 3, 4].
* Batch management with timing slots mapped to active courses[cite: 3, 4].
* Student batch assignment workflows[cite: 3, 4].

### 💰 Fee Management & Installment Ledger
* Dynamic financial ledger that recalculates `fee_paid` and `balance_fee` with every transaction.
* Validation controls preventing negative payments or overpayments exceeding total course fees[cite: 3, 4].
* Complete chronological installment history per student[cite: 3, 4].

### 📅 Attendance Tracking
* Daily attendance logger with duplicate prevention (restricts marking a student more than once per day)[cite: 3, 4].
* Real-time calculation of overall attendance percentage[cite: 3, 4].
* Chronological student-level attendance logs[cite: 3, 4].

### 📊 System Reporting & Audit Logs
* Tabular export views for student directories, fee balances, and attendance records[cite: 4].
* Persistent audit log table documenting administrative transactions and system events.

---

## 🛠️ Architecture & Tech Stack

The application uses a decoupled two-tier architecture:
* **Frontend / Presentation Layer (`main.py`):** Structured with Object-Oriented Programming (OOP) using `CustomTkinter` and `ttk.Treeview`[cite: 4].
* **Backend / Persistence Layer (`database.py`):** Direct SQLite data-access layer configured with foreign key enforcement (`PRAGMA foreign_keys = ON`).

### Database Schema

```mermaid
erDiagram
    admin {
        TEXT username PK
        TEXT password
    }
    students {
        INTEGER student_id PK
        TEXT full_name
        TEXT mobile UK
        TEXT course
        TEXT batch
        REAL course_fee
        REAL fee_paid
        REAL balance_fee
    }
    courses {
        INTEGER course_id PK
        TEXT course_name UK
        TEXT duration
        REAL fees
    }
    batches {
        INTEGER batch_id PK
        TEXT batch_name
        TEXT timing
        TEXT course_name
    }
    attendance {
        INTEGER attendance_id PK
        INTEGER student_id FK
        TEXT date
        TEXT status
    }
    fee_payments {
        INTEGER payment_id PK
        INTEGER student_id FK
        TEXT payment_date
        REAL amount
    }
    logs {
        INTEGER log_id PK
        TEXT activity
        TEXT log_time
    }

    students ||--o{ attendance : "has"
    students ||--o{ fee_payments : "makes"
