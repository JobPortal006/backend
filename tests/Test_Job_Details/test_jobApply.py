import pytest
import requests
import json
from backend.settings import base_url

@pytest.mark.django_db
def test_job_apply():
  headers = {'Content-Type': 'application/json'} 
  api_url = base_url + 'apply_job/'
  data = {
    "job_id":1,
    "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6InJhZ3Vsa3RyMDA3QGdtYWlsLmNvbSIsInJlZ2lzdGVyZWRfYnkiOiJSZWNydWl0ZXIiLCJleHAiOjE3MTA1NjQ2ODV9.TOCwe5qSSyJxSWclTydc3Px487PDFW1OfQlFFqrtfDg",
    "additional_queries":"Yes",
    "current_ctc":"3 LPA",
    "expected_ctc":"5 LPA",
    "total_experience":"3 years",
    "notice_period":"3 months",
    "resume_file":"resume/2_image.png"
  }
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