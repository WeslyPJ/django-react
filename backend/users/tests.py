from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse


class UserModelTest(TestCase):
    def test_user_creation(self):
        """Test user creation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))


class AuthenticationTest(APITestCase):
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_token_creation(self):
        """Test that token is created for user"""
        token = Token.objects.create(user=self.user)
        self.assertIsNotNone(token.key)
        self.assertEqual(token.user, self.user)
