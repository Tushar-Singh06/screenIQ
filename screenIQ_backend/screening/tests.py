from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Application
from .utils import normalize_score


class ScreeningTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

        response = self.client.post(
            '/api/token/',
            {
                'username': 'testuser',
                'password': 'password123'
            }
        )

        self.token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

    def test_unauthorized_access(self):
        self.client.credentials()

        response = self.client.get('/api/applications/')

        self.assertEqual(response.status_code, 401)

    def test_user_only_sees_own_data(self):

        another_user = User.objects.create_user(
            username='another',
            password='password123'
        )

        Application.objects.create(
            candidate_name='John',
            job_description='JD',
            resume='Resume',
            ai_score=8,
            ai_reasons=['Good'],
            created_by=another_user
        )

        response = self.client.get('/api/applications/')

        self.assertEqual(len(response.data['results']), 0)

    def test_score_normalization(self):
        self.assertEqual(normalize_score('Seven'), 7.0)
        self.assertEqual(normalize_score('7.5'), 7.5)