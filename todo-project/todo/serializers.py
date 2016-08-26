# coding=utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from todo.models import ToDo

__author__ = 'ad'
__date__ = '25/08/16'


class ToDoSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True)
    changed = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True)

    class Meta:
        model = ToDo
        exclude = ('created_by', )
