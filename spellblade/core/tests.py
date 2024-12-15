from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from . import models
from . import serializers

class TestLogin(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'y79rNX#+l45M',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            self.user = serializer.save()
        else:
            print(serializer.errors)

        self.url = reverse('login')

    def test_success(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'y79rNX#+l45M',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertTrue('token' in response.data)

    def test_missing_email(self):
        data = {
            'password': 'y79rNX#+l45M',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_password(self):
        data = {
            'email': 'jdoe@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_email_format(self):
        data = {
            'email': 'jdoe',
            'password': 'y79rNX#+l45M',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_email(self):
        data = {
            'email': 'jdoe7@example.com',
            'password': 'y79rNX#+l45M',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'y79rNX#+l45m',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
