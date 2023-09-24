from django.test import TestCase


# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.factories import UserFactory, CollectionFactory

class UserViewSetTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('user-register')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        user = UserFactory()
        url = reverse('user-login')
        data = {'username': user.username, 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

class CollectionViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_collection(self):
        url = reverse('collection-list')
        data = {'title': 'Test Collection', 'description': 'Test Description', 'movies': [{'uuid': 'uuid1'}]}

        # data = {
        # "title": "Title of the collection sep 24",
        # "description": "All-time Favorite",
        # "movies": [
        #     {
        #         "title": "Shadow of the Blair Witch",
        #         "description": "In this true-crime documentary...",
        #         "genres": ["Mystery", "Horror"],
        #         "uuid": "bcacfa33-a886-4ecb-a62a-6bbcb9d9509d"
        #     },
        #     {
        #         "title": "House of Horrors",
        #         "description": "An unsuccessful sculptor saves a madman named...",
        #         "genres": ["Horror", "Mystery", "Thriller"],
        #         "uuid": "388c99da-0cba-4ff0-a528-faea153b43c3"
        #     }
        # ]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_collections(self):
        collection = CollectionFactory(user=self.user)
        url = reverse('collection-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], collection.title)

    def test_get_collection_detail(self):
        collection = CollectionFactory(user=self.user)
        url = reverse('collection-detail', args=[str(collection.collection_ting)])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], collection.title)

    def test_update_collection(self):
        collection = CollectionFactory(user=self.user)
        url = reverse('collection-detail', args=[str(collection.collection_ting)])
        data = {'title': 'Updated Collection'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Collection')
