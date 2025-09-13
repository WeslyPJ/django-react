from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse


class HelloYouViewTest(APITestCase):
    def setUp(self):
        """Set up test user and authentication"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
    def test_helloyou_with_authentication(self):
        """Test HelloYou endpoint with proper authentication"""
        url = reverse('helloyou')
        data = {'name': 'World'}
        
        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Hello World!')
        
    def test_helloyou_without_authentication(self):
        """Test HelloYou endpoint without authentication (should fail)"""
        url = reverse('helloyou')
        data = {'name': 'World'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_helloyou_with_empty_name(self):
        """Test HelloYou endpoint with empty name"""
        url = reverse('helloyou')
        data = {'name': ''}
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Hello !')
