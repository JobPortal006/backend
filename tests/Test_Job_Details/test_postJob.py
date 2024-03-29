import pytest
import requests
from data.message import create_session
import json,jwt
from data.Account_creation.Tables.table import (
    JobPost, Location, EmployeeTypes, JobRole, SkillSets, SkillSetMapping, Signup,CompanyDetails, QualificationMapping, LocationMapping
)
from backend.settings import base_url

@pytest.fixture
def data():
    return {
        "job_title": "AWS Developer",
        "job_description": "Develop and maintain software applications.",
        "employee_type": "Part Time",
        "job_role": "Full Stack Developer",
        "location": ["Chennai","Coimbatore"],
        "skill_set": ["AWS"],
        "qualification": ["B.E"],
        "experience": "0-1 year",
        "salary_range": "4 - 6 LPA",
        "no_of_vacancies": 3,
        "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6InJhZ3Vsa3RyMDA3QGdtYWlsLmNvbSIsInJlZ2lzdGVyZWRfYnkiOiJSZWNydWl0ZXIiLCJleHAiOjE3MTA1NjQ2ODV9.TOCwe5qSSyJxSWclTydc3Px487PDFW1OfQlFFqrtfDg"
    }

def get_or_create_and_get_id(session, model, column_name, value):
    obj = session.query(model).filter_by(**{column_name: value}).first()
    if obj is None:
        obj = model(**{column_name: value})
        session.add(obj)
        session.commit()
    return obj.id

@pytest.mark.django_db
def test_create_job_post(data):
    session = create_session()
    headers = {'Content-Type': 'application/json'}
    # API testing
    api_url = base_url + 'job_post/'
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    message = response_data.get('message', '')
    if response_data['statusCode'] == 200:
        # Fetch the employee_id after the signup is inserted
        token = data['token']
        secret_key = "12345"
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        # employee_id,registered_by,email = decode_token(token)
        inserted_signup = session.query(Signup).filter_by(email=data['email']).first()
        employee_id = inserted_signup.id

        # Fetch the company_id after the company details are inserted
        inserted_company_details = session.query(CompanyDetails).filter_by(company_name=data['company_name']).first()
        company_id = inserted_company_details.id

        # Get or create employee_type_id, job_role_id, and location_id
        employee_type_id = get_or_create_and_get_id(session, EmployeeTypes, 'employee_type', data['employee_type'])
        job_role_id = get_or_create_and_get_id(session, JobRole, 'job_role', data['job_role'])

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
            "job_role_id": job_role_id
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

        # Insert data into the SkillSets table and get IDs
        qualification_ids = []
        for qualification in data['qualification']:
            qualification_id = get_or_create_and_get_id(session, QualificationMapping, 'qualification', qualification)
            qualification_ids.append(qualification_id)

        # Insert data into the qualificationSetMapping table
        for qualification_id in qualification_ids:
            qualification_mapping_data = {
                "employee_id": employee_id,
                "qualification_id": qualification_id,
                "job_id": job_post_entry.id
            }

            qualification_mapping_entry = QualificationMapping(**qualification_mapping_data)
            session.add(qualification_mapping_entry)
            session.commit()

        # Check if data is inserted into the SkillSetMapping table
        assert session.query(QualificationMapping).filter_by(id=qualification_mapping_entry.id).first() is not None

        # Insert data into the SkillSets table and get IDs
        location_ids = []
        for location in data['location']:
            location_id = get_or_create_and_get_id(session, LocationMapping, 'location', location)
            location_ids.append(location_id)

        # Insert data into the locationSetMapping table
        for location_id in location_ids:
            location_mapping_data = {
                "employee_id": employee_id,
                "location_id": location_id,
                "job_id": job_post_entry.id
            }

            location_mapping_entry = LocationMapping(**location_mapping_data)
            session.add(location_mapping_entry)
            session.commit()

        # Check if data is inserted into the SkillSetMapping table
        assert session.query(LocationMapping).filter_by(id=location_mapping_entry.id).first() is not None

        assert 'message' in response_data
        assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
        assert 'message' in response_data
        assert response_data['message'] == message

    session.close()  # Close the session after use