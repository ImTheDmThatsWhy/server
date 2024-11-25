from flask import Blueprint, request
from init import db
from models.teacher import Teacher, teachers_schema, teacher_schema

teachers_bp= Blueprint("teachers",__name__,url_prefix="/teachers")

@teachers_bp.route("/")
def get_teachers():
    stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt)
    data=teachers_schema.dump(teachers_list)
    return data

@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher=db.session.scalar(stmt)
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404

teachers_bp.route("/", methods=["POST"])
def create_teacher():
    body_data = request.get_json()
    new_teacher = Teacher(
        name=body_data.get("name"),
       department=body_data.get("department"),
       address=body_data.get("address"),
    )
    db.session.add(new_teacher)
    db.session.commit()
    return teacher_schema.dump(new_teacher), 201
