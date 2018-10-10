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
    url(r'^proposicoes/?$', views.ProposicaoList.as_view()),
    url(r'^etapas/?$', views.EtapasList.as_view()),
    url(r'^energia/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.EnergiaHistoricoList.as_view()),
    url(r'^proposicoes/(?P<id_ext>[0-9]+)/fases/?$', views.Info.as_view()),
    url(r'^progresso/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.ProgressoList.as_view()),
]
