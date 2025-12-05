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