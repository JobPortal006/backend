import pytest
from django.test import Client
from django import urls

@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('signup'),
    ('login'),
    ('loginWithOTP'),
    ('forgetpassword'),
    ('updatepassword')

])
def test_render_views(param):
    client = Client()
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200