from django.conf.urls import url  # , include
# from rest_framework.routers import DefaultRouter
from api import views

# router = DefaultRouter()
# router.register(r'proposicoes', views.ProposicaoViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^info/?$', views.Info.as_view()),
    url(r'^proposicoes/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.ProposicaoDetail.as_view()),
    url(r'^proposicoes/?$', views.ProposicaoList.as_view())
]
