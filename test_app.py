from typing import Any, Generator, Sequence
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.test import TestResponse
from app_constants import *
import app as main_app
import pytest

# Test with command: pytest -vv -s

@pytest.fixture()
def app() -> Generator[Any, Any, Any]:
    app: Flask = main_app.app

    with app.app_context():
        # Create DB
        main_app.db.create_all()
        
        # Reset student table
        main_app.db.session.execute(text(DELETE_ALL_STUDENT_QUERY.format(id=id)))
        main_app.db.session.commit()
    
    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_home(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")
    assert b"<h1>Students</h1>" in response.data


def test_form_add_proper(client: FlaskClient, app: Flask):
    fail_message = "the proper input for the form should be stored and displayed"
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": "20", "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1, fail_message
    
    response: TestResponse = client.get("/")
    assert b"<td>Lorem Ipsum</td>" in response.data, fail_message
    assert b"<td>20</td>" in response.data, fail_message
    assert b"<td>Ammet</td>" in response.data, fail_message


def test_form_add_name_over_limit(client: FlaskClient, app: Flask):
    fail_message = f"name with characters over {STUDENT_NAME_CHARACTER_LIMIT} is not allowed"
    above_limit: int = STUDENT_NAME_CHARACTER_LIMIT+10
    response = client.post(ADD_ROUTE, data={"name": "a"*(above_limit), "age": "20", "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 0, fail_message
    
    response: TestResponse = client.get("/")
    assert not b"a"*above_limit in response.data, fail_message


def test_form_add_name_at_limit(client: FlaskClient, app: Flask):
    fail_message = f"name with characters at {STUDENT_NAME_CHARACTER_LIMIT} is allowed"
    response = client.post(ADD_ROUTE, data={"name": "a"*STUDENT_NAME_CHARACTER_LIMIT, "age": "20", "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1, fail_message
    
    response: TestResponse = client.get("/")
    assert b"a"*STUDENT_NAME_CHARACTER_LIMIT in response.data, fail_message


def test_form_add_name_empty(client: FlaskClient, app: Flask):
    fail_message = "empty name field is not allowed"
    response = client.post(ADD_ROUTE, data={"name": "", "age": "20", "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 0, fail_message
    
    response: TestResponse = client.get("/")
    assert not b"<td>Ammet</td>" in response.data, fail_message


def test_form_add_age_over_limit(client: FlaskClient, app: Flask):
    fail_message = f"age with value over {MAX_AGE} is not allowed"
    above_limit = MAX_AGE+1
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": str(above_limit), "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 0, fail_message
    
    response: TestResponse = client.get("/")
    assert not bytes(f"<td>{above_limit}</td>", "utf-8") in response.data, fail_message


def test_form_add_age_at_upper_limit(client: FlaskClient, app: Flask):
    fail_message = f"age with value at {MAX_AGE} is allowed"
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": str(MAX_AGE), "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1, fail_message
    
    response: TestResponse = client.get("/")
    assert bytes(f"<td>{MAX_AGE}</td>", "utf-8") in response.data, fail_message


def test_form_add_age_under_limit(client: FlaskClient, app: Flask):
    fail_message = f"age with value under {MIN_AGE} is not allowed"
    under_limit = MIN_AGE-1
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": str(under_limit), "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 0, fail_message
    
    response: TestResponse = client.get("/")
    assert not bytes(f"<td>{under_limit}</td>", "utf-8") in response.data, fail_message


def test_form_add_age_at_lower_limit(client: FlaskClient, app: Flask):
    fail_message = f"age with value at {MIN_AGE} is allowed"
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": str(MIN_AGE), "grade": "Ammet"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1, fail_message
    
    response: TestResponse = client.get("/")
    assert bytes(f"<td>{MIN_AGE}</td>", "utf-8") in response.data, fail_message


def test_form_add_grade_over_limit(client: FlaskClient, app: Flask):
    fail_message = f"grade with characters over {STUDENT_GRADE_CHARACTER_LIMIT} is not allowed"
    above_limit: int = STUDENT_GRADE_CHARACTER_LIMIT+10
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": "20", "grade": "a"*(above_limit)})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 0, fail_message
    
    response: TestResponse = client.get("/")
    assert not b"a"*above_limit in response.data, fail_message


def test_form_add_grade_at_limit(client: FlaskClient, app: Flask):
    fail_message = f"grade with characters at {STUDENT_GRADE_CHARACTER_LIMIT} is allowed"
    response = client.post(ADD_ROUTE, data={"name": "Lorem Ipsum", "age": "20", "grade": "a"*STUDENT_GRADE_CHARACTER_LIMIT})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1, fail_message
    
    response: TestResponse = client.get("/")
    assert b"a"*STUDENT_GRADE_CHARACTER_LIMIT in response.data, fail_message