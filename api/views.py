from django.shortcuts import get_object_or_404
from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.models import Proposicao, EnergiaHistorico, Progresso
from datetime import datetime, timedelta


class ProposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposicao
        fields = (
            'id', 'id_ext', 'casa', 'sigla', 'data_apresentacao', 'ano', 'sigla_tipo',
            'regime_tramitacao', 'forma_apreciacao', 'ementa', 'justificativa', 'url',
            'energia', 'autor_nome', 'em_pauta', 'apelido', 'tema', 'resumo_tramitacao', 'resumo_progresso')

class EnergiaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergiaHistorico
        fields = ('periodo', 'energia_recente', 'energia_periodo')

class ProgressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progresso
        fields = ('fase_global', 'local', 'data_inicio', 'data_fim', 'local_casa')


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''
    def get(self, request, format=None):
        return Response({'status': 'ok'})


class ProposicaoList(generics.ListAPIView):
    '''
    Dados gerais da proposição.
    '''
    queryset = Proposicao.objects.prefetch_related('tramitacao', 'energia_historico', 'progresso')
    serializer_class = ProposicaoSerializer

class EnergiaHistoricoList(generics.ListAPIView):
    '''
    Dados de energia da proposição por periodo de acordo com uma data de referência.
    '''
    serializer_class = EnergiaHistoricoSerializer
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'semanas_anteriores', openapi.IN_PATH, 'número de semanas anteriores a retornar',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_referencia', openapi.IN_PATH, 'data de referência a ser considerada',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna o histórico de energias de uma proposição, retornando a quantidade especificada de semanas anteriores à data de referência.
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        semanas_anteriores = self.request.query_params.get('semanas_anteriores', None)
        data_referencia = self.request.query_params.get('data_referencia', None)
        queryset = EnergiaHistorico.objects.filter(proposicao__casa=casa, proposicao__id_ext=id_ext)

        try:
            hoje = datetime.today() if data_referencia is None else datetime.strptime(data_referencia, '%Y-%m-%d')
        except:
            print("Data de referência (" + data_referencia + ") inválida. Utilizando data atual como data de referência.")
            hoje = datetime.today()

        queryset = queryset.filter(periodo__lte=hoje)
        
        if semanas_anteriores is not None:
            start_date = hoje - timedelta(weeks=int(semanas_anteriores))
            queryset = queryset.filter(periodo__gte=start_date)
        return queryset


class ProgressoList(generics.ListAPIView):
    '''
    Dados do progresso da proposição por periodo de acordo com uma data de referência.
    '''
    serializer_class = ProgressoSerializer
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_referencia', openapi.IN_PATH, 'data de referência a ser considerada',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna o progresso de uma proposição, passando uma data de referência.
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        data_referencia = self.request.query_params.get('data_referencia', None)
        queryset = Progresso.objects.filter(proposicao__casa=casa, proposicao__id_ext=id_ext)

        try:
            hoje = datetime.today() if data_referencia is None else datetime.strptime(data_referencia, '%Y-%m-%d')
        except:
            print("Data de referência (" + data_referencia + ") inválida. Utilizando data atual como data de referência.")
            hoje = datetime.today()

        queryset = queryset.filter(data_inicio__lte=hoje)
               
        return queryset

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
