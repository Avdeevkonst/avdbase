from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse

from avddisk.models import Profile

# class SigninTest(TestCase):
#     def setUp(self):
#         self.valid_data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'testpassword',
#             'password2': 'testpassword',
#         }
#         self.invalid_data = {
#             'username': '',
#             'email': 'invalidemail',
#             'password1': '',
#             'password2': '',
#         }
#         Profile.objects.create_user(
#             username='existinguser',
#             email='existinguser@example.com',
#             password='existingpassword'
#         )
#
#
#     def test_wrong_username(self):
#         user = authenticate(first_name='wrong', password='12test12')
#         self.assertFalse(user is not None and user.is_authenticated)
#
#     def test_wrong_password(self):
#         user = authenticate(first_name='test', password='wrong')
#         self.assertFalse(user is not None and user.is_authenticated)
#
#     def test_valid_registration(self):
#         response = self.client.post(reverse('registration'), data=self.valid_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(Profile.objects.filter(username=self.valid_data['username']).exists())

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': '',
            'password2': '',
        }
        Profile.objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            password='existingpassword'
        )

    def test_valid_registration(self):
        response = self.client.post(reverse('registration'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(username=self.valid_data['username']).exists())

    def test_invalid_registration(self):
        response = self.client.post(reverse('registration'), data=self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Profile.objects.filter(username=self.invalid_data['username']).exists())

    def test_existing_email(self):
        self.valid_data['email'] = 'existinguser@example.com'
        response = self.client.post(reverse('registration'), data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Profile.objects.filter(username=self.valid_data['username']).exists())
