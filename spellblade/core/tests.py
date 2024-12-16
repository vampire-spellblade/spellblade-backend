from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from . import models
from . import serializers

class TestLogin(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

        self.url = reverse('login')

    def test_login_success(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Login successful'))
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

    def test_login_missing_email(self):
        data = {
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))

    def test_login_empty_email(self):
        data = {
            'email': '',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))

    def test_login_missing_password(self):
        data = {
            'email': 'jdoe@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password required'))

    def test_login_empty_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password required'))

    def test_login_missing_email_and_password(self):
        data = {}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))
        self.assertEqual(response.data['error'][1], _('Password required'))

    def test_login_empty_email_and_password(self):
        data = {
            'email': '',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))
        self.assertEqual(response.data['error'][1], _('Password required'))

    def test_login_missing_email_and_empty_password(self):
        data = {
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))
        self.assertEqual(response.data['error'][1], _('Password required'))

    def test_login_empty_email_and_missing_password(self):
        data = {
            'email': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))
        self.assertEqual(response.data['error'][1], _('Password required'))

    def test_login_incorrect_email(self):
        data = {
            'email': 'incorrect_email',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Incorrect email or password'))

    def test_login_incorrect_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'incorrect_password',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Incorrect email or password'))

    def test_login_incorrect_email_and_password(self):
        data = {
            'email': 'invalid_email',
            'password': 'incorrect_password',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Incorrect email or password'))

    def test_login_invalid_email_type(self):
        data = {
            'email': 123,
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email must be a string'))

    def test_login_invalid_password_type(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be a string'))

    def test_login_invalid_email_and_password_type(self):
        data = {
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email must be a string'))
        self.assertEqual(response.data['error'][1], _('Password must be a string'))

    def test_login_email_with_uppercase_characters(self):
        data = {
            'email': 'JDOE@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Login successful'))
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

    def test_login_email_with_trailing_whitespaces(self):
        data = {
            'email': ' jdoe@example.com ',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Login successful'))
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

class TestLogout(APITestCase):

    def setUp(self):
        self.url = reverse('logout')

class TestSignUp(APITestCase):

    def setUp(self):
        self.url = reverse('sign_up')

class TestLoginRenew(APITestCase):

    def setUp(self):
        self.url = reverse('login_renew')
