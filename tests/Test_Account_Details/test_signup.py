import pytest
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from data.Account_creation.Tables.table import Signup

# Define the SQLAlchemy model
Base = declarative_base()

engine = create_engine('mysql://theuser:thepassword@172.31.34.63:3306/backend')
Base.metadata.create_all(bind=engine)

@pytest.fixture
def api_url():
    return 'http://192.168.1.39:8000/signup/'

@pytest.fixture
def data():
    return {
        "email": "brochill26@gmail.com",
        "mobile_number": "+91123456786",
        "password": "vimal",
        "signup_by": "User"
    }

@pytest.mark.django_db
def test_create_user_success(api_url, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    headers = {'Content-Type': 'application/json'}  
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

@pytest.mark.django_db
def test_create_user_failure(api_url, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    headers = {'Content-Type': 'application/json'}  
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data['statusCode'] == 404
    session.close()  # Close the session after use
