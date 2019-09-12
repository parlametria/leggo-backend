from django.conf.urls import url  # , include
# from rest_framework.routers import DefaultRouter
from api.views.info_serializer import Info
from api.views.proposicao_serializer import ProposicaoDetail, ProposicaoList
from api.views.etapa_serializer import EtapasList
from api.views.tramitacao_serializer import TramitacaoEventList
from api.views.progresso_serializer import ProgressoList
from api.views.comissao_serializer import ComissaoList
from api.views.pauta_serializer import PautaList
from api.views.emenda_serializer import EmendasList
from api.views.ator_serializer import AtoresList
from api.views.pressao_serializer import PressaoList

# router = DefaultRouter()
# router.register(r'proposicoes', views.ProposicaoViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^info/?$', Info.as_view()),
    url(r'^proposicoes/(?P<id>[0-9]+)/?$',
        ProposicaoDetail.as_view()),
    url(r'^proposicoes/?$', ProposicaoList.as_view()),
    url(r'^etapas/?$', EtapasList.as_view()),
    # url(r'^temperatura/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
    #     views.TemperaturaHistoricoAPI.as_view()),
    url(r'^eventos_tramitacao/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        TramitacaoEventList.as_view()),
    url(r'^eventos_tramitacao/?$', TramitacaoEventList.as_view()),
    url(r'^proposicoes/(?P<id_ext>[0-9]+)/fases/?$', Info.as_view()),
    url(r'^progresso/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        ProgressoList.as_view()),
    url(r'^comissao/(?P<casa>[a-z]+)/(?P<sigla>([a-z]+|[A-Z]+)[0-9]*)/?$',
        ComissaoList.as_view()),
    url(r'^pauta/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        PautaList.as_view()),
    url(r'^emenda/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        EmendasList.as_view()),
    url(r'^atores/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        AtoresList.as_view()),
    url(r'^pressao/(?P<casa>[a-z]+)/(?P<id_ext>[0-9]+)/?$',
        PressaoList.as_view()),
]
