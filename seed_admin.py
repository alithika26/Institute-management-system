import os

from app import create_app
from app.extensions import db
from app.models import Admin
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


load_dotenv()

app = create_app()
bcrypt = Bcrypt()

admin_password = os.getenv("ADMIN_PASSWORD")

if not admin_password:
    print("ADMIN_PASSWORD is not set in the .env file.")
    raise SystemExit(1)


with app.app_context():

    existing_admin = Admin.query.filter_by(
        name="admin"
    ).first()

    if existing_admin:

        print("Admin already exists.")

    else:

        hashed_password = bcrypt.generate_password_hash(
            admin_password
        ).decode("utf-8")

        admin = Admin(
            name="admin",
            password=hashed_password,
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin account created.")