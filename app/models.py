from app.extensions import db


class Student(db.Model):
    __tablename__ = "Student_Tab"

    roll_no = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    performance = db.relationship(
        "StudentPerformance",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class Faculty(db.Model):
    __tablename__ = "Faculty_Tab"

    fac_code = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room_no = db.Column(db.String(50))
    phone_no = db.Column(db.String(50))
    email_id = db.Column(db.String(100))
    office = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)

    courses = db.relationship(
        "FacultyCourse",
        back_populates="faculty",
        cascade="all, delete-orphan"
    )


class Admin(db.Model):
    __tablename__ = "Admin_Tab"

    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(255), nullable=False)


class Programme(db.Model):
    __tablename__ = "Programme_Tab"

    programme = db.Column(db.String(100), primary_key=True)
    branch = db.Column(db.String(100), primary_key=True)
    no_of_students = db.Column(db.Integer, default=0)
    total_no_of_sem = db.Column(db.Integer, nullable=False)


class Course(db.Model):
    __tablename__ = "Course_Tab"

    code = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    faculty = db.relationship(
        "FacultyCourse",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    performance = db.relationship(
        "StudentPerformance",
        back_populates="course",
        cascade="all, delete-orphan"
    )


class FacultyCourse(db.Model):
    __tablename__ = "Fac_Course_Tab"

    fac_code = db.Column(
        db.String(50),
        db.ForeignKey("Faculty_Tab.fac_code"),
        primary_key=True
    )

    course_code = db.Column(
        db.String(50),
        db.ForeignKey("Course_Tab.code"),
        primary_key=True
    )

    faculty = db.relationship(
        "Faculty",
        back_populates="courses"
    )

    course = db.relationship(
        "Course",
        back_populates="faculty"
    )


class StudentPerformance(db.Model):
    __tablename__ = "Stud_Perf_Tab"

    student_id = db.Column(
        db.String(50),
        db.ForeignKey("Student_Tab.roll_no"),
        primary_key=True
    )

    course_code = db.Column(
        db.String(50),
        db.ForeignKey("Course_Tab.code"),
        primary_key=True
    )

    quiz1_marks = db.Column(db.Float)
    midsem_marks = db.Column(db.Float)
    quiz2_marks = db.Column(db.Float)
    endsem_marks = db.Column(db.Float)
    lab_test_marks = db.Column(db.Float)
    attendance_in_perc = db.Column(db.Float)

    student = db.relationship(
        "Student",
        back_populates="performance"
    )

    course = db.relationship(
        "Course",
        back_populates="performance"
    )


class StudentCourse(db.Model):
    __tablename__ = "Stud_Course_Tab"

    student_id = db.Column(
        db.String(50),
        db.ForeignKey("Student_Tab.roll_no"),
        primary_key=True
    )

    course_code = db.Column(
        db.String(50),
        db.ForeignKey("Course_Tab.code"),
        primary_key=True
    )

    student = db.relationship(
        "Student",
        backref="enrolled_courses"
    )

    course = db.relationship(
        "Course",
        backref="enrolled_students"
    )