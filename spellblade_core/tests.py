from django.utils.translation import gettext as _
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

class TestIndexView(APITestCase):

    def setUp(self):
        self.url = reverse('index')

    def test_index_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], _('Hello, World!'))
