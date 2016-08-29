# coding=utf-8
from __future__ import unicode_literals

import pyotp
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from todo_api.totp.models import SecretKey

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


class TOTPSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'})
    totp = serializers.CharField(
        label=_("TOTP"))

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        totp = attrs.get('totp')

        if not username or not password or not totp:
            raise AuthenticationFailed(
                'Invalid request. No credentials provided.')
        credentials = {
            get_user_model().USERNAME_FIELD: username,
            'password': password
        }
        user = authenticate(**credentials)
        if user is None:
            raise AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        try:
            secret_key = SecretKey.objects.get(user=user)
        except SecretKey.DoesNotExist:
            raise AuthenticationFailed(_('Invalid authentication method. '
                                         'Enable OPT authentication first'))
        else:
            valid_totp = pyotp.TOTP(secret_key.key)
            if valid_totp.now() == totp:
                attrs['user'] = user
                return attrs
            else:
                raise AuthenticationFailed('Invalid one time password.')
