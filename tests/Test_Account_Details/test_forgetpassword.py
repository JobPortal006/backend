from backend.settings import base_url
import requests

def test_forgetpassword():
    # Define the API endpoint
    api_url = base_url + 'forgetpassword/'

    # Define the data to be sent
    data = {
        "email":"brochill547@gmail.com"
    }
    # Send a POST request with the data
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    response_data = response.json()
    message = response_data['message']
   
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

