from django.shortcuts import get_object_or_404
# from django.db.models import Prefetch
from rest_framework import serializers, generics  # , viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.models import Proposicao  # , TramitacaoEvent


class ProposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposicao
        fields = (
            'id', 'id_ext', 'casa', 'sigla', 'data_apresentacao', 'ano', 'sigla_tipo',
            'regime_tramitacao', 'forma_apreciacao', 'ementa', 'justificativa', 'url',
            'resumo_tramitacao', 'energia', 'autor_nome')


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''
    def get(self, request, format=None):
        return Response({'status': 'ok'})


class ProposicaoList(generics.ListAPIView):
    queryset = Proposicao.objects.prefetch_related('tramitacao')
    # queryset = Proposicao.objects.prefetch_related(
    #     Prefetch(
    #         'tramitacao',
    #         TramitacaoEvent.objects.order_by().distinct('proposicao', 'sigla_local')
    #     )
    # )
    serializer_class = ProposicaoSerializer


class ProposicaoDetail(APIView):
    '''
    Detalha proposição.
    '''

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, casa, id_ext, format=None):
        prop = get_object_or_404(Proposicao, casa=casa, id_ext=id_ext)
        return Response(ProposicaoSerializer(prop).data)


# Talvez valha a pena usar ViewSets ao invés de APIView, mas não consegui
# achar um jeito bom de tratar as nested-routes (/proposicoes/{casa}/{id})
# Por outro lado, segundo o padrão REST, talvez fosse bom não fazer isso.
# Deixo referências para avaliarmos melhor abaixo.
# https://stackoverflow.com/questions/21365906/rest-calls-with-multiple-lookup-fields-for-reverse-lookup
# https://stackoverflow.com/questions/27463055/django-rest-framework-add-a-viewset-as-detail-on-another-viewset
# https://chibisov.github.io/drf-extensions/docs/#nested-routes
# class ProposicaoViewSet(viewsets.ReadOnlyModelViewSet):
#     '''
#     This viewset automatically provides `list` and `detail` actions.
#     '''
#     queryset = Proposicao.objects.all()
#     serializer_class = ProposicaoSerializer
