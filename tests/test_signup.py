from django import urls
import pytest
from django.test import Client

@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('signup'),
    ('login'),
    ('loginWithOTP'),
    ('forgetpassword')
])
def test_render_views(param):
    client = Client()
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200

import json
from django.test import TestCase
from django.urls import reverse

class MyApiTests(TestCase):
    def test_hello_world_api(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Request method should be POST')

import pytest
import json
from django.test import TestCase, Client
from unittest.mock import patch
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SignupTestCase(TestCase):
    def test_successful_signup(self):
        client = Client()
        data = {
            "email": "jeevael@gmail.com",
            "mobile_number": "+916380532243",
            "password": "vimal",
            "signup_by": "Recruiter",
        }
        response = client.post("/signup/", json.dumps(data), content_type="application/json")
        assert response.status_code == 200

    def test_email_already_registered(self):
        existing_email = "jeevael@gmail.com"
        client = Client()
        data = {
            "email": existing_email,
            "mobile_number": "1234567890",
            "password": "testpassword",
            "signup_by": "user",
        }
        response = client.post("/signup/", json.dumps(data), content_type="application/json")
        assert response.status_code == 200

    def test_server_error(self):
        client = Client()
        data = {
            "email": "test@example.com",
        }
        response = client.post("/signup/", json.dumps(data), content_type="application/json")
        assert response.status_code == 200




