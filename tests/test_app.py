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
    db.session.remove()
    db.drop_all()
    
def test_welcome_page(client):
    response = client.get('api/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_post_conference(client):
    input_data = {"title":"Scala Conference", "description":"This conference will be conducted at Gurgaon", "start_date": "2021-08-11","end_date": "2021-08-18"}
    response = client.post('api/Conference', json=input_data)
    assert response.status_code == 201
    response = json.loads(response.data)
    assert response['status'] == 'success'
    response['data'].pop('id')
    for key in input_data:
        assert response['data'][key] == input_data[key]
