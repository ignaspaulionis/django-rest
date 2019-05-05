from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the uers API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating with valid payload is successful"""
        payload = {
            'email': 'test@ignas.lt',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exits(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@ignas.lt',
            'password': 'testpass',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'test11@ignas.lt',
            'password': '12',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        users_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(users_exists)

    def test_create_token_for_user(self):
        """Test tht toekn is created for user"""
        payload = {
            'email': 'test@ignas.lt',
            'password': 'testpass123',
            'name': 'Test name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that invalid credentials do not supply token"""
        payload = {
            'email': 'test@ignas.lt',
            'password': 'testpass123',
            'name': 'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_token_is_not_created_if_user_does_not_exist(self):
        """Test that token is not given for the non existing user"""
        payload = {
            'email': 'test@ignas.lt',
            'password': 'testpass123',
            'name': 'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_token_is_not_created_if_user_is_not_supplied(self):
        """Test that email and password are required"""
        payload = {
            'email': '',
            'password': '',
            'name': 'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
