from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

class TestSignUp(APITestCase):

    def setUp(self):
        self.url = reverse('signup')

    def test_signup_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        self.assertIn(
            _(
                'Username must be between 1 and 20 characters, and can only contain letters, numbers, hyphens, '
                'and periods. It can\'t start with a number or a special character, end with a special character, '
                'or contain consecutive special characters.'
            ),
            response.data['username']
        )
        self.assertIn(
            _('Your password must contain at least 8 characters.'),
            response.data['password']
        )
        self.assertIn(
            _('Your password can’t be entirely numeric.'),
            response.data['password']
        )
        self.assertIn(
            _('Your password can’t be too similar to your other personal information.'),
            response.data['password']
        )
        self.assertTrue(len(response.data['username']) == 1)
        self.assertTrue(len(response.data['password']) == 3)
