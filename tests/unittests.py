import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import json
from src.main import app, r

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_update_user_valid(self):
        with patch.object(r, 'set') as mock_redis_set:
            response = self.app.put('/hello/username', data=json.dumps({"dateOfBirth": "1990-01-01"}), content_type='application/json')
            self.assertEqual(response.status_code, 204)
            mock_redis_set.assert_called_with('username', json.dumps({"date_of_birth": "1990-01-01"}))

    def test_update_user_invalid_username(self):
        response = self.app.put('/hello/user123', data=json.dumps({"dateOfBirth": "1990-01-01"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", response.data.decode())

    def test_update_user_invalid_date_of_birth(self):
        response = self.app.put('/hello/username', data=json.dumps({"dateOfBirth": "1990-13-01"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date of birth", response.data.decode())

    def test_get_user_birthday_message_valid(self):
        with patch.object(r, 'get', return_value=json.dumps({"date_of_birth": "1990-01-01"})) as mock_redis_get:
            with patch('your_flask_app.datetime') as mock_datetime:
                mock_datetime.today.return_value = datetime(2024, 1, 1)  # Mock today's date
                response = self.app.get('/hello/username')
                self.assertEqual(response.status_code, 200)
                self.assertIn("Happy birthday", response.json['message'])
                mock_redis_get.assert_called_with('username')

    def test_get_user_birthday_message_not_found(self):
        with patch.object(r, 'get', return_value=None) as mock_redis_get:
            response = self.app.get('/hello/username')
            self.assertEqual(response.status_code, 404)
            self.assertIn("User not found", response.data.decode())
            mock_redis_get.assert_called_with('username')

    def test_get_user_birthday_message_invalid_username(self):
        response = self.app.get('/hello/user123')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", response.data.decode())

if __name__ == '__main__':
    unittest.main()
