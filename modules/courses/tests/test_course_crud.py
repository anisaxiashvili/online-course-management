import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
def test_teacher_creates_course():
    client = APIClient()
    User.objects.create_user(username='t', password='Pass123!', role='teacher')
    token = client.post('/api/v1/accounts/token/', {'username':'t','password':'Pass123!'}, format='json').data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    resp = client.post('/api/v1/courses/courses/', {'title':'Math','description':'Algebra'}, format='json')
    assert resp.status_code == 201
