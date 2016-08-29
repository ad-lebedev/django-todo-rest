# coding=utf-8
from __future__ import unicode_literals

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from todo.models import ToDo
from todo.serializers import ToDoSerializer

__author__ = 'ad'
__date__ = '25/08/16'


class ToDoViewSet(ModelViewSet):
    model = ToDo
    serializer_class = ToDoSerializer
    queryset = model.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.model.objects.by_user(user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance in self.model.objects.by_user(user):
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        else:
            return Response()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    @list_route(methods=['get'])
    def completed(self, request):
        user = self.request.user
        queryset = self.model.objects.by_user(user).completed()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def active(self, request):
        user = self.request.user
        queryset = self.model.objects.by_user(user).active()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
