# coding=utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from todo.models import ToDo

__author__ = 'ad'
__date__ = '25/08/16'


class ToDoSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source='created_by.username',
        read_only=True)
    created = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True)
    changed = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True)

    class Meta:
        model = ToDo
        fields = '__all__'
