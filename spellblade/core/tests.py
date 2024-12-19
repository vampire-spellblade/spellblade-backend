from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from . import models
from . import serializers
from . import errors as core_errors

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
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        self.assertEqual(access_token['user_id'], self.user.id)
        self.assertEqual(refresh_token['user_id'], self.user.id)

    def test_login_missing_email(self):
        data = {
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)

    def test_login_empty_email(self):
        data = {
            'email': '',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)

    def test_login_missing_password(self):
        data = {
            'email': 'jdoe@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)

    def test_login_empty_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)

    def test_login_missing_email_and_password(self):
        data = {}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_empty_email_and_password(self):
        data = {
            'email': '',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_missing_email_and_empty_password(self):
        data = {
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_empty_email_and_missing_password(self):
        data = {
            'email': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_incorrect_email(self):
        data = {
            'email': 'incorrect_email@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_CREDENTIALS)

    def test_login_incorrect_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'incorrect_password',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_CREDENTIALS)

    def test_login_incorrect_email_and_password(self):
        data = {
            'email': 'incorrect_email@example.com',
            'password': 'incorrect_password',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_CREDENTIALS)

    def test_login_invalid_email_type(self):
        data = {
            'email': 123,
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)

    def test_login_invalid_password_type(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_login_invalid_email_and_password_type(self):
        data = {
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_login_success_email_with_different_case(self):
        data = {
            'email': 'jDoE@eXamPlE.Com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        self.assertEqual(access_token['user_id'], self.user.id)
        self.assertEqual(refresh_token['user_id'], self.user.id)

    def test_login_success_email_with_trailing_whitespaces(self):
        data = {
            'email': ' jdoe@example.com ',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        self.assertEqual(access_token['user_id'], self.user.id)
        self.assertEqual(refresh_token['user_id'], self.user.id)

    def test_login_password_with_trailing_whitespaces(self):
        data = {
            'email': 'jdoe@example.com',
            'password': ' ABC123!xyz ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_CREDENTIALS)

    def test_login_mismatch_email_invalid_password(self):
        data = {
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_login_empty_email_invalid_password(self):
        data = {
            'email': '',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_login_invalid_email_missing_password(self):
        data = {
            'email': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_invalid_email_empty_password(self):
        data = {
            'email': 123,
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_REQUIRED)

    def test_login_invalid_email_and_password(self):
        data = {
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.PASSWORD_TYPE_MISMATCH)

class TestLogout(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        user = self.client.post(reverse('sign_up'), data, format='json')

        self.access_token = AccessToken(user.data['access_token'])
        self.refresh_token = RefreshToken(user.data['refresh_token'])

        self.url = reverse('logout')

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {
            'refresh_token': str(self.refresh_token),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {
            'refresh_token': 'invalid_refresh_token',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)

    def test_logout_missing_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.REFRESH_TOKEN_REQUIRED)

    def test_logout_different_user(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane_doe@example.com',
            'password': 'ABC123!xyz',
        }

        user = self.client.post(reverse('sign_up'), data, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {
            'refresh_token': user.data['refresh_token'],
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)

    def test_logout_not_logged_in(self):
        response = self.client.post(self.url, {
            'refresh_token': str(self.refresh_token),
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
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(access_token['user_id'], user.id)
        self.assertEqual(refresh_token['user_id'], user.id)

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

        response = self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_ALREADY_EXISTS)

    def test_signup_missing_first_name(self):
        data = {
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)

    def test_signup_missing_last_name(self):
        data = {
            'first_name': 'John',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_REQUIRED)

    def test_signup_missing_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)

    def test_signup_missing_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)

    def test_signup_empty_first_name(self):
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)

    def test_signup_empty_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': '',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_REQUIRED)

    def test_signup_empty_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)

    def test_signup_empty_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)

    def test_signup_all_fields_missing(self):
        data = {}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][2], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][3], core_errors.PASSWORD_REQUIRED)

    def test_signup_all_fields_empty(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][2], core_errors.EMAIL_REQUIRED)
        self.assertEqual(response.data['errors'][3], core_errors.PASSWORD_REQUIRED)

    def test_signup_first_name_invalid_type(self):
        data = {
            'first_name': 123,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_TYPE_MISMATCH)

    def test_signup_last_name_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 123,
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_TYPE_MISMATCH)

    def test_signup_email_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 123,
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)

    def test_signup_password_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_signup_all_fields_invalid_type(self):
        data = {
            'first_name': 123,
            'last_name': 123,
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][2], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][3], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_signup_missing_first_name_last_name_invalid_email_password(self):
        data = {
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][2], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][3], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_signup_empty_first_name_last_name_invalid_email_password(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': 123,
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(response.data['errors'][2], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(response.data['errors'][3], core_errors.PASSWORD_TYPE_MISMATCH)

    def test_signup_first_name_too_long(self):
        data = {
            'first_name': 'J' * 65,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_LENGTH_MISMATCH)

    def test_signup_last_name_too_long(self):
        data = {
            'first_name': 'John',
            'last_name': 'D' * 65,
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_LENGTH_MISMATCH)

    def test_signup_first_name_last_name_too_long(self):
        data = {
            'first_name': 'J' * 65,
            'last_name': 'D' * 65,
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_LENGTH_MISMATCH)
        self.assertEqual(response.data['errors'][1], core_errors.LAST_NAME_LENGTH_MISMATCH)

    def test_signup_success_trailing_space_first_name(self):
        data = {
            'first_name': ' John ',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(access_token['user_id'], user.id)
        self.assertEqual(refresh_token['user_id'], user.id)

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
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(access_token['user_id'], user.id)
        self.assertEqual(refresh_token['user_id'], user.id)

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
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(access_token['user_id'], user.id)
        self.assertEqual(refresh_token['user_id'], user.id)

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': ' ABC123!xyz ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe2@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe2@example.com')

        self.assertEqual(access_token['user_id'], user.id)
        self.assertEqual(refresh_token['user_id'], user.id)

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_too_long_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'j' * 181  + '@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_LENGTH_MISMATCH)

    def test_signup_invalid_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_EMAIL_FORMAT)

    def test_signup_password_less_than_8_characters(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'Abc123!',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)

    def test_signup_password_no_uppercase(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'abc123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)

    def test_signup_password_no_lowercase(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)

    def test_signup_password_no_number(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABCxyz!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)

    def test_signup_password_no_special_character(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password': 'ABC123xyzXYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)

    def test_signup_success_email_different_case(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jDoE@eXamPlE.Com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.id, access_token['user_id'])
        self.assertEqual(user.id, refresh_token['user_id'])

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

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
            'email': 'jDoE@eXamPlE.Com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_ALREADY_EXISTS)

    def test_signup_is_active_false_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
            'is_active': False,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.id, access_token['user_id'])
        self.assertEqual(user.id, refresh_token['user_id'])

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertTrue(user.is_active)

    def test_signup_is_superuser_true_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
            'is_superuser': True,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.id, access_token['user_id'])
        self.assertEqual(user.id, refresh_token['user_id'])

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertFalse(user.is_superuser)

    def test_signup_is_staff_true_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
            'is_staff': True,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

        access_token = AccessToken(response.data['access_token'])
        refresh_token = RefreshToken(response.data['refresh_token'])

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.id, access_token['user_id'])
        self.assertEqual(user.id, refresh_token['user_id'])

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertFalse(user.is_staff)

class TestLoginRenew(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        user = self.client.post(reverse('sign_up'), data, format='json')

        self.access_token = AccessToken(user.data['access_token'])
        self.refresh_token = RefreshToken(user.data['refresh_token'])

        self.url = reverse('login_renew')

    def test_login_renew_not_logged_in(self):
        response = self.client.post(self.url, {
            'refresh_token': str(self.refresh_token),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_renew_no_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.REFRESH_TOKEN_REQUIRED)

    def test_login_renew_invalid_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {
            'refresh_token': 'invalid_refresh_token',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)

    def test_login_renew_different_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jane_doe@example.com',
            'password': 'ABC123!xyz',
        }

        user = self.client.post(reverse('sign_up'), data, format='json')

        refresh_token = user.data['refresh_token']

        response = self.client.post(self.url, {
            'refresh_token': refresh_token,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)

    def test_login_renew_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.post(self.url, {
            'refresh_token': str(self.refresh_token),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)

        access_token = AccessToken(response.data['access_token'])

        self.assertEqual(access_token['user_id'], self.access_token['user_id'])
