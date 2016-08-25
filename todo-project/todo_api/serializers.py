# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

__author__ = 'ad'
__date__ = '20/08/16'


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        read_only = ('username', 'password')
