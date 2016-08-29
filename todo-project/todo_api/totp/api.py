# coding=utf-8
from __future__ import unicode_literals

import pyotp
from django.contrib.auth import login, logout

from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SecretKey
from .serializers import SecretKeySerializer, TOTPSerializer

__author__ = 'ad'
__date__ = '28/08/16'


class ObtainSecretKey(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SecretKeySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        secret_key, created = SecretKey.objects.get_or_create(user=user)
        totp = pyotp.TOTP(secret_key.key)
        url = totp.provisioning_uri(
            '{}@example.com'.format(secret_key.user.username))
        return Response({'url': url})


class TOTPAuthenticate(APIView):
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = TOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=200)


class TOTPLogout(APIView):
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=200)


obtain_secret_key = ObtainSecretKey.as_view()
totp_authenticate = TOTPAuthenticate.as_view()
totp_logout = TOTPLogout.as_view()
