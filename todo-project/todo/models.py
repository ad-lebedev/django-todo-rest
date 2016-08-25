# coding=utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models

__author__ = 'ad'
__date__ = '25/08/16'


class ToDoQuerySet(models.QuerySet):
    def by_user(self, user=None):
        """
        Gets ToDos by given creator
        :param user: User object
        :return: ToDo queryset
        """
        if user and isinstance(user, User):
            return self.filter(created_by=user)
        else:
            return self.none()

    def completed(self):
        """
        Gets ToDos where `completed` is True
        :return: ToDo queryset
        """
        return self.filter(completed=True)

    def active(self):
        """
        Gets ToDos where `completed` is False
        :return: ToDo queryset
        """
        return self.filter(completed=False)


@python_2_unicode_compatible
class ToDo(models.Model):
    """
    Main application class
    """
    title = models.CharField(
        _('Заголовок'),
        max_length=128)
    completed = models.BooleanField(
        _('Выполнено'),
        default=False)
    created = models.DateTimeField(
        _('Создано'),
        auto_now_add=True)
    changed = models.DateTimeField(
        _('Изменено'),
        auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Создатель'),
        on_delete=models.CASCADE)

    objects = ToDoQuerySet.as_manager()

    def __str__(self):
        return '{} ({})'.format(
            self.title, self.created_by.username)
