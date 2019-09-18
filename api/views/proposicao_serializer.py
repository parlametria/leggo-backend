from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.proposicao import Proposicao
from api.views.temperatura_historico_serializer import TemperaturaHistoricoSerializer
from api.views.etapa_serializer import EtapasSerializer, EtapasDetailSerializer
from api.utils.filters import get_time_filtered_pauta
from django.db.models import Prefetch


class ProposicaoDetailSerializer(serializers.ModelSerializer):
    etapas = EtapasDetailSerializer(many=True, read_only=True)
    temperatura_historico = TemperaturaHistoricoSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            'id', 'temas', 'apelido', 'etapas', 'resumo_progresso', 'id_leggo',
            'temperatura_historico', 'ultima_temperatura', 'temperatura_coeficiente')


class ProposicaoSerializer(serializers.ModelSerializer):
    etapas = EtapasSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            'id', 'temas', 'apelido', 'etapas', 'resumo_progresso',
            'ultima_temperatura', 'temperatura_coeficiente', 'id_leggo')


class ProposicaoList(generics.ListAPIView):
    '''
    Lista de proposições e seus dados gerais.
    '''
    serializer_class = ProposicaoSerializer

    def get_queryset(self):
        pautaQs = get_time_filtered_pauta(self.request)
        props = Proposicao.objects.prefetch_related(
            'etapas', 'etapas__tramitacao', 'progresso',
            Prefetch('etapas__pauta_historico', queryset=pautaQs),
        )
        return props


class ProposicaoDetail(generics.ListAPIView):
    '''
    Detalha proposição.
    '''
    serializer_class = ProposicaoDetailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return Proposicao.objects.filter(id_leggo=id_prop)