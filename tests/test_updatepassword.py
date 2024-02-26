import pytest
import requests

def test_updatepassword():
    # Define the API endpoint
    api_url = "http://192.168.1.39:8000/updatepassword/"

    # Define the data to be sent
    data = {
        "password":"vimal12",
        "email":"brochill547@gmail.com"
    }
    # Send a POST request with the data
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    response_data = response.json()
    message = response_data['message']
    data = response_data['data']
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
    assert response_data['data'] == data