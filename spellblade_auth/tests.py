from hashlib import sha1
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OutstandingToken

class TestLoginView(APITestCase):

    def setUp(self):
        self.url = reverse('login')

class TestLoginRenewView(APITestCase):

    def setUp(self):
        self.url = reverse('login_renew')

class TestLogoutView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('logout')

        self.token = sha1(str(
            self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'}).data['refresh']
        ).encode()).hexdigest()

    def test_logout_success(self):
        # Arrange
        token = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'}).data['refresh']

        # Act
        response = self.client.post(self.url, {'token': token})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 1)

        try:
            OutstandingToken.objects.get(token=self.token)
        except OutstandingToken.DoesNotExist:
            self.assertRaises(OutstandingToken.DoesNotExist)

    def test_logout_failure_token_not_registered(self):
        # Arrange
        token = str(RefreshToken.for_user(self.user))

        # Act
        response = self.client.post(self.url, {'token': str(token)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)
        self.assertListEqual(response.data['non_field_errors'], [_('Token is invalid.')])

    def test_logout_failure_token_invalid(self):
        # Act
        response = self.client.post(self.url, {'token': 'invalid'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)
        self.assertListEqual(response.data['non_field_errors'], [_('Token is invalid.')])

    def test_logout_empty_token(self):
        # Act
        response = self.client.post(self.url, {'token': ''})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['token']), 1)
        self.assertListEqual(response.data['token'], [_('This field may not be blank.')])

class TestLogoutAllView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('logout_all')

    def test_logout_all_success_single_login(self):
        # Arrange
        token = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'}).data['access']

        # Act
        response = self.client.post(self.url, HTTP_AUTHORIZATION=f'Bearer {token}')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 0)

    def test_logout_all_success_multiple_logins(self):
        # Arrange
        for i in range(3): # Slows down the test.
            self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        token = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'}).data['access']

        # Act
        response = self.client.post(self.url, HTTP_AUTHORIZATION=f'Bearer {token}')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 0)

    def test_logout_all_failure_not_logged_in(self):
        # Act
        response = self.client.post(self.url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
