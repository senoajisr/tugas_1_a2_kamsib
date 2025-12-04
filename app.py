from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from typing import Sequence, Optional
from werkzeug.wrappers import Response
import sqlite3
from app_constants import *


app: Flask = Flask(__name__)
app.config[SQLALCHEMY_DATABASE_URI_STRING] = APP_SQLITE_URI
app.config[SQLALCHEMY_TRACK_MODIFICATIONS_STRING] = SQLALCHEMY_TRACK_MODIFICATIONS_VALUE
db: SQLAlchemy = SQLAlchemy(app)


class Student(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(STUDENT_NAME_CHARACTER_LIMIT), nullable=False)
    age: int = db.Column(db.Integer, nullable=False)
    grade: str = db.Column(db.String(STUDENT_GRADE_CHARACTER_LIMIT), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'


@app.route(INDEX_ROUTE)
def index() -> str:
    # RAW Query
    students: Sequence = db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
    return render_template(INDEX_URI, students=students)


@app.route(ADD_ROUTE, methods=[METHOD_POST])
def add_student() -> Response:
    name: str = request.form[NAME_FORM_NAME]
    age: str = request.form[AGE_FORM_NAME]
    grade: str = request.form[GRADE_FORM_NAME]
    
    if not verify_form(name, age, grade):
        return redirect(url_for(INDEX_PAGE))
    
    connection: sqlite3.Connection = sqlite3.connect(SQLITE_STUDENT_DATABASE_PATH)
    cursor: sqlite3.Cursor = connection.cursor()

    # RAW Query
    # db.session.execute(
    #     text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),
    #     {'name': name, 'age': age, 'grade': grade}
    # )
    # db.session.commit()
    query: str = INSERT_STUDENT_QUERY.format(name=name, age=age, grade=grade)
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect(url_for(INDEX_PAGE))


@app.route(DELETE_ROUTE) 
def delete_student(id) -> Response:
    # RAW Query
    db.session.execute(text(DELETE_STUDENT_BY_ID_QUERY.format(id=id)))
    db.session.commit()
    return redirect(url_for(INDEX_PAGE))


@app.route(EDIT_ROUTE, methods=[METHOD_GET, METHOD_POST])
def edit_student(id) -> Response|str:
    if request.method == METHOD_POST:
        name: str = request.form[NAME_FORM_NAME]
        age: str = request.form[AGE_FORM_NAME]
        grade: str = request.form[GRADE_FORM_NAME]
        
        # RAW Query
        db.session.execute(text(UPDATE_STUDENT_QUERY.format(name=name, age=age, grade=grade, id=id)))
        db.session.commit()
        return redirect(url_for(INDEX_PAGE))
    else:
        # RAW Query
        student: Optional[SQLAlchemy.Row] = db.session.execute(text(FETCH_ALL_STUDENT_QUERY.format(id=id))).fetchone()
        return render_template(EDIT_URI, student=student)


def verify_form(name: str, age: str, grade: str) -> bool:
    if not verify_age_form(age):
        return False
    return True


def verify_age_form(value: str) -> bool:
    if not validate_string_is_digit(value):
        return False
    value: int = int(value)
    if not validate_number_is_in_range(value, MIN_AGE, MAX_AGE):
        return False
    return True


def validate_string_is_digit(value: str) -> bool:
    return value.isdigit()


def validate_number_is_in_range(value: int, min: int, max: int):
    return value in range(min, max, 1)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=APP_HOST_URI, port=APP_PORT, debug=APP_DEBUG)

