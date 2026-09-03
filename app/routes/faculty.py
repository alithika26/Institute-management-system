from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
)

from flask_bcrypt import Bcrypt

from app.extensions import db

from app.models import (
    Faculty,
    FacultyCourse,
    StudentCourse,
    StudentPerformance,
)

from app.forms import (
    FacultyRegistrationForm,
    FacultyLoginForm,
    PerformanceForm,
)


faculty_bp = Blueprint("faculty", __name__)
bcrypt = Bcrypt()


# =========================
# FACULTY REGISTRATION
# =========================

@faculty_bp.route(
    "/faculty/register",
    methods=["GET", "POST"]
)
def faculty_register():

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

            return render_template(
                "faculty_register.html",
                form=form,
            )

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

        flash(
            "Faculty registration successful.",
            "success",
        )

        return redirect(
            url_for("faculty.faculty_login")
        )

    return render_template(
        "faculty_register.html",
        form=form,
    )


# =========================
# FACULTY LOGIN
# =========================

@faculty_bp.route(
    "/faculty/login",
    methods=["GET", "POST"]
)
def faculty_login():

    form = FacultyLoginForm()

    if form.validate_on_submit():

        faculty = Faculty.query.filter_by(
            fac_code=form.fac_code.data
        ).first()

        if faculty and bcrypt.check_password_hash(
            faculty.password,
            form.password.data,
        ):

            session["faculty_code"] = faculty.fac_code

            return redirect(
                url_for("faculty.faculty_dashboard")
            )

        flash(
            "Invalid faculty code or password.",
            "danger",
        )

    return render_template(
        "faculty_login.html",
        form=form,
    )


# =========================
# FACULTY DASHBOARD
# =========================

@faculty_bp.route("/faculty/dashboard")
def faculty_dashboard():

    fac_code = session.get("faculty_code")

    if not fac_code:

        return redirect(
            url_for("faculty.faculty_login")
        )

    faculty = Faculty.query.filter_by(
        fac_code=fac_code
    ).first()

    if not faculty:

        session.pop("faculty_code", None)

        return redirect(
            url_for("faculty.faculty_login")
        )

    assignments = FacultyCourse.query.filter_by(
        fac_code=faculty.fac_code
    ).all()

    return render_template(
        "faculty_dashboard.html",
        faculty=faculty,
        assignments=assignments,
    )


# =========================
# VIEW COURSE STUDENTS
# =========================

@faculty_bp.route(
    "/faculty/course/<course_code>"
)
def faculty_course(course_code):

    fac_code = session.get("faculty_code")

    if not fac_code:

        return redirect(
            url_for("faculty.faculty_login")
        )

    faculty = Faculty.query.filter_by(
        fac_code=fac_code
    ).first()

    if not faculty:

        session.pop("faculty_code", None)

        return redirect(
            url_for("faculty.faculty_login")
        )

    assignment = FacultyCourse.query.filter_by(
        fac_code=faculty.fac_code,
        course_code=course_code,
    ).first()

    if not assignment:

        flash(
            "You are not assigned to this course.",
            "danger",
        )

        return redirect(
            url_for("faculty.faculty_dashboard")
        )

    enrollments = StudentCourse.query.filter_by(
        course_code=course_code
    ).all()

    return render_template(
        "faculty_course.html",
        faculty=faculty,
        course=assignment.course,
        enrollments=enrollments,
    )


# =========================
# ENTER / UPDATE PERFORMANCE
# =========================

@faculty_bp.route(
    "/faculty/course/<course_code>/student/<student_id>/performance",
    methods=["GET", "POST"]
)
def student_performance(
    course_code,
    student_id,
):

    fac_code = session.get("faculty_code")

    if not fac_code:

        return redirect(
            url_for("faculty.faculty_login")
        )

    faculty = Faculty.query.filter_by(
        fac_code=fac_code
    ).first()

    if not faculty:

        session.pop("faculty_code", None)

        return redirect(
            url_for("faculty.faculty_login")
        )

    # Check faculty assignment
    assignment = FacultyCourse.query.filter_by(
        fac_code=faculty.fac_code,
        course_code=course_code,
    ).first()

    if not assignment:

        flash(
            "You are not assigned to this course.",
            "danger",
        )

        return redirect(
            url_for("faculty.faculty_dashboard")
        )

    # Check student enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=student_id,
        course_code=course_code,
    ).first()

    if not enrollment:

        flash(
            "This student is not enrolled in this course.",
            "danger",
        )

        return redirect(
            url_for(
                "faculty.faculty_course",
                course_code=course_code,
            )
        )

    student = enrollment.student
    course = enrollment.course

    # Look for existing performance record
    performance = StudentPerformance.query.filter_by(
        student_id=student_id,
        course_code=course_code,
    ).first()

    form = PerformanceForm()

    # Fill form with existing values
    if request.method == "GET" and performance:

        form.quiz1_marks.data = performance.quiz1_marks
        form.midsem_marks.data = performance.midsem_marks
        form.quiz2_marks.data = performance.quiz2_marks
        form.lab_test_marks.data = performance.lab_test_marks
        form.endsem_marks.data = performance.endsem_marks
        form.attendance_in_perc.data = (
            performance.attendance_in_perc
        )

    if form.validate_on_submit():

        if not performance:

            performance = StudentPerformance(
                student_id=student_id,
                course_code=course_code,
            )

            db.session.add(performance)

        performance.quiz1_marks = form.quiz1_marks.data
        performance.midsem_marks = form.midsem_marks.data
        performance.quiz2_marks = form.quiz2_marks.data
        performance.lab_test_marks = form.lab_test_marks.data
        performance.endsem_marks = form.endsem_marks.data
        performance.attendance_in_perc = (
            form.attendance_in_perc.data
        )

        db.session.commit()

        flash(
            "Student performance saved successfully.",
            "success",
        )

        return redirect(
            url_for(
                "faculty.student_performance",
                course_code=course_code,
                student_id=student_id,
            )
        )

    return render_template(
        "student_performance.html",
        form=form,
        faculty=faculty,
        student=student,
        course=course,
        performance=performance,
    )


# =========================
# FACULTY LOGOUT
# =========================

@faculty_bp.route("/faculty/logout")
def faculty_logout():

    session.pop("faculty_code", None)

    return redirect(
        url_for("faculty.faculty_login")
    )