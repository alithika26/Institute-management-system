from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    SubmitField,
    SelectField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
)


# =========================
# STUDENT FORMS
# =========================

class StudentRegistrationForm(FlaskForm):

    roll_no = StringField(
        "Roll Number",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    programme = StringField(
        "Programme",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    branch = StringField(
        "Branch",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    semester = IntegerField(
        "Semester",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=12),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=100),
        ],
    )

    submit = SubmitField("Register")


class StudentLoginForm(FlaskForm):

    roll_no = StringField(
        "Roll Number",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Login")


class StudentEditForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    programme = StringField(
        "Programme",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    branch = StringField(
        "Branch",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    semester = IntegerField(
        "Semester",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=12),
        ],
    )

    submit = SubmitField("Update Student")


# =========================
# FACULTY FORMS
# =========================

class FacultyRegistrationForm(FlaskForm):

    fac_code = StringField(
        "Faculty Code",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    room_no = StringField(
        "Room Number",
        validators=[
            Length(max=50),
        ],
    )

    phone_no = StringField(
        "Phone Number",
        validators=[
            Length(max=50),
        ],
    )

    email_id = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=100),
        ],
    )

    office = StringField(
        "Office",
        validators=[
            Length(max=100),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=100),
        ],
    )

    submit = SubmitField("Register")


class FacultyLoginForm(FlaskForm):

    fac_code = StringField(
        "Faculty Code",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Login")


class FacultyEditForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    room_no = StringField(
        "Room Number",
        validators=[
            Length(max=50),
        ],
    )

    phone_no = StringField(
        "Phone Number",
        validators=[
            Length(max=50),
        ],
    )

    email_id = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=100),
        ],
    )

    office = StringField(
        "Office",
        validators=[
            Length(max=100),
        ],
    )

    submit = SubmitField("Update Faculty")


# =========================
# ADMIN FORMS
# =========================

class AdminLoginForm(FlaskForm):

    name = StringField(
        "Admin Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Login")


# =========================
# COURSE FORM
# =========================

class CourseForm(FlaskForm):

    code = StringField(
        "Course Code",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    name = StringField(
        "Course Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    programme = StringField(
        "Programme",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    branch = StringField(
        "Branch",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    semester = IntegerField(
        "Semester",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=12),
        ],
    )

    faculty_code = SelectField(
        "Assign Faculty",
        choices=[],
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Create Course")


# =========================
# ENROLLMENT FORM
# =========================

class EnrollmentForm(FlaskForm):

    student_id = SelectField(
        "Student",
        choices=[],
        validators=[
            DataRequired(),
        ],
    )

    course_code = SelectField(
        "Course",
        choices=[],
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Enroll Student")


# =========================
# PERFORMANCE FORM
# =========================

class PerformanceForm(FlaskForm):

    quiz1_marks = IntegerField(
        "Quiz 1 Marks",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    midsem_marks = IntegerField(
        "Midsem Marks",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    quiz2_marks = IntegerField(
        "Quiz 2 Marks",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    lab_test_marks = IntegerField(
        "Lab Test Marks",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    endsem_marks = IntegerField(
        "Endsem Marks",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    attendance_in_perc = IntegerField(
        "Attendance (%)",
        validators=[
            NumberRange(min=0, max=100),
        ],
    )

    submit = SubmitField("Save Performance")


# =========================
# PROGRAMME FORM
# =========================

class ProgrammeForm(FlaskForm):

    programme = StringField(
        "Programme",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    branch = StringField(
        "Branch",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    no_of_students = IntegerField(
        "Number of Students",
        validators=[
            DataRequired(),
            NumberRange(min=0),
        ],
    )

    total_no_of_sem = IntegerField(
        "Total Number of Semesters",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=20),
        ],
    )

    submit = SubmitField("Add Programme")