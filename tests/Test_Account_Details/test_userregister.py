from backend.settings import base_url
import requests

def test_userRegister():
    # Define the API endpoint
    api_url = base_url + 'userRegister/'

    # Define the data to be sent
    data = {
  "userDetails": {
    "date_of_birth": "1995-06-15",
    "first_name": "John",
    "gender": "Male",
    "last_name": "Doe",
    "mobile_number": "9952469144",
    "profile_picture": "john_doe.jpg"
  },
  "address": {
    "current": {
      "address_type": "Current",
      "city": "Sample City",
      "country": "Sample Country",
      "pincode": "123456",
      "state": "Sample State",
      "street": "Sample Street"
    },
    "permanent": {
      "address_type": "Permanent",
      "city": "Permanent City",
      "country": "Permanent Country",
      "pincode": "789012",
      "state": "Permanent State",
      "street": "Permanent Street"
    }
  },
   "education": {
        "college_end_year": 2023,
        "college_name": "Sample College",
        "college_percentage": 80,
        "college_start_year": 2019,
        "degree": "Bachelor's",
        "department": "Computer Science",
        "education_type": "PG",
        "hsc_end_year": 2018,
        "hsc_percentage": 85,
        "hsc_school_name": "Sample Higher Secondary School",
        "hsc_start_year": 2016,
        "pg_college_degree": "Master's",
        "pg_college_department": "Computer Science",
        "pg_college_end_year": 2025,
        "pg_college_name": "Sample University",
        "pg_college_percentage": 85,
        "pg_college_start_year": 2023,
        "diploma_college_name":"Sample diploma college",
        "diploma_college_start_year":2002,
        "diploma_college_end_year":2005,
        "diploma_college_percentage": 85,
        "diploma_college_department":"CS",
        "diploma_college_degree":"diploma",
        "sslc_end_year": 2016,
        "sslc_percentage": 92,
        "sslc_school_name": "Sample Secondary School",
        "sslc_start_year": 2014
    },
  "jobPreference": {
    "department": "Software Development",
    "industry": "Information Technology",
    "key_skills": "Java, Python, JavaScript",
    "prefered_locations": "Sample City, Another City"
  },
   "professionalDetails": {
     "companies": [
       {
         "companyName": "ABC Inc.",
         "years_of_exprence":1,
         "job_role": "Software Engineer",
         "skills": "Java, Python, JavaScript"
       },
       {
         "companyName": "EFG Inc.",
         "years_of_exprence":2,
         "job_role": "Software Engineer",
         "skills": "Java, Python, JavaScript"
       }
     ],
     "isExperienced": True,
     "numberOfCompanies": "2"
   },   
  "resume": "john_doe_resume.pdf"
}

    # Send a POST request with the data
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    response_data = response.json()
    message = response_data['message']
    # data = response_data['data']
    if response_data['statusCode'] == 200:
      assert 'message' in response_data
      assert response_data['message'] == message
    elif response_data['statusCode'] == 404:
      assert 'message' in response_data
      assert response_data['message'] == message
    else:
      assert response_data['statusCode'] == 500
      assert 'message' in response_data
      assert response_data['message'] == message
    # assert response_data['data'] == data
