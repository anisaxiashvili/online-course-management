import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
def test_register_and_token():
    client = APIClient()
    resp = client.post(reverse('register'), {
        'username': 'teacher1',
        'password': 'StrongPass123!',
        'role': 'teacher',
        'email': 't1@example.com'
    }, format='json')
    assert resp.status_code == 201
    token = client.post(reverse('token_obtain_pair'), {
        'username': 'teacher1', 'password': 'StrongPass123!'
    }, format='json')
    assert token.status_code == 200
    assert 'access' in token.data
