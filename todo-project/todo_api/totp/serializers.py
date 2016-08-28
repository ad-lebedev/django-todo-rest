# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

__author__ = 'ad'
__date__ = '28/08/16'


class SecretKeySerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
