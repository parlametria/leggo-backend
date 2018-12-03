from django.shortcuts import get_object_or_404
from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.models import (
    EtapaProposicao, TemperaturaHistorico,
    Progresso, Proposicao, PautaHistorico)
from datetime import datetime, timedelta
from api.utils import get_coefficient, datetime_to_timestamp


class EtapasSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapaProposicao
        fields = (
            'id', 'id_ext', 'casa', 'sigla', 'data_apresentacao', 'ano', 'sigla_tipo',
            'regime_tramitacao', 'forma_apreciacao', 'ementa', 'justificativa', 'url',
            'temperatura', 'autor_nome', 'relator_nome', 'em_pauta', 'apelido', 'tema',
            'resumo_tramitacao')


class ProposicaoSerializer(serializers.ModelSerializer):
    etapas = EtapasSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = ('id', 'tema', 'apelido', 'etapas', 'resumo_progresso')


class TemperaturaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturaHistorico
        fields = ('periodo', 'temperatura_recente', 'temperatura_periodo')


class PautaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PautaHistorico
        fields = ('data', 'semana', 'local', 'em_pauta')


class ProgressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progresso
        fields = ('fase_global', 'local', 'data_inicio',
                  'data_fim', 'local_casa', 'pulou')


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''

    def get(self, request, format=None):
        return Response({'status': 'ok'})


class EtapasList(generics.ListAPIView):
    '''
    Dados gerais da proposição.
    '''
    queryset = EtapaProposicao.objects.prefetch_related(
        'tramitacao', 'temperatura_historico')
    serializer_class = EtapasSerializer


class ProposicaoList(generics.ListAPIView):
    '''
    Dados gerais da proposição.
    '''
    queryset = Proposicao.objects.prefetch_related(
        'etapas', 'etapas__tramitacao', 'progresso')
    serializer_class = ProposicaoSerializer


class TemperaturaHistoricoList(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'semanas_anteriores', openapi.IN_PATH,
                'número de semanas anteriores a retornar',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_referencia', openapi.IN_PATH,
                'data de referência a ser considerada',
                type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, casa, id_ext):
        '''
        Retorna o histórico de temperaturas de uma proposição, retornando a quantidade
        especificada de semanas anteriores à data de referência.
        '''
        semanas_anteriores = request.query_params.get('semanas_anteriores')
        data_referencia = request.query_params.get('data_referencia')

        queryset = TemperaturaHistorico.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        try:
            hoje = (
                datetime.today() if data_referencia is None else datetime.strptime(
                    data_referencia, '%Y-%m-%d'))
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            hoje = datetime.today()

        queryset = queryset.filter(periodo__lte=hoje)

        if semanas_anteriores is not None:
            start_date = hoje - timedelta(weeks=int(semanas_anteriores))
            queryset = queryset.filter(periodo__gte=start_date)
        temperaturas = []
        dates_x = [datetime_to_timestamp(temperatura.periodo)
                   for temperatura in queryset[:6]]  # pega as ultimas 6 temperaturas
        temperaturas_y = [temperatura.temperatura_recente for temperatura in queryset[:6]]

        for temperatura in queryset:
            temperaturas.append(TemperaturaHistoricoSerializer(temperatura).data)

        return Response({
            'coeficiente': get_coefficient(dates_x, temperaturas_y),
            'temperaturas': temperaturas
        })


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
                'data_referencia', openapi.IN_PATH,
                'data de referência a ser considerada',
                type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        '''
        Retorna o progresso de uma proposição, passando uma data de referência.
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        data_referencia = self.request.query_params.get('data_referencia', None)
        queryset = Progresso.objects.filter(
            etapa__casa=casa, etapa__id_ext=id_ext)

        try:
            hoje = datetime.today() if data_referencia is None else datetime.strptime(
                data_referencia, '%Y-%m-%d')
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            hoje = datetime.today()

        if(data_referencia is None):
            queryset = queryset.filter()
        else:
            queryset = queryset.filter(data_inicio__lte=hoje)

        return queryset


class PautaList(generics.ListAPIView):
    '''
    Dados do progresso da proposição por periodo de acordo com uma data de referência.
    '''

    serializer_class = PautaHistoricoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_referencia', openapi.IN_PATH,
                'data de referência a ser considerada',
                type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        '''
        Retorna o histórico da pauta
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        data_referencia = self.request.query_params.get('data_referencia', None)
        queryset = PautaHistorico.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        try:
            hoje = datetime.today() if data_referencia is None else datetime.strptime(
                data_referencia, '%Y-%m-%d')
            semana_atual = hoje.isocalendar()[1]
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            semana_atual = datetime.today().isocalendar()[1]

        if(data_referencia is None):
            queryset = queryset.filter()
        else:
            queryset = queryset.filter(semana=semana_atual)

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
        prop = get_object_or_404(EtapaProposicao, casa=casa, id_ext=id_ext)
        return Response(EtapasSerializer(prop).data)
