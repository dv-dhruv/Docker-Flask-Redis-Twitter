# -*- coding: utf-8 -*-
"""
    Retwis Tests
    ~~~~~~~~~~~~

    Tests the retwis application.

    :copyright: (c) 2016 by Joydeep Bhattacharjee.
    :license: MIT, see LICENSE for more details.
"""

import os
import tempfile
import pytest
from retwis import app
from retwis.views import init_db


@pytest.fixture
def client(request):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'Login' in rv.data


def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, app.config['username'],
               app.config['password'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, app.config['username'] + 'x',
               app.config['password'])
    assert b'Invalid username' in rv.data
    rv = login(client, app.config['username'],
               app.config['password'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(client):
    """Test that messages work"""
    login(client, app.config['username'],
          app.config['password'])
    rv = client.post('/home', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
