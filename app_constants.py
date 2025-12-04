SQLALCHEMY_DATABASE_URI: str = "SQLALCHEMY_DATABASE_URI"
SQLALCHEMY_TRACK_MODIFICATIONS: str = "SQLALCHEMY_TRACK_MODIFICATIONS"

APP_SQLITE_URI: str = "sqlite:///students.db"
SQLITE_STUDENT_DATABASE_PATH: str = "instance/students.db"
INDEX_URI: str = "index.html"
EDIT_URI: str = "edit.html"
APP_HOST_URI: str = "0.0.0.0"

INDEX_ROUTE: str = "/"
ADD_ROUTE: str = "/add"
DELETE_ROUTE: str = "/delete/<string:id>"
EDIT_ROUTE: str = "/edit/<int:id>"

INDEX_PAGE: str = "index"

METHOD_POST: str = "POST"
METHOD_GET: str = "GET"

FETCH_ALL_STUDENT_QUERY: str = "SELECT * FROM student"
INSERT_STUDENT_QUERY: str = "INSERT INTO student (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
UPDATE_STUDENT_QUERY: str = "UPDATE student SET name='{name}', age={age}, grade='{grade}' WHERE id={id}"
FETCH_STUDENT_BY_ID_QUERY: str = "SELECT * FROM student WHERE id={id}"
DELETE_STUDENT_BY_ID_QUERY = "DELETE FROM student WHERE id={id}"

NAME_FORM_NAME: str = "name"
AGE_FORM_NAME: str = "age"
GRADE_FORM_NAME: str = "grade"