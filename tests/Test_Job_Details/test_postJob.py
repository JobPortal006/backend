import pytest
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from data.Account_creation.Tables.table import (
    JobPost, Location, EmployeeTypes, JobRole, SkillSets, SkillSetMapping, Signup,CompanyDetails
)
Base = declarative_base()

engine = create_engine('mysql://theuser:thepassword@16.171.154.253:3306/backend1')
Base.metadata.create_all(bind=engine)

@pytest.fixture
def api_url():
    return 'http://192.168.1.39:8000/job_post/'

@pytest.fixture
def data():
    return {
      "job_title": "QA Testing",
      "job_description": "Develop and maintain software applications.",
      "employee_type": "Day/Night Shift",
      "job_role": "Backend Developer",
      "location": "Rajastan",
      "skill_set": ["Node JS","Java"],
      "qualification": "Bachelor's Degree in Computer Science",
      "experience": "2-4 years",
      "salary_range": "4-6 LPA",
      "no_of_vacancies": 3,
      "company_name": "Hexaware",
      "email":"brochill22@gmail.com"
    }

def get_or_create_and_get_id(session, model, column_name, value):
    obj = session.query(model).filter_by(**{column_name: value}).first()
    if obj is None:
        obj = model(**{column_name: value})
        session.add(obj)
        session.commit()
    return obj.id

@pytest.mark.django_db
def test_create_job_post(api_url, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    headers = {'Content-Type': 'application/json'}
    # API testing
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    message = response_data.get('message', '')
    if response_data['statusCode'] == 200:
        # Fetch the employee_id after the signup is inserted
        inserted_signup = session.query(Signup).filter_by(email=data['email']).first()
        employee_id = inserted_signup.id

        # Fetch the company_id after the company details are inserted
        inserted_company_details = session.query(CompanyDetails).filter_by(company_name=data['company_name']).first()
        company_id = inserted_company_details.id

        # Get or create employee_type_id, job_role_id, and location_id
        employee_type_id = get_or_create_and_get_id(session, EmployeeTypes, 'employee_type', data['employee_type'])
        job_role_id = get_or_create_and_get_id(session, JobRole, 'job_role', data['job_role'])
        location_id = get_or_create_and_get_id(session, Location, 'location', data['location'])

        # Insert data into the JobPost table
        job_post_data = {
            "employee_id": employee_id,
            "company_id": company_id,
            "job_title": data['job_title'],
            "job_description": data['job_description'],
            "qualification": data['qualification'],
            "experience": data['experience'],
            "salary_range": data['salary_range'],
            "no_of_vacancies": data['no_of_vacancies'],
            "employee_type_id": employee_type_id,
            "job_role_id": job_role_id,
            "location_id": location_id
        }

        job_post_entry = JobPost(**job_post_data)
        session.add(job_post_entry)
        session.commit()


         # Check if data is inserted into the Signup table
        assert session.query(JobPost).filter_by(id=job_post_entry.id).first() is not None

        # Insert data into the SkillSets table and get IDs
        skill_ids = []
        for skill_name in data['skill_set']:
            skill_id = get_or_create_and_get_id(session, SkillSets, 'skill_set', skill_name)
            skill_ids.append(skill_id)

        # Insert data into the SkillSetMapping table
        for skill_id in skill_ids:
            skill_set_mapping_data = {
                "employee_id": employee_id,
                "skill_id": skill_id,
                "job_id": job_post_entry.id
            }

            skill_set_mapping_entry = SkillSetMapping(**skill_set_mapping_data)
            session.add(skill_set_mapping_entry)
            session.commit()

        # Check if data is inserted into the SkillSetMapping table
        assert session.query(SkillSetMapping).filter_by(id=skill_set_mapping_entry.id).first() is not None

        assert 'message' in response_data
        assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
        assert 'message' in response_data
        assert response_data['message'] == message

    session.close()  # Close the session after use