#!/usr/bin/env python3
"""
Unit tests for the update_password functionality in the Flask app
"""
import unittest
from app import app
from unittest.mock import patch
from auth import Auth


class TestUpdatePassword(unittest.TestCase):
    """Test cases for the /reset_password route"""

    def setUp(self):
        """Set up the test client for the Flask app"""
        self.client = app.test_client()
        self.client.testing = True

    @patch.object(Auth, 'update_password')
    def test_successful_password_update(self, mock_update_password):
        """Test successful password update with valid token"""
        mock_update_password.return_value = None  # Simulate successful update

        # Simulate form data for the PUT request
        response = self.client.put(
            '/reset_password',
            data={
                'email': 'test@example.com',
                'reset_token': 'valid_token',
                'new_password': 'new_password123'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "email": "test@example.com",
            "message": "Password updated"
        })

    @patch.object(Auth, 'update_password')
    def test_invalid_reset_token(self, mock_update_password):
        """Test password update with an invalid reset token"""
        mock_update_password.side_effect = ValueError  # Simulate invalid token

        # Simulate form data for the PUT request with invalid token
        response = self.client.put(
            '/reset_password',
            data={
                'email': 'test@example.com',
                'reset_token': 'invalid_token',
                'new_password': 'new_password123'
            }
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Invalid reset token", response.data)

    def test_missing_form_data(self):
        """Test password update with missing form data"""
        # Simulate form data with missing fields
        response = self.client.put(
            '/reset_password',
            data={
                'email': 'test@example.com',
                'reset_token': 'valid_token'
                # Missing new_password
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing form data", response.data)


if __name__ == "__main__":
    unittest.main()
