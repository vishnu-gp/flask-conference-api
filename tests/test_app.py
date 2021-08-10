import sys
import pytest
import json

# setting path
sys.path.append('../conference')
from run import create_app
from Model import db



@pytest.fixture
def client():

    app = create_app("configtest")
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    with app.test_client() as client:
        yield client

# 1 Testing the welcome page
def test_welcome_page(client):
    response = client.get('api/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Test for Conference Model

# 2 Testing the conference creation
def test_post_conference(client):
    input_data = {"title":"Scala Conference", "description":"This conference will be conducted at Gurgaon", "start_date": "2021-08-11","end_date": "2021-08-18"}
    response = client.post('api/Conference', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    response['data'].pop('id')
    for key in input_data:
        assert response['data'][key] == input_data[key]

# 3 Testing the conference creation fail
def test_post_conference_fail(client):
    input_data = ''
    response = client.post('api/Conference', json=input_data)
    assert response.status_code == 400
    assert b"error" in response.data

# 4 Testing the conference edit
def test_patch_conference(client):
    input_data = {"id": 1, "title":"Python Conference", "description":"This conference will be conducted at Delhi", "start_date": "2021-08-12","end_date": "2021-08-20"}
    response = client.patch('api/Conference', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    for key in input_data:
        assert response['data'][key] == input_data[key]

# 5 Testing the conference edit fail
def test_patch_conference_fail(client):
    input_data = {"id": 100, "title":"Python Conference", "description":"This conference will be conducted at Delhi", "start_date": "2021-08-12","end_date": "2021-08-20"}
    response = client.patch('api/Conference', json=input_data)
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['status'] == 'error'

# 6 Testing the conference listing
def test_get_conference(client):
    input_data = {"id": 1, "title":"Python Conference", "description":"This conference will be conducted at Delhi", "start_date": "2021-08-12","end_date": "2021-08-20"}
    response = client.get('api/Conference', json=input_data)
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['status'] == 'success'
    for key in input_data:
        assert response['data'][0][key] == input_data[key]

# Tests for Talk Model

# 7 Testing adding a Talk
def test_post_talk(client):
    input_data = {"title":"Python DataType", "description":"This talk is about Python DataTypes", "scheduled_at":"2021-08-15T16:30:00", "duration_min": 120, "conference_id": 1}
    response = client.post('api/Talk', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    for key in input_data:
        assert response['data'][key] == input_data[key]

# 8 Testing adding a Talk fail
def test_post_talk_fail(client):
    input_data = {"title":"Python DataType", "description":"This talk is about Python DataTypes", "scheduled_at":"2021-08-15T16:30:00", "duration_min": 120, "conference_id": 100}
    response = client.post('api/Talk', json=input_data)
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['status'] == 'error'

# 9 Testing editing a talk
def test_patch_talk(client):
    input_data = {"title":"Python DataTypes", "description":"This talk is about Python and Python DataTypes", "scheduled_at":"2021-08-15T17:30:00", "duration_min": 150, "conference_id": 1, "id":1}
    response = client.patch('api/Talk', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    for key in input_data:
        assert response['data'][key] == input_data[key]

# 10 Testing editing a talk fail
def test_patch_talk_fail(client):
    input_data = {"title":"Python DataTypes", "description":"This talk is about Python and Python DataTypes", "scheduled_at":"2021-08-15T17:30:00", "duration_min": 150, "conference_id": 1, "id":100}
    response = client.patch('api/Talk', json=input_data)
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['status'] == 'error'

# 11 Testing add speaker to a talk
def test_post_talk_speaker(client):
    input_data = { "talk_id":1, "user_type": "speaker", "username": "monica", "email":"monica@test.com"}
    response = client.post('api/Talk/User', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    input_data['id'] = input_data.pop('talk_id')
    input_data.pop('user_type')
    for key in input_data:
        if key == 'id':
            assert response['data'][key] == input_data[key]
        else:
            assert response['data']['speakers'][0][key] == input_data[key]

# 12 Testing add speaker to a talk fail
def test_post_talk_speaker_fail(client):
    input_data = { "talk_id":100, "user_type": "speaker", "username": "monica", "email":"monica@test.com"}
    response = client.post('api/Talk/User', json=input_data)
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['status'] == 'error'

# 13 Testing add participant to a talk
def test_post_talk_participant(client):
    input_data = { "talk_id":1, "user_type": "participant", "username": "sam", "email":"sam@test.com"}
    response = client.post('api/Talk/User', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    input_data['id'] = input_data.pop('talk_id')
    input_data.pop('user_type')
    for key in input_data:
        if key == 'id':
            assert response['data'][key] == input_data[key]
        else:
            assert response['data']['participants'][0][key] == input_data[key]

# 14 Testing add participant to a talk
def test_post_talk_participant_fail(client):
    input_data = { "talk_id":100, "user_type": "participant", "username": "sam", "email":"sam@test.com"}
    response = client.post('api/Talk/User', json=input_data)
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['status'] == 'error'

def clear_db(client):
    db.session.remove()
    db.drop_all()