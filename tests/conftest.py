import os

import pytest

from portal import create_app
from portal import db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DB_NAME': 'portal_test',
        'DB_USER': 'portal_user',
    })

    with app.app_context():
        db.init_db()

        with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(f.read())
                con.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email, password):
        return self._client.post('/', data={'email': email, 'password': password})

    def login_teacher(self):
        return self.login('teacher@stevenscollege.edu', 'qwerty')

    def login_student(self):
        return self.login('student@stevenscollege.edu', 'asdfgh')

    def logout(self):
        return self._client.get('/logout')

class CourseActions(object):
    def __init__(self, client):
        self._client = client

    def create(self, course_number, course_title):
        return self._client.post('/courses/create', data={'course_number': course_number, 'course_title': course_title})

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def course(client):
    return CourseActions(client)
