import requests
from backend.settings import base_url

def test_send_data_to_api():
    # Define the data to be sent
    data = {
        "email":"brochill11@gmail.com",
        "password":"R@gul007"
    }
    # Send a POST request with the data
    api_url = base_url + 'login/'
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    response_data = response.json()
    message = response_data['message']
    print(message)
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