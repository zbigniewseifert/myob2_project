import os
import tempfile
import io
import re
from flask import url_for

import pytest
import application


@pytest.fixture
def client():
    db_fd, application.app.config['DATABASE'] = tempfile.mkstemp()
    application.app.config['TESTING'] = True

    with application.app.test_client() as client:
        with application.app.app_context():
            application.Schema()
        yield client
    os.close(db_fd)
    os.unlink(application.app.config['DATABASE'])

def test_first_page(client):
    #Checks template generation and ranking system
    rv = client.get('/')
    assert b'Welcome to the voting application!' in rv.data
    assert b'Rank:0' in rv.data

def test_file_upload(client):
    #Checks file upload
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    data['description'] = "TestFile"
    response = client.post('/upload', data=data)
    rv = client.get('/')
    assert b'Name:TestFile' in rv.data

def test_file_vote(client):
    #Checks voting mechanism
    data = {}
    rv = client.get('/')
    search_id = re.search(r'(Name:TestFile ID:)([\d]+)',rv.data.decode())
    id = search_id.groups()[1]
    data['file_id'] = id
    response = client.post('/vote', data=data)
    assert b'Vote Successfull!' in response.data

def test_first_page2(client):
    #Checks template generation and ranking system after TestFile addition
    rv = client.get('/')
    assert b'Welcome to the voting application!' in rv.data
    assert b'Rank:0 </b> Name:TestFile' in rv.data

def test_file_deletion(client):
    #Checks file deletion
    rv = client.get('/')
    search_id = re.search(r'(Name:TestFile ID:)([\d]+)',rv.data.decode())
    id = search_id.groups()[1]
    data = {}
    data['item'] = id
    response = client.post('/del', data=data)
    assert b'Deleted' in response.data
