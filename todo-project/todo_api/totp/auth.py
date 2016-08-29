# coding=utf-8
from __future__ import unicode_literals

import pyotp

from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed

from todo_api.totp.models import SecretKey

__author__ = 'ad'
__date__ = '29/08/16'


class TOTPAuthentication(object):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if user and user.is_authenticated():
            return user, None

        username = request.data.get('username')
        password = request.data.get('password')
        totp = request.data.get('totp')
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
                return user, None
            else:
                raise AuthenticationFailed('Invalid one time password.')

    def authenticate_header(self, request):
        return 'TOTP realm="%s"' % self.www_authenticate_realm
