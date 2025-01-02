from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from . import serializers

class TestIndexView(APITestCase):

    def test_index_view_success(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello, World!')
