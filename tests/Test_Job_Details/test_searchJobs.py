import pytest
import requests
import json

@pytest.fixture
def api_url():
    return 'http://192.168.1.39:8000/view_jobs/'

@pytest.fixture
def data():
    return {
      "skill": ["JavaScript"],
      "location": "Chennai",
      "experience": "0-1 year"
    }

@pytest.mark.django_db
def test_search_job(api_url, data):
    headers = {'Content-Type': 'application/json'}  
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    message = response_data.get('message', '')
    if response_data['statusCode'] == 200:
        assert 'message' in response_data
        assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
        assert 'message' in response_data
        assert response_data['message'] == message

