# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import SecretKey

__author__ = 'ad'
__date__ = '28/08/16'


@register(SecretKey)
class SecretKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user', )
    ordering = ('-created', )
