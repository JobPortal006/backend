import pytest
import requests
import json

@pytest.mark.django_db
def test_employeer_job_posts():
    headers = {'Content-Type': 'application/json'} 
    url = 'http://192.168.1.39:8000/employer_post_jobs/' 
    data = {
        "employee_id":1
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
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

