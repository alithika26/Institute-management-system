# Institute Management System

A web-based Institute Management System built with Flask to manage students, faculty, courses, enrollments, and academic performance through role-based access.

## Features

### 👨‍🎓 Student
- Student registration and login
- View personal academic information
- View enrolled courses
- View course-wise performance
- View attendance and marks

### 👨‍🏫 Faculty
- Faculty registration and login
- View assigned courses
- View enrolled students
- Enter and update student performance
- Manage academic records

### 👨‍💼 Admin
- Admin authentication
- Manage students
- Manage faculty
- Manage programmes
- Manage courses
- Manage student enrollments

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy
- **Authentication & Security:** Flask-Bcrypt
- **Forms:** Flask-WTF, WTForms
- **Frontend:** HTML, CSS
- **Configuration:** python-dotenv

## Project Structure

```text
institute-management-system/
│
├── app/
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── faculty.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   ├── extensions.py
│   ├── forms.py
│   └── models.py
│
├── config.py
├── init_db.py
├── seed_admin.py
├── seed_data.py
├── run.py
├── .env.example
└── .gitignore
## Installation

### 1. Clone the repository

```bash
git clone https://github.com/alithika26/Institute-management-system.git
cd Institute-management-system
