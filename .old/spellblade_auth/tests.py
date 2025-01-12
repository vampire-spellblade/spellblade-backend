from hashlib import sha1
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OutstandingToken

User = get_user_model()

class TestLoginView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('refresh_exp', response.data)
        self.assertIn('access', response.data)
        self.assertIn('access_exp', response.data)

        try:
            token = OutstandingToken.objects.get(
                user=self.user,
                token=sha1(response.data['refresh'].encode('utf-8')).hexdigest()
            )
        except OutstandingToken.DoesNotExist:
            self.fail(_('Outstanding token not created.'))

    def test_login_failure_empty_fields(self):
        response = self.client.post(self.url, {
            'username': '',
            'password': '',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 2)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        self.assertListEqual(response.data['username'], [_('This field may not be blank.')])
        self.assertListEqual(response.data['password'], [_('This field may not be blank.')])

    def test_login_failure_empty_username(self):
        response = self.client.post(self.url, {
            'username': '',
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIn('username', response.data)
        self.assertListEqual(response.data['username'], [_('This field may not be blank.')])

    def test_login_failure_empty_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': '',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIn('password', response.data)
        self.assertListEqual(response.data['password'], [_('This field may not be blank.')])

    def test_login_failure_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username': 'invaliduser',
            'password': 'invalidpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIn('non_field_errors', response.data)
        self.assertListEqual([str(error) for error in response.data['non_field_errors']], [_('Invalid credentials')])
