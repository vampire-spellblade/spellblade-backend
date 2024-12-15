from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
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
            self.user = serializer.save()

        self.url = reverse('login')

    def test_login_success(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Login successful'))
        self.assertEqual(response.data['user']['email'], self.user.email)
        self.assertEqual(response.data['user']['first_name'], self.user.first_name)
        self.assertEqual(response.data['user']['last_name'], self.user.last_name)
        self.assertTrue('token' in response.data['user'])

    def test_login_missing_email(self):
        data = {
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid email or password'))

    def test_login_missing_password(self):
        data = {
            'email': 'jdoe@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid email or password'))

    def test_login_invalid_email_format(self):
        data = {
            'email': 'jdoe',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid email or password'))

    def test_login_wrong_email(self):
        data = {
            'email': 'jdoe7@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid email or password'))

    def test_login_wrong_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'abc123!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid email or password'))

class TestLogout(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            self.user = serializer.save()

        self.url = reverse('logout')

        response = self.client.post(reverse('login'), {
            'email': data['email'],
            'password': data['password'],
        }, format='json')

        self.token = response.data['user']['token']

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Logout successful'))
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestSignup(APITestCase):

    def setUp(self):
        self.url = reverse('signup')

    def test_signup_successful_signup(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Signup successful'))
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue('token' in response.data['user'])

    def test_signup_account_already_exists(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            self.user = serializer.save()

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Account already exists'))

    def test_signup_invalid_signup_data(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'short',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['error'], _('Invalid data'))
