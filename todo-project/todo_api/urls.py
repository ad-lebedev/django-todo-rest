from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views as auth_token
from rest_framework import routers

from todo.api import ToDoViewSet
from todo_api.totp import api as auth_totp

router = routers.SimpleRouter()
router.register(r'todo', ToDoViewSet)

urlpatterns = [
    url(r'^auth-token/', auth_token.obtain_auth_token),
    url(r'^auth-totp/register/', auth_totp.obtain_secret_key),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
