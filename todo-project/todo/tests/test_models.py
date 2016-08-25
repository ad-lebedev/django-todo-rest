# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase

from mixer.backend.django import mixer

from todo.models import ToDo

__author__ = 'ad'
__date__ = '20/08/16'


class ToDoModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ToDoModelTestCase, cls).setUpClass()
        cls.user_one = get_user_model().objects.create_user(
            username='user_one', password='password_one', email='one@todo.com')
        cls.user_two = get_user_model().objects.create_user(
            username='user_two', password='password_two', email='two@todo.com')

        cls.todo_user_one = mixer.cycle(5).\
            blend('todo.ToDo', created_by=cls.user_one)
        cls.todo_user_two = mixer.cycle(3).\
            blend('todo.ToDo', created_by=cls.user_two)

    def test_by_user_queryset_method(self):
        """
        Test that user can get only his own ToDos
        """
        # Tests method without `user` parameter
        todo = ToDo.objects.by_user()
        self.assertQuerysetEqual(todo, ToDo.objects.none())

        # Tests method with given user object
        user_one_todo = ToDo.objects.by_user(self.user_one)
        user_two_todo = ToDo.objects.by_user(self.user_two)

        self.assertEqual(user_one_todo.count(), len(self.todo_user_one))
        self.assertEqual(user_two_todo.count(), len(self.todo_user_two))

    def test_completed_queryset_method(self):
        """
        Test that `completed()` queryset method returns valid count of ToDos
        """
        user_one_todo = ToDo.objects.by_user(self.user_one).completed()
        self.assertEqual(user_one_todo.count(), 0)

        todo = ToDo.objects.by_user(self.user_one).first()
        todo.completed = True
        todo.save()

        self.assertEqual(user_one_todo.count(), 1)

    def test_active_queryset_method(self):
        """
        Test that `active()` queryset method returns valid count of ToDos
        """
        user_one_todo = ToDo.objects.by_user(self.user_one).active()
        self.assertEqual(user_one_todo.count(), len(self.todo_user_one))

        todo = user_one_todo.first()
        todo.completed = True
        todo.save()

        self.assertEqual(user_one_todo.count(), len(self.todo_user_one) - 1)
