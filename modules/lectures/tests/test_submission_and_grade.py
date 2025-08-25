import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from modules.courses.models import Course

User = get_user_model()

@pytest.mark.django_db
def test_student_submit_and_teacher_grade():
    t = User.objects.create_user(username='t', password='Pass123!', role='teacher')
    s = User.objects.create_user(username='s', password='Pass123!', role='student')
    course = Course.objects.create(title='Sci', description='desc', owner=t)
    course.teachers.add(t)
    course.students.add(s)

    client_t = APIClient()
    token_t = client_t.post('/api/v1/accounts/token/', {'username':'t','password':'Pass123!'}, format='json').data['access']
    client_t.credentials(HTTP_AUTHORIZATION=f'Bearer {token_t}')

    lec = client_t.post('/api/v1/lectures/lectures/', {'course': course.id, 'topic':'Intro'}, format='json').data

    ass = client_t.post('/api/v1/lectures/assignments/', {'lecture': lec['id'], 'text':'Solve Q1'}, format='json')
    assert ass.status_code == 201

    client_s = APIClient()
    token_s = client_s.post('/api/v1/accounts/token/', {'username':'s','password':'Pass123!'}, format='json').data['access']
    client_s.credentials(HTTP_AUTHORIZATION=f'Bearer {token_s}')

    sub = client_s.post('/api/v1/lectures/submissions/', {'lecture': lec['id'], 'text':'My answer'}, format='json')
    assert sub.status_code == 201

    grade = client_t.post('/api/v1/lectures/grades/', {'submission': sub.data['id'], 'score': 95, 'feedback':'Well done'}, format='json')
    assert grade.status_code == 201
