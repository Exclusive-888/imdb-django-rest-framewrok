"""default router/urlpatterns"""
from django.urls import include, path

from rest_framework import routers

from users.models import User
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
