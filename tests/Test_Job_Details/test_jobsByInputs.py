import pytest
import requests
import json

@pytest.mark.django_db
def test_job_by_company_name():
    headers = {'Content-Type': 'application/json'} 
    url = 'http://192.168.1.39:8000/job_details_by_companyName/' 
    data = {
     "company_name":"Google"
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

@pytest.mark.django_db
def test_job_by_employee_type():
    headers = {'Content-Type': 'application/json'} 
    url = 'http://192.168.1.39:8000/job_details_by_employeeType/'  
    data = {
       "employee_type":"Part time"
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