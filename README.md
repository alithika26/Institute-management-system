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
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///institute.db
ADMIN_PASSWORD=your-admin-password
```

### 6. Initialize the database

```bash
python init_db.py
```

### 7. Add sample data

```bash
python seed_data.py
```

### 8. Create the admin account

```bash-
python seed_admin.py
```

### 9. Run the application

```bash
python run.py
```

Open `http://127.0.0.1:5000` in your browser.

## Application Roles

| Role | Main Responsibilities |
|------|------------------------|
| Student | View courses, marks and attendance |
| Faculty | Manage assigned courses and student performance |
| Admin | Manage students, faculty, programmes, courses and enrollments |

## Security

- Passwords are stored using password hashing.
- Sensitive configuration values are managed through environment variables.
- Database files and local environment files are excluded from version control.

## Future Improvements

- REST API integration
- Advanced reporting and analytics
- Email notifications
- Improved deployment configuration
- Automated testing
## Author

**Alithika**

Built as a full-stack academic management application using Flask.

