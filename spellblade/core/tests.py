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
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

        user = self.client.post(reverse('login'), {
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }, format='json')

        self.url = reverse('logout')

        self.refresh_token = user.data['user']['refresh_token']
        self.access_token = user.data['user']['access_token']

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(self.url, {
            'refresh_token': self.refresh_token,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Logout successful'))

    def test_logout_invalid_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(self.url, {
            'refresh_token': 'invalid_refresh_token',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Invalid refresh token'))

    def test_logout_missing_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Refresh token required'))

    def test_logout_different_user(self):
        serializer = serializers.UserSerializer(data={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane_doe@example.com',
            'password': 'ABC123!xyz',
        })

        if serializer.is_valid():
            serializer.save()

        user = self.client.post(reverse('login'), {
            'email': 'jane_doe@example.com',
            'password': 'ABC123!xyz',
        }, format='json')

        refresh_token_2 = user.data['user']['refresh_token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(self.url, {
            'refresh_token': refresh_token_2,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Invalid refresh token'))

    def test_logout_not_logged_in(self):
        response = self.client.post(self.url, {
            'refresh_token': self.refresh_token,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestSignUp(APITestCase):

    def setUp(self):
        self.url = reverse('sign_up')

    def test_signup_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Signup successful'))
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_duplicate_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        self.client.post(self.url, data, format='json')

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Account already exists'))

    def test_signup_missing_first_name(self):
        data = {
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('First name required'))

    def test_signup_missing_last_name(self):
        data = {
            'first_name': 'John',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Last name required'))

    def test_signup_missing_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))

    def test_signup_missing_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password required'))

    def test_signup_empty_first_name(self):
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('First name required'))

    def test_signup_empty_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': '',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Last name required'))

    def test_signup_empty_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email required'))

    def test_signup_empty_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password required'))

    def test_signup_first_name_invalid_type(self):
        data = {
            'first_name': 123,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('First name must be a string'))

    def test_signup_last_name_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 123,
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Last name must be a string'))

    def test_signup_email_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 123,
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email must be a string'))

    def test_signup_password_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be a string'))

    def test_signup_first_name_too_short(self):
        data = {
            'first_name': 'J',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('First name must be between 2 and 64 characters'))

    def test_signup_last_name_too_short(self):
        data = {
            'first_name': 'John',
            'last_name': 'D',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Last name must be between 2 and 64 characters'))

    def test_signup_first_name_too_long(self):
        data = {
            'first_name': 'J' * 65,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('First name must be between 2 and 64 characters'))

    def test_signup_last_name_too_long(self):
        data = {
            'first_name': 'John',
            'last_name': 'D' * 65,
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Last name must be between 2 and 64 characters'))

    def test_signup_success_trailing_space_first_name(self):
        data = {
            'first_name': ' John ',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': ' Doe ',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': ' jdoe2@example.com ',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')
        self.assertEqual(response.data['user']['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data['user'])
        self.assertTrue('refresh_token' in response.data['user'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_too_short_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'j@',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email must be between 3 and 192 characters'))

    def test_signup_too_long_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'j' * 181  + '@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email must be between 3 and 192 characters'))

    def test_signup_invalid_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Email is invalid'))

    def test_signup_password_less_than_8_characters(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'Abc123!',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    def test_signup_password_no_uppercase(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'abc123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    def test_signup_password_no_lowercase(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    def test_signup_password_no_number(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABCxyz!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    def test_signup_password_no_special_character(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123xyzXYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'))

    def test_signup_duplicate_email_different_case(self):
        serializer = serializers.UserSerializer(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        })

        if serializer.is_valid():
            serializer.save()

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'JDOE@eXamplE.Com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], _('Account already exists'))

class TestLoginRenew(APITestCase):

    def setUp(self):
        self.url = reverse('login_renew')
