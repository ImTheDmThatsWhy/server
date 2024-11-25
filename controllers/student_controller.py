from flask import Blueprint, request
from init import db 
from models.student import Student, students_schema, student_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
students_bp= Blueprint("students",__name__,url_prefix="/students")

@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    return data 
@students_bp.route("/<int:student_id>")
def get_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        data = student_schema.dump(student)
        return data
    else:
        return {"message":f"Studnet with id {student_id} does not exist"}, 404

@students_bp.route("/", methods=["POST"])
def create_student():
    try:
        #get info from request body
        body_data= request.get_json()
        #create student instance
        new_student=Student(
            name=body_data.get("name"),
            email=body_data.get("email"),
            address=body_data.get("address")
        )
        #add to session
        db.session.add(new_student)
        #commit
        db.session.commit()
        #return response
        return student_schema.dump(new_student), 201
    except IntegrityError as err:
        print (err.orig.pgcode)
        if err.orig.pgcode ==errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
        
        if err.orig.pgcode==errorcodes.UNIQUE_VIOLATION:
            return{"messgae":"email address already in use"}, 409
#delete
students_bp.route("/<int:student_id>", methods=["Delete"])
def delete_student(student_id):
    stmt=db.select(Student).filter_by(id=student_id)
    student=db.session.scalar(stmt)
    if student: 
        db.session.delete(student)
        db.session.commit()
        return{"messgae"f"student with {Student.name} deleted"}
    else:
        return {"message"f"student with {student_id} does not exist"}, 404

#update
@students_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    try:
        # find student with id you want to update
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)
        # get the data to be updated from the request body
        body_data = request.get_json()
        # if student exists
        if student:
            # update the student data
            student.name = body_data.get("name") or student.name
            student.email = body_data.get("email") or student.email
            student.address = body_data.get("address") or student.address
            # commit the changes
            db.session.commit()
            # return updated data
            return student_schema.dump(student)
        # else
        else:
            # return error message
            return {"message": f"Student with id {student_id} does not exist"}, 404
    
    except IntegrityError:
        return {"message": "Email address already in use"}, 409
