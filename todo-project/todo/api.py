# coding=utf-8
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from todo.models import ToDo
from todo.serializers import ToDoSerializer

__author__ = 'ad'
__date__ = '25/08/16'


class ToDoViewSet(ModelViewSet):
    model = ToDo
    serializer_class = ToDoSerializer
    queryset = model.objects.none()

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.model.objects.by_user(user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)