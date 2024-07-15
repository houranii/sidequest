import unittest
from src.main import app, r
import json
from unittest.mock import patch
from datetime import datetime

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.main.r')
    def test_update_user_valid(self, mock_redis):
        response = self.app.put('/hello/johndoe', data=json.dumps({"dateOfBirth": "1990-01-01"}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        mock_redis.set.assert_called_with('johndoe', json.dumps({"date_of_birth": "1990-01-01"}))

    @patch('src.main.r')
    def test_update_user_invalid_username(self, mock_redis):
        response = self.app.put('/hello/john123', data=json.dumps({"dateOfBirth": "1990-01-01"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", response.data.decode())

    @patch('src.main.r')
    def test_update_user_invalid_date_of_birth(self, mock_redis):
        response = self.app.put('/hello/johndoe', data=json.dumps({"dateOfBirth": "1990-13-01"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date of birth", response.data.decode())

    @patch('src.main.r')
    def test_get_user_birthday_message_valid(self, mock_redis):
        mock_redis.get.return_value = json.dumps({"date_of_birth": "1990-01-01"})
        with patch('src.main.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime(2024, 1, 1)  # Mock today's date
            response = self.app.get('/hello/johndoe')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Happy birthday", response.json['message'])

    @patch('src.main.r')
    def test_get_user_birthday_message_not_found(self, mock_redis):
        mock_redis.get.return_value = None
        response = self.app.get('/hello/johndoe')
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.data.decode())

    def test_get_user_birthday_message_invalid_username(self):
        response = self.app.get('/hello/john123')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", response.data.decode())

if __name__ == '__main__':
    unittest.main()
