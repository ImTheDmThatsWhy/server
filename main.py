import os
from flask import Flask
from init import db, ma
from flask import Blueprint
from controllers.cli_controller import db_commands
from controllers.student_controller import students_bp
from controllers.teachers_controller import teachers_bp
from controllers.course_controllers import courses_bp
#example of an app factory
def create_app():
    app= Flask(__name__)
    print("server begins")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(db_commands)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    return app






