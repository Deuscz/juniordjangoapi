from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import Account


class AccountTests(APITestCase):

    def setUp(self):
        Account.objects.create(username="roman", first_name="Roman", last_name="Snihyr", email="Robert355335@gmail.com",
                               password="roman1111")

    def test_create_account(self):
        self.assertEqual(Account.objects.count(), 1)
        url = 'http://localhost:8000/api/accounts/registration/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Account.objects.get(pk=1).first_name, 'Roman')

    def test_get_users_list(self):
        client = APIClient()
        url = 'http://localhost:8000/api/accounts/registration/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        response = self.client.post(url, data, format='json')
        url = 'http://localhost:8000/api/accounts/all-accounts/'
        client.login(username='ivan', password='ivan1111')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'Roman')
        self.assertEqual(response.data[1]['first_name'], 'ivan')
        self.assertEqual(len(response.data), 2)

    def test_get_user_detail(self):
        client = APIClient()
        url = 'http://localhost:8000/api/accounts/registration/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        response = self.client.post(url, data, format='json')
        url = 'http://localhost:8000/api/accounts/all-accounts/Robert355335@gmail.com/'
        client.login(username='ivan', password='ivan1111')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Roman')
        self.assertEqual(response.data['last_name'], 'Snihyr')
        self.assertEqual(response.data['email'], 'Robert355335@gmail.com')

    def test_get_user_login_logout(self):
        client = APIClient()
        url = 'http://localhost:8000/api-auth/login/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        response = self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        url = 'http://localhost:8000/api/accounts/all-accounts/Robert355335@gmail.com/'
        client.login(username='ivan', password='ivan1111')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Roman')
        self.assertEqual(response.data['last_name'], 'Snihyr')
        self.assertEqual(response.data['email'], 'Robert355335@gmail.com')
        url = 'http://localhost:8000/api-auth/logout/'
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TokenTest(APITestCase):
    def test_token_obtain_pair(self):
        client = APIClient()
        url = 'http://localhost:8000/api/token/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        response = self.client.post(url, data={'username': 'ivan', 'password': 'ivan1111'}, format='json')
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])

    def test_token_refresh(self):
        client = APIClient()
        url = 'http://localhost:8000/api/token/refresh/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        response = self.client.post('http://localhost:8000/api/token/',
                                    data={'username': 'ivan', 'password': 'ivan1111'}, format='json')
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])
        response = self.client.post(url, data={'username': 'ivan', 'password': 'ivan1111',
                                               'refresh': response.data['refresh']}, format='json')
        self.assertIsNotNone(response.data['access'])
