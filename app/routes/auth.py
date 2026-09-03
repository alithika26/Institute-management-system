from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
)

from flask_bcrypt import Bcrypt

from app.extensions import db
from app.models import Student, StudentPerformance
from app.forms import (
    StudentRegistrationForm,
    StudentLoginForm,
)


auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth.route("/student/register", methods=["GET", "POST"])
def student_register():
    form = StudentRegistrationForm()

    if form.validate_on_submit():

        existing_student = Student.query.filter_by(
            roll_no=form.roll_no.data
        ).first()

        if existing_student:
            flash(
                "A student with this roll number already exists.",
                "danger",
            )

            return render_template(
                "student_register.html",
                form=form,
            )

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

        flash(
            "Registration successful. Please log in.",
            "success",
        )

        return redirect(url_for("auth.student_login"))

    return render_template(
        "student_register.html",
        form=form,
    )


@auth.route("/student/login", methods=["GET", "POST"])
def student_login():
    form = StudentLoginForm()

    if form.validate_on_submit():

        student = Student.query.filter_by(
            roll_no=form.roll_no.data
        ).first()

        if student and bcrypt.check_password_hash(
            student.password,
            form.password.data,
        ):
            session["student_roll_no"] = student.roll_no

            return redirect(
                url_for("auth.student_dashboard")
            )

        flash(
            "Invalid roll number or password.",
            "danger",
        )

    return render_template(
        "student_login.html",
        form=form,
    )


@auth.route("/student/dashboard")
def student_dashboard():

    roll_no = session.get("student_roll_no")

    if not roll_no:
        return redirect(
            url_for("auth.student_login")
        )

    student = Student.query.filter_by(
        roll_no=roll_no
    ).first()

    if not student:
        session.pop("student_roll_no", None)

        return redirect(
            url_for("auth.student_login")
        )

    performances = StudentPerformance.query.filter_by(
        student_id=student.roll_no
    ).all()

    return render_template(
        "student_dashboard.html",
        student=student,
        performances=performances,
    )


@auth.route("/student/logout")
def student_logout():

    session.pop("student_roll_no", None)

    return redirect(
        url_for("auth.student_login")
    )