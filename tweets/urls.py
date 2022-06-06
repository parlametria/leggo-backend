from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from tweets.views import TweetsViewSet, PressaoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"tweets", TweetsViewSet, basename='tweets')
router.register(r"pressao", PressaoViewSet, basename='pressao')

# urlpatterns = [
#     path("", include(router.urls)),
# ]
