from posixpath import basename
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from tweets.views import TweetsViewSet, PressaoViewSet, EngajamentoViewSet, ParlamentarPefilViewSet, TweetsInfoViewSet
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'^tweets/info/', TweetsInfoViewSet, basename="info")
# router.register(r'^tweets/', TweetsViewSet, basename="tweets")
# router.register(r'^pressao/', PressaoViewSet, basename="pressao")
# router.register(r'^engajamento/', EngajamentoViewSet, basename="engajamento")
# router.register(r'^parlamentar-perfil/', ParlamentarPefilViewSet,
#                 basename="parlamentar-perfil")
app_name = 'tweets'
urlpatterns = [
    # path("", include(router.urls)),
    path("tweets/info/", TweetsInfoViewSet),
    path("tweets/", TweetsViewSet),
    path("pressao/", PressaoViewSet),
    path("engajamento/", EngajamentoViewSet),
    path("parlamentar-perfil/", ParlamentarPefilViewSet)
]
