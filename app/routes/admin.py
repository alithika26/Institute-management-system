from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db, bcrypt
from app.models import (
    Admin,
    Course,
    Faculty,
    FacultyCourse,
    Programme,
    Student,
    StudentCourse,
    StudentPerformance,
)
from app.forms import (
    AdminLoginForm,
    CourseForm,
    EnrollmentForm,
    StudentRegistrationForm,
    StudentEditForm,
    FacultyRegistrationForm,
    FacultyEditForm,
    ProgrammeForm,
)

admin_bp = Blueprint("admin", __name__)


# =========================
# ADMIN LOGIN
# =========================

@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data).first()

        if admin and bcrypt.check_password_hash(
            admin.password, form.password.data
        ):
            session["admin_name"] = admin.name
            flash("Admin login successful.", "success")
            return redirect(url_for("admin.admin_dashboard"))

        flash("Invalid admin credentials.", "danger")

    return render_template("admin_login.html", form=form)


# =========================
# ADMIN DASHBOARD
# =========================

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    student_count = Student.query.count()
    faculty_count = Faculty.query.count()
    course_count = Course.query.count()

    return render_template(
        "admin_dashboard.html",
        admin_name=admin_name,
        student_count=student_count,
        faculty_count=faculty_count,
        course_count=course_count,
    )


# =========================
# COURSE MANAGEMENT
# =========================

@admin_bp.route("/admin/courses", methods=["GET", "POST"])
def manage_courses():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    form = CourseForm()

    if form.validate_on_submit():
        existing_course = Course.query.filter_by(
            code=form.code.data
        ).first()

        if existing_course:
            flash("A course with this code already exists.", "danger")
        else:
            course = Course(
                code=form.code.data,
                name=form.name.data,
                programme=form.programme.data,
                branch=form.branch.data,
                semester=form.semester.data,
            )

            db.session.add(course)
            db.session.commit()

            flash("Course added successfully.", "success")
            return redirect(url_for("admin.manage_courses"))

    courses = Course.query.order_by(Course.code).all()

    return render_template(
        "admin_courses.html",
        form=form,
        courses=courses,
    )


# =========================
# ENROLLMENT MANAGEMENT
# =========================

@admin_bp.route("/admin/enrollments", methods=["GET", "POST"])
def manage_enrollments():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    form = EnrollmentForm()

    form.student_id.choices = [
        (student.roll_no, f"{student.roll_no} - {student.name}")
        for student in Student.query.order_by(Student.roll_no).all()
    ]

    form.course_code.choices = [
        (course.code, f"{course.code} - {course.name}")
        for course in Course.query.order_by(Course.code).all()
    ]

    if form.validate_on_submit():
        existing_enrollment = StudentCourse.query.filter_by(
            student_id=form.student_id.data,
            course_code=form.course_code.data,
        ).first()

        if existing_enrollment:
            flash("Student is already enrolled in this course.", "danger")
        else:
            enrollment = StudentCourse(
                student_id=form.student_id.data,
                course_code=form.course_code.data,
            )

            db.session.add(enrollment)
            db.session.commit()

            flash("Student enrolled successfully.", "success")
            return redirect(url_for("admin.manage_enrollments"))

    enrollments = StudentCourse.query.all()

    return render_template(
        "admin_enrollments.html",
        form=form,
        enrollments=enrollments,
    )


# =========================
# STUDENT MANAGEMENT
# =========================

@admin_bp.route("/admin/students", methods=["GET", "POST"])
def manage_students():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    form = StudentRegistrationForm()

    if form.validate_on_submit():
        existing_student = Student.query.filter_by(
            roll_no=form.roll_no.data
        ).first()

        if existing_student:
            flash("A student with this roll number already exists.", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")

            student = Student(
                roll_no=form.roll_no.data,
                name=form.name.data,
                programme=form.programme.data,
                branch=form.branch.data,
                semester=form.semester.data,
                password=hashed_password,
            )

            db.session.add(student)
            db.session.commit()

            flash("Student added successfully.", "success")
            return redirect(url_for("admin.manage_students"))

    students = Student.query.order_by(Student.roll_no).all()

    return render_template(
        "admin_students.html",
        form=form,
        students=students,
    )


# =========================
# EDIT STUDENT
# =========================

@admin_bp.route("/admin/students/<roll_no>/edit", methods=["GET", "POST"])
def edit_student(roll_no):
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    student = Student.query.filter_by(roll_no=roll_no).first_or_404()

    form = StudentEditForm(obj=student)

    if form.validate_on_submit():
        student.name = form.name.data
        student.programme = form.programme.data
        student.branch = form.branch.data
        student.semester = form.semester.data

        db.session.commit()

        flash("Student updated successfully.", "success")
        return redirect(url_for("admin.manage_students"))

    return render_template(
        "edit_student.html",
        form=form,
        student=student,
    )


# =========================
# DELETE STUDENT
# =========================

@admin_bp.route("/admin/students/<roll_no>/delete", methods=["POST"])
def delete_student(roll_no):
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    student = Student.query.filter_by(roll_no=roll_no).first_or_404()

    StudentCourse.query.filter_by(
        student_id=student.roll_no
    ).delete(synchronize_session=False)

    StudentPerformance.query.filter_by(
        student_id=student.roll_no
    ).delete(synchronize_session=False)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully.", "success")

    return redirect(url_for("admin.manage_students"))


# =========================
# FACULTY MANAGEMENT
# =========================

@admin_bp.route("/admin/faculty", methods=["GET", "POST"])
def manage_faculty():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    form = FacultyRegistrationForm()

    if form.validate_on_submit():
        existing_faculty = Faculty.query.filter_by(
            fac_code=form.fac_code.data
        ).first()

        if existing_faculty:
            flash(
                "A faculty member with this code already exists.",
                "danger",
            )
        else:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")

            faculty = Faculty(
                fac_code=form.fac_code.data,
                name=form.name.data,
                room_no=form.room_no.data,
                phone_no=form.phone_no.data,
                email_id=form.email_id.data,
                office=form.office.data,
                password=hashed_password,
            )

            db.session.add(faculty)
            db.session.commit()

            flash("Faculty added successfully.", "success")

            return redirect(url_for("admin.manage_faculty"))

    faculty_members = Faculty.query.order_by(Faculty.fac_code).all()

    return render_template(
        "admin_faculty.html",
        form=form,
        faculty_members=faculty_members,
    )


# =========================
# EDIT FACULTY
# =========================

@admin_bp.route("/admin/faculty/<fac_code>/edit", methods=["GET", "POST"])
def edit_faculty(fac_code):
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    faculty = Faculty.query.filter_by(
        fac_code=fac_code
    ).first_or_404()

    form = FacultyEditForm(obj=faculty)

    if form.validate_on_submit():
        faculty.name = form.name.data
        faculty.room_no = form.room_no.data
        faculty.phone_no = form.phone_no.data
        faculty.email_id = form.email_id.data
        faculty.office = form.office.data

        db.session.commit()

        flash("Faculty updated successfully.", "success")

        return redirect(url_for("admin.manage_faculty"))

    return render_template(
        "edit_faculty.html",
        form=form,
        faculty=faculty,
    )


# =========================
# DELETE FACULTY
# =========================

@admin_bp.route("/admin/faculty/<fac_code>/delete", methods=["POST"])
def delete_faculty(fac_code):
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    faculty = Faculty.query.filter_by(
        fac_code=fac_code
    ).first_or_404()

    FacultyCourse.query.filter_by(
        fac_code=faculty.fac_code
    ).delete(synchronize_session=False)

    db.session.delete(faculty)
    db.session.commit()

    flash("Faculty deleted successfully.", "success")

    return redirect(url_for("admin.manage_faculty"))

# =========================
# PROGRAMME MANAGEMENT
# =========================

@admin_bp.route("/admin/programmes", methods=["GET", "POST"])
def manage_programmes():
    admin_name = session.get("admin_name")

    if not admin_name:
        return redirect(url_for("admin.admin_login"))

    form = ProgrammeForm()

    if form.validate_on_submit():
        existing_programme = Programme.query.filter_by(
            programme=form.programme.data,
            branch=form.branch.data,
        ).first()

        if existing_programme:
            flash(
                "This programme and branch already exists.",
                "danger",
            )
        else:
            programme = Programme(
                programme=form.programme.data,
                branch=form.branch.data,
                no_of_students=form.no_of_students.data,
                total_no_of_sem=form.total_no_of_sem.data,
            )

            db.session.add(programme)
            db.session.commit()

            flash("Programme added successfully.", "success")

            return redirect(url_for("admin.manage_programmes"))

    programmes = Programme.query.order_by(
        Programme.programme,
        Programme.branch,
    ).all()

    return render_template(
        "admin_programmes.html",
        form=form,
        programmes=programmes,
    )


# =========================
# ADMIN LOGOUT
# =========================

@admin_bp.route("/admin/logout")
def admin_logout():
    session.pop("admin_name", None)

    flash("Admin logged out successfully.", "success")

    return redirect(url_for("admin.admin_login"))