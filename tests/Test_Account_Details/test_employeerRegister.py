import pytest
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from data.Account_creation.Tables.table import Signup, Address, CompanyDetails

# Define the SQLAlchemy model
Base = declarative_base()

engine = create_engine('mysql://theuser:thepassword@51.20.54.231:3306/backend1')
Base.metadata.create_all(bind=engine)

@pytest.fixture
def api_url():
    return 'http://192.168.1.39:8000/employerRegister/'

@pytest.fixture
def data():
    return {
        "contact_information": {
            "contact_person_name": "John",
            "contact_person_position": "HR",
            "email": "brochill227@gmail.com",
            "mobile_number": "+911234567827"
        },
        "company_address": {
            "address_type": "Permanent",
            "city": "Sample City",
            "country": "Sample Country",
            "pincode": "123456",
            "state": "Sample State",
            "street": "Sample Street"
        },
        "company_details": {
            "company_logo": "john_doe.jpg",
            "company_name": "Bosch",
            "company_industry": "IT",
            "company_description": "IT Service Company",
            "no_of_employees": 100,
            "company_website_link": "www.cts.com"
        }
    }

@pytest.mark.django_db
def test_employeer_register_success(api_url, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    headers = {'Content-Type': 'application/json'}  
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    message = response_data.get('message', '')
    if response_data['statusCode'] == 200:
        # Insert data into the tables
        signup_entry = Signup(**data['contact_information'])
        session.add(signup_entry)
        session.commit()
        
        # Fetch the employee_id after the signup is inserted
        inserted_signup = session.query(Signup).filter_by(email=data['contact_information']['email']).first()
        employee_id = inserted_signup.id

        # Insert data into the Address table
        address_data = data['company_address']
        address_data['employee_id'] = employee_id
        address_entry = Address(**address_data)
        session.add(address_entry)
        session.commit()

        # Insert data into the CompanyDetails table
        company_details_data = data['company_details']
        company_details_data['employee_id'] = employee_id
        company_details_entry = CompanyDetails(**company_details_data)
        session.add(company_details_entry)
        session.commit()

        # Check the row count after the inserts
        row_count_signup = session.query(Signup).count()
        row_count_address = session.query(Address).count()
        row_count_company_details = session.query(CompanyDetails).count()
        
        assert row_count_signup > 0
        assert row_count_address > 0
        assert row_count_company_details > 0

        assert 'message' in response_data
        assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
        assert 'message' in response_data
        assert response_data['message'] == message
    session.close()  # Close the session after use

@pytest.mark.django_db
def test_employeer_register_failure(api_url, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    headers = {'Content-Type': 'application/json'}  
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data['statusCode'] == 404
    session.close()  # Close the session after use
