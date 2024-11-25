from flask import Blueprint
db_commands=Blueprint("db", __name__)
from init import db
from models.student import Student
from models.teacher import Teacher
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print ("Tables Created")
@db_commands.cli.command("drop")
def drop_all():
     db.drop_all()
     print ("tables dropped")
@db_commands.cli.command("seed")
def seed_tables():
     students = [
        Student(
             name="Bob",
             email="a@a.com",
             address="Sydney"

        ),
        Student(
             name="sam",
             email="b@b.com",
             address="Melbourne"
        )  
     ]
     db.session.add_all(students)
     
     teachers = [
          Teacher(name="mrs odd",
                  department="Science",
                  address="Sydney"
                  ),
          Teacher(
               name="mrs weird",
                  department="English",
                  address="Darwin"
                  ),
          
     ]
     db.session.add_all(teachers)
     db.session.commit()
     print("tables seeded")
