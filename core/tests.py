from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import Profile


class UserRegistrationTests(APITestCase):
    url = reverse('core:register')

    def test_register_user(self):
        """
        Ensure we can register a new user profile
        """

        data = {'username': 'some_username', 'email': 'some_email@gmail.com', 'password': 'some_password'}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user.username, 'some_username')

    def test_email_required(self):
        """
        Ensure that email field is required and cannot be submitted blank
        """

        data = {'username': 'some_username', 'email': '', 'password': 'some_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Profile.objects.count(), 0)

        data = {'username': 'some_username', 'password': 'some_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Profile.objects.count(), 0)

    def test_unique_email(self):
        """
        Test unique validation of email
        """
        # Register first user
        data = {'username': 'some_username', 'email': 'some_email@gmail.com', 'password': 'some_password'}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user.username, 'some_username')
        # Register another user with same email
        data = {'username': 'some_other_username', 'email': 'some_email@gmail.com',
                'password': 'some_password'}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "A user with that email already exists.")
