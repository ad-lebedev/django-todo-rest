# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mixer.backend.django import mixer

from todo_api.serializers import SignInSerializer

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

        cls.todo = mixer.cycle(6).blend('todo.ToDo', created_by=cls.user)

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

    # User can filter TODOs: get only active TODOs or only completed TODOs;
    #
    # User can create new TODOs;
    #
    # User can change TODOs;
    #
    # User can remove TODOs;
    #
    # User can mark TODOs as completed;
    #
    # User can clear all completed TODOs (remove them);
