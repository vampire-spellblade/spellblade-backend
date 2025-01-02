# pylint: disable=missing-module-docstring
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
#from .. import serializers

class TestIndexView(APITestCase): # pylint: disable=missing-class-docstring

    def setUp(self):
        self.index = reverse('index')

    def test_index_view_success(self): # pylint: disable=missing-function-docstring
        response = self.client.get(self.index)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello, World!')
