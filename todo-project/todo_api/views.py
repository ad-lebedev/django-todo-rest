# coding=utf-8
from __future__ import unicode_literals

from rest_framework import response
from rest_framework import schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer

__author__ = 'ad'
__date__ = '29/08/16'


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='TODO API')
    return response.Response(generator.get_schema(request=request))
