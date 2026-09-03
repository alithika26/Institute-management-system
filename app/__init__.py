from flask import Flask, render_template

from app.extensions import db
from config import Config


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app import models

    from app.routes.auth import auth
    from app.routes.faculty import faculty_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app