from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from datetime import datetime, timezone, timedelta

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

    def test_login_failure_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_failure_missing_email(self):
        data = {
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_missing_password(self):
        data = {
            'email': 'jdoe@example.com',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_empty_email(self):
        data = {
            'email': '',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_empty_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_incorrect_email(self):
        data = {
            'email': 'incorrect@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_DOES_NOT_EXIST)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_incorrect_password(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 'incorrect',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INCORRECT_PASSWORD)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_invalid_email_type(self):
        data = {
            'email': 123,
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_invalid_password_type(self):
        data = {
            'email': 'jdoe@example.com',
            'password': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_failure_account_inactive(self):
        self.user.is_active = False
        self.user.save()

        data = {
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_INACTIVE)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_success(self):
        data = {
            'email': ' jDoE@ExamPlE.Com ',
            'password': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue('first_name' in response.data)
        self.assertTrue('last_name' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)
        self.assertTrue('access_token_expiry' in response.data)
        self.assertTrue('refresh_token_expiry' in response.data)

        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jdoe@example.com')

        access_token = AccessToken(response.data['access_token'])
        access_token_expiry = datetime.fromtimestamp(access_token['exp'], tz=timezone.utc).isoformat()
        refresh_token = RefreshToken(response.data['refresh_token'])
        refresh_token_expiry = datetime.fromtimestamp(refresh_token['exp'], tz=timezone.utc).isoformat()

        self.assertEqual(access_token['user_id'], self.user.id)
        self.assertEqual(refresh_token['user_id'], self.user.id)

        self.assertEqual(access_token_expiry, response.data['access_token_expiry'])
        self.assertEqual(refresh_token_expiry, response.data['refresh_token_expiry'])

class TestLoginRenew(APITestCase):

    def setUp(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password': 'ABC123!xyz',
        }

        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

            self.refresh_token = str(RefreshToken.for_user(user))

        self.url = reverse('login_renew')

    def test_login_renew_failure_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_renew_failure_no_refresh_token(self):
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.REFRESH_TOKEN_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_renew_failure_empty_refresh_token(self):
        response = self.client.post(self.url, {
            'refresh_token': '',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.REFRESH_TOKEN_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_renew_failure_invalid_refresh_token(self):
        response = self.client.post(self.url, {
            'refresh_token': 'invalid_refresh_token',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_renew_failure_expired_refresh_token(self):
        refresh_token = RefreshToken(self.refresh_token)

        refresh_token['exp'] = datetime.now(timezone.utc) - timedelta(days=1)

        self.refresh_token = str(refresh_token)

        response = self.client.post(self.url, {
            'refresh_token': self.refresh_token,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_REFRESH_TOKEN)
        self.assertEqual(len(response.data['errors']), 1)

    def test_login_renew_success(self):
        response = self.client.post(self.url, {
            'refresh_token': self.refresh_token,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue('access_token' in response.data)
        self.assertTrue('access_token_expiry' in response.data)

        access_token = AccessToken(response.data['access_token'])
        access_token_expiry = datetime.fromtimestamp(access_token['exp'], tz=timezone.utc).isoformat()

        self.assertEqual(access_token_expiry, response.data['access_token_expiry'])

class TestSignUp(APITestCase):

    def setUp(self):
        self.url = reverse('signup')

    def test_signup_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_first_name(self):
        data = {
            'first_name': ' John ',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': ' Doe ',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': ' JdOe@EXaMple.cOm ',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_success_trailing_space_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': ' ABC123!xyz ',
            'password2': ' ABC123!xyz ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))

    def test_signup_failure_duplicate_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_ALREADY_EXISTS)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_duplicate_email_alternate_case(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        data['email'] = 'jDoE@eXamPlE.Com'

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.ACCOUNT_ALREADY_EXISTS)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_missing_first_name(self):
        data = {
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_missing_last_name(self):
        data = {
            'first_name': 'John',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_missing_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_missing_password1(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD1_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_missing_password2(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD2_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_empty_first_name(self):
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_empty_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': '',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_empty_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_empty_password1(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': '',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD1_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_empty_password2(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': '',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD2_REQUIRED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_passwords_mismatch(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'XYZ123!abc',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORDS_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_first_name_invalid_type(self):
        data = {
            'first_name': 123,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_last_name_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 123,
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_email_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 123,
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password1_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 123,
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD1_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password2_invalid_type(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 123,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD2_TYPE_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_first_name_too_long(self):
        data = {
            'first_name': 'J' * 65,
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.FIRST_NAME_LENGTH_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_last_name_too_long(self):
        data = {
            'first_name': 'John',
            'last_name': 'D' * 65,
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.LAST_NAME_LENGTH_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_email_too_long(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'j' * 181  + '@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.EMAIL_LENGTH_MISMATCH)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_invalid_email_format(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.INVALID_EMAIL_FORMAT)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password_less_than_8_characters(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'Abc123!',
            'password2': 'Abc123!',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password_no_uppercase_character(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'abc123!xyz',
            'password2': 'abc123!xyz',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password_no_lowercase_characters(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123!XYZ',
            'password2': 'ABC123!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password_no_digit_characters(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABCxyz!XYZ',
            'password2': 'ABCxyz!XYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_failure_password_no_special_character(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe2@example.com',
            'password1': 'ABC123xyzXYZ',
            'password2': 'ABC123xyzXYZ',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'][0], core_errors.PASSWORD_TOO_WEAK)
        self.assertEqual(len(response.data['errors']), 1)

    def test_signup_success_is_active_false_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
            'is_active': False,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertTrue(user.is_active)

    def test_signup_success_is_superuser_true_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
            'is_superuser': True,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertFalse(user.is_superuser)

    def test_signup_success_is_staff_true_no_effect(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jdoe@example.com',
            'password1': 'ABC123!xyz',
            'password2': 'ABC123!xyz',
            'is_staff': True,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(email='jdoe@example.com')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('ABC123!xyz'))
        self.assertFalse(user.is_staff)

    def test_signup_failure_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
