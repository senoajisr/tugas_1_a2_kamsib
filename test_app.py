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
    main_app.db_path = TEST_SQLITE_STUDENT_DATABASE_PATH
    main_app.db_uri = TEST_APP_SQLITE_URI
    app: Flask = main_app.app

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_home(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")
    assert b"<h1>Students</h1>" in response.data


def test_proper_add_form(client: FlaskClient, app: Flask):
    response = client.post(ADD_ROUTE, data={"name": "testing", "age": "20", "grade": "A"})
    
    with app.app_context():
        students: Sequence = main_app.db.session.execute(text(FETCH_ALL_STUDENT_QUERY)).fetchall()
        assert len(students) == 1