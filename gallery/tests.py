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

# test stripe API


import unittest
from unittest.mock import patch, MagicMock
import stripe_payment   # noqa

class TestStripePayment(unittest.TestCase):
    @patch('stripe.Token.create')
    def test_generate_card_token(self, mock_create):
        mock_create.return_value = {'id': 'test_id'}

        stripe = MagicMock()
        cardnumber = 1234567812345678
        expmonth = 11
        expyear = 29
        cvv = 233

        result = stripe_payment.generate_card_token(stripe, cardnumber, expmonth, expyear, cvv)

        self.assertEqual(result, 'test_id')

    @patch('stripe.Charge.create')
    def test_create_payment_charge(self, mock_create):
        mock_create.return_value = {'paid': True}

        stripe = MagicMock()
        tokenid = 'test_id'
        amount = 100
        description = 'test'

        result = stripe_payment.create_payment_charge(stripe, tokenid, amount, description)

        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()