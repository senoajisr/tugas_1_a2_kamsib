SQLALCHEMY_DATABASE_URI_STRING: str = "SQLALCHEMY_DATABASE_URI"
SQLALCHEMY_TRACK_MODIFICATIONS_STRING: str = "SQLALCHEMY_TRACK_MODIFICATIONS"
SESSION_LOGGED_IN_STRING: str = "logged_in"
INCORRECT_LOGIN_WARNING: str = "Username or password is incorrect."

APP_SQLITE_URI: str = "sqlite:///students.db"
SQLITE_STUDENT_DATABASE_PATH: str = "instance/students.db"
HOME_URI: str = "home.html"
EDIT_URI: str = "edit.html"
LOGIN_URI: str = "login.html"
APP_HOST_URI: str = "0.0.0.0"

INDEX_ROUTE: str = "/"
HOME_ROUTE: str = "/home"
ADD_ROUTE: str = "/add"
DELETE_ROUTE: str = "/delete/<string:id>"
EDIT_ROUTE: str = "/edit/<int:id>"
LOGOUT_ROUTE: str = "/logout"

HOME_PAGE: str = "home"

METHOD_POST: str = "POST"
METHOD_GET: str = "GET"

FETCH_ALL_STUDENT_QUERY: str = "SELECT * FROM student"
INSERT_STUDENT_QUERY: str = "INSERT INTO student (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
UPDATE_STUDENT_QUERY: str = "UPDATE student SET name='{name}', age={age}, grade='{grade}' WHERE id={id}"
FETCH_STUDENT_BY_ID_QUERY: str = "SELECT * FROM student WHERE id={id}"
DELETE_STUDENT_BY_ID_QUERY = "DELETE FROM student WHERE id={id}"
DELETE_ALL_STUDENT_QUERY: str = "DELETE FROM student"

NAME_FORM_NAME: str = "name"
AGE_FORM_NAME: str = "age"
GRADE_FORM_NAME: str = "grade"
USERNAME_FORM_NAME: str = "username"
PASSWORD_FORM_NAME: str = "password"

APP_PORT: int = 5000
APP_SECRET_KEY: str = "Tugas-Keamanan-Siber-2025" # This is NOT safe
APP_ADMIN_USERNAME: str = "admin" # This is NOT safe
APP_ADMIN_PASSWORD: str = "i_am_admin" # This is NOT safe

STUDENT_NAME_CHARACTER_LIMIT: int = 100
STUDENT_GRADE_CHARACTER_LIMIT: int = 10

APP_DEBUG: bool = True

SQLALCHEMY_TRACK_MODIFICATIONS_VALUE: bool = False

MIN_AGE: int = 0
MAX_AGE: int = 122