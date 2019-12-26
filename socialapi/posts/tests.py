from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from posts.models import Post


class PostTests(APITestCase):

    def test_create_post(self):
        client = APIClient()
        url = 'http://localhost:8000/api/posts/create/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        self.assertEqual(Post.objects.count(), 0)
        client.login(username='ivan', password='ivan1111')
        data = {
            'title': 'hello',
            'text': 'world'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.get().title, 'hello')
        self.assertEqual(Post.objects.get().text, 'world')
        self.assertEqual(Post.objects.count(), 1)

    def test_get_post_list(self):
        client = APIClient()
        url = 'http://localhost:8000/api/posts/all/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        self.assertEqual(Post.objects.count(), 0)
        client.login(username='ivan', password='ivan1111')
        data = {
            'title': 'hello',
            'text': 'world'
        }
        client.post('http://localhost:8000/api/posts/create/', data, format='json')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        data = {
            'title': 'test',
            'text': 'test2'
        }
        client.post('http://localhost:8000/api/posts/create/', data, format='json')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_post_detail(self):
        client = APIClient()
        url = 'http://localhost:8000/api/posts/post/hello/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        self.assertEqual(Post.objects.count(), 0)
        client.login(username='ivan', password='ivan1111')
        data = {
            'title': 'hello',
            'text': 'world'
        }
        client.post('http://localhost:8000/api/posts/create/', data, format='json')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['text'], 'world')

    def test_post_like(self):
        client = APIClient()
        url = 'http://localhost:8000/api/posts/post/hello/like/'
        data = {
            'username': 'ivan',
            'first_name': 'ivan',
            'last_name': 'shan',
            'email': 'Ivan@gmail.com',
            'password': 'ivan1111',
            'password2': 'ivan1111',
        }
        self.client.post('http://localhost:8000/api/accounts/registration/', data, format='json')
        self.assertEqual(Post.objects.count(), 0)
        client.login(username='ivan', password='ivan1111')
        data = {
            'title': 'hello',
            'text': 'world'
        }
        client.post('http://localhost:8000/api/posts/create/', data, format='json')
        response = client.get('http://localhost:8000/api/posts/post/hello/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 0)
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['text'], 'world')
        self.assertEqual(response.data['likes'], 1)
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['text'], 'world')
        self.assertEqual(response.data['likes'], 0)
