# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mixer.backend.django import mixer

from todo.models import ToDo
from todo_api.serializers import SignInSerializer
from todo.serializers import ToDoSerializer

__author__ = 'ad'
__date__ = '20/08/16'


class ToDoAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(ToDoAPITestCase, cls).setUpClass()

        cls.username = 'user'
        cls.password = 'password'
        cls.user = get_user_model().objects.create_user(
            username=cls.username, email='user@todo.com',
            password=cls.password)
        cls.token = Token.objects.create(user=cls.user).key

        cls.todo = mixer.cycle(7).blend('todo.ToDo', created_by=cls.user)

    def test_user_can_authenticate_with_token(self):
        """
        Test that we can authenticate with token
        """
        request_data = SignInSerializer(
            {'username': self.username, 'password': self.password}).data
        response = self.client.post('/auth-token/', data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get('token'))
        self.assertEqual(response.data.get('token'), self.token)

    def test_user_can_get_a_list_of_all_todo(self):
        """
        Test that user can get a list of all his ToDos
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.todo))

    def test_user_can_filter_todo_by_status(self):
        """
        Test that user can get only active or only completed ToDos
        """
        for todo in self.todo[:3]:
            todo.completed = True
            todo.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/todo/active/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

        response = self.client.get('/todo/completed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_user_can_create_todo(self):
        """
        Test that user can create new ToDo
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        request_data = ToDoSerializer({
            'title': 'Create new ToDo via this API'
        }).data
        response = self.client.post('/todo/', data=request_data)
        # Checks that valid status code has been returned
        self.assertEqual(response.status_code, 201)
        # Checks that  objects count has been increased
        todo = ToDo.objects.by_user(self.user)
        self.assertEqual(todo.count(), len(self.todo) + 1)

        # Checks that object with valid `title` and `created_by` values
        # has been created
        try:
            new_todo = ToDo.objects.get(title='Create new ToDo via this API')
        except ToDo.DoesNotExist:
            new_todo = None
        self.assertIsNotNone(new_todo)
        self.assertEqual(new_todo.created_by, self.user)

    def test_user_can_change_todo(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        todo = self.todo[0]
        # Checks that single object can be retrieved
        response = self.client.get('/todo/{}/'.format(todo.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], todo.title)
        # Checks that object can be updated via PUT request
        request_data = {
            'title': todo.title,
            'completed': 'true'
        }
        response = self.client.\
            put('/todo/{}/'.format(todo.id), data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], todo.title)
        self.assertEqual(response.data['completed'], True)

    # User can remove TODOs;
