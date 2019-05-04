from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """Test creating a new user with email is succsefull"""
        email = 'test@london.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalised(self):
        """Test the email for the new user is normalized"""
        email = 'test@LONDON.com'
        user = get_user_model().objects.create_user(
            email,
            'test1234'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with invalid email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'test12345'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@something.com',
            'test123'
        )
        self.assertTrue(user.is_superuser, True)
        self.assertTrue(user.is_staff, True)
