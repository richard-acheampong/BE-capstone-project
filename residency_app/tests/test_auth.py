from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class TestAuthEndpoints(APITestCase):

    def test_user_registration(self):
        url = reverse('register')  
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "role": "resident",
        }
        response = self.client.post(url, data)
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
       

    def test_user_login(self):
        # First create a user
        user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="loginpass123",
            role="Resident",
        )
        url = reverse('login')  
        data = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_wrong_password(self):
    # First, create a user
        user = User.objects.create_user(
        username="wrongpassuser",
        email="wrongpass@example.com",
        password="correctpassword123",
        role="Resident",
        )
        url = reverse('login')
        data = {
             "username": "wrongpassuser",
            "password": "wrongpassword123" 
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
