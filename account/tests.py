from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from .models import User

# Create your tests here.
class TestUserModel(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username = 'name', password = 'password', email = 'test@test.com')
        self.assertEqual(user.username, 'name')
        
    def test_login(self):
        User.objects.create_user(username = 'name', password = 'password', email = 'test@test.com')
        c = Client()
        result = c.login(username = 'name', password = 'password')
        self.assertTrue(result)

class TestAccountViews(TestCase):
    def test_register_response_not_logged_in(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_response_logged_in(self):
        client = Client()
        user = User.objects.create_user(username = 'name')
        client.force_login(user)
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_registration(self):
        client = Client()
        response = client.post(reverse('register'), {'username': 'name', 'email': 'test@email.com', 'password1': 'S3CR3T@P4SSW0RD', 'password2': 'S3CR3T@P4SSW0RD'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username = 'name')
        self.assertFalse(user.is_active)
        
    def test_login_response_not_logged_in(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_response_logged_in(self):
        client = Client()
        user = User.objects.create_user(username = 'name')
        client.force_login(user)
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        client = Client()
        User.objects.create_user(username = 'name', password = 'password')
        response = client.post(reverse('login'), {'username': 'name', 'password': 'password'})
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        client = Client()
        user_object = User.objects.create_user(username = 'name')
        client.force_login(user_object)
        user = auth.get_user(client)
        self.assertTrue(user.is_authenticated)
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(client)
        self.assertFalse(user.is_authenticated)