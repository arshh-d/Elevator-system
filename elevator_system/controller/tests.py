"""test cases for controller app
    """
import json
from django.test import TestCase
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework.test import APIClient


class ControllerViewTestCase(TestCase):

    CLIENT = APIClient()

    def test_create_elevator_system(self):
        """test create elevator_system init view.
        """
        mock_create_elevators = "controller.views.create_elevators"
        mock_return_value = True
        data = {
            "system_id": "10",
            "system_name": "apt1",
            "max_floor": 12,
            "elevator_count": 4
        }
        client = self.CLIENT

        with patch(mock_create_elevators, side_effect=Mock(return_value=mock_return_value)):
            response = client.post(
                reverse('create_elevator_system'), data=data, format="json")
            response_content = json.loads(response.content)
            self.assertEqual(response_content["msg"], "created elevator")
            self.assertEqual(response.status_code, 200)

    def test_get_all_elevators(self):
        """test fetch all elevators for an elevator_system view
        """
        client = self.CLIENT
        url = "/controller/get_system/10/"
        response = client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_get_elevator(self):
        """test get single elevator view.
        """
        client = self.CLIENT
        url = "/controller/get_elevator/10/2/"
        response = client.get(path=url)
        self.assertEqual(response.status_code, 200)
