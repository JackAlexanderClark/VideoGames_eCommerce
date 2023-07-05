from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from django.shortcuts import render, redirect
from django.test import TestCase, Client
from django.urls import reverse
from shipping.models import Order
from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    @patch('django.http.request.HttpRequest')
    def test_login_view_valid_credentials(self, mock_request):
        mock_request.method = 'POST'
        mock_request.POST = {'username': self.username, 'password': self.password}

        response = self.client.post(reverse('login_view'), {'username': self.username, 'password': self.password})

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))

    @patch('django.http.request.HttpRequest')
    def test_login_view_invalid_credentials(self, mock_request):
        mock_request.method = 'POST'
        mock_request.POST = {'username': 'wronguser', 'password': 'wrongpassword'}

        response = self.client.post(reverse('login_view'), {'username': 'wronguser', 'password': 'wrongpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/login.html')
        self.assertEqual(response.context['message'], 'Invalid credentials')

    @patch('django.http.request.HttpRequest')
    def test_login_view_get_request(self, mock_request):
        mock_request.method = 'GET'

        response = self.client.get(reverse('login_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/login.html')


