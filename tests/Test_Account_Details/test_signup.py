import pytest
import requests
import json
from data.Tables.table import Signup
from backend.settings import base_url
from data.message import create_session

@pytest.fixture
def data():
    return {
        "email": "brochill26@gmail.com",
        "mobile_number": "+91123456786",
        "password": "vimal",
        "signup_by": "User"
    }

@pytest.mark.django_db
def test_create_user_success(data):
    session = create_session()
    headers = {'Content-Type': 'application/json'}  
    # api_url = base_url + 'signup/'
    api_url = 'http://192.168.1.44:8000/signup/'
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    message = response_data.get('message', '')
    if response_data['statusCode'] == 200:
        # Insert data into the table only when the status code is 200
        signup_entry = Signup(**data)
        session.add(signup_entry)
        session.commit()
        inserted_signup = session.query(Signup).filter_by(email=data['email']).first()
        # Check if data is inserted into the Signup table
        assert session.query(Signup).filter_by(id=inserted_signup.id).first() is not None
        assert inserted_signup is not None
        assert inserted_signup.signup_by == data['signup_by']
        assert inserted_signup.mobile_number == data['mobile_number']
        assert 'message' in response_data
        assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
        assert 'message' in response_data
        assert response_data['message'] == message
    session.close()  # Close the session after use

# @pytest.mark.django_db
# def test_create_user_failure(api_url, data):
#     session = create_session()
#     headers = {'Content-Type': 'application/json'}  
#     response = requests.post(api_url, data=json.dumps(data), headers=headers)
#     assert response.status_code == 200
#     response_data = response.json()
#     print(response_data)
#     assert response_data['statusCode'] == 404
#     session.close()  # Close the session after use
