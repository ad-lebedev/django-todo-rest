from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework import routers

from todo.api import ToDoViewSet

router = routers.SimpleRouter()
router.register(r'todo', ToDoViewSet)

urlpatterns = [
    url(r'^auth-token/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]


