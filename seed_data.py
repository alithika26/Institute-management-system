from app import create_app
from app.extensions import db
from app.models import Student, Course, StudentPerformance


app = create_app()


with app.app_context():

    student = Student.query.filter_by(
        roll_no="STU001"
    ).first()

    if not student:
        print("STU001 not found. Register the student first.")
        exit()

    course = Course.query.filter_by(
        code="CS101"
    ).first()

    if not course:
        course = Course(
            code="CS101",
            name="Introduction to Computer Science",
            programme="BTech",
            branch="IT",
            semester=6,
        )

        db.session.add(course)
        db.session.commit()

    performance = StudentPerformance.query.filter_by(
        student_id=student.roll_no,
        course_code=course.code,
    ).first()

    if not performance:
        performance = StudentPerformance(
            student_id=student.roll_no,
            course_code=course.code,
            quiz1_marks=8,
            midsem_marks=22,
            quiz2_marks=9,
            endsem_marks=42,
            lab_test_marks=18,
            attendance_in_perc=88,
        )

        db.session.add(performance)
        db.session.commit()

        print("Sample performance data added.")

    else:
        print("Performance data already exists.")