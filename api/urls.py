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
    # url(r'^temperatura/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
    #     views.TemperaturaHistoricoAPI.as_view()),
    url(r'^eventos_tramitacao/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.TramitacaoEventList.as_view()),
    url(r'^eventos_tramitacao/?$', views.TramitacaoEventList.as_view()),
    url(r'^proposicoes/(?P<id_ext>[0-9]+)/fases/?$', views.Info.as_view()),
    url(r'^progresso/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.ProgressoList.as_view()),
    url(r'^comissao/(?P<casa>[a-z]+)/(?P<sigla>([a-z]+|[A-Z]+)[0-9]*)/?$',
        views.ComissaoList.as_view()),
    url(r'^pauta/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.PautaList.as_view()),
    url(r'^emenda/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.EmendasList.as_view()),
    url(r'^atores/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        views.AtoresList.as_view()),
]
