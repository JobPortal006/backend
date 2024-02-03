# import json
# import pytest
# from django.test import Client
# from django import urls
# from django.db import connection

# @pytest.mark.django_db
# @pytest.mark.parametrize('param', [
#     ('signup'),
#     ('login'),
#     ('loginWithOTP'),
#     ('forgetpassword')
# ])
# def test_render_views(param):
#     client = Client()
#     temp_url = urls.reverse(param)
#     resp = client.get(temp_url)
#     assert resp.status_code == 200
    
import pytest
import requests
from data.User_details import message

def test_signup():
    # Define the API endpoint
    api_url = "http://192.168.1.38:8000/signup/"

    # Define the data to be sent
    data = {
        "email":"ragul@gmail.com",
        "mobile_number":"8072850717",
        "password":"vimal",
        "signup_by":"User"
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
