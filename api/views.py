from django.shortcuts import get_object_or_404
from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.models import (
    EtapaProposicao, TemperaturaHistorico, InfoGerais,
    Progresso, Proposicao, PautaHistorico, Emendas, TramitacaoEvent)
from datetime import datetime, timedelta
from api.utils import get_coefficient_temperature


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


class TramitacaoEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TramitacaoEvent
        fields = ('data', 'casa', 'sigla_local', 'evento', 'texto_tramitacao')


class PautaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PautaHistorico
        fields = ('data', 'semana', 'local', 'em_pauta')


class ProgressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progresso
        fields = ('fase_global', 'local', 'data_inicio',
                  'data_fim', 'local_casa', 'pulou')


class EmendasSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Emendas
        fields = ('data_apresentacao', 'local', 'autor')


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''

    def get(self, request, format=None):
        return Response({i.name: i.value for i in InfoGerais.objects.all()})


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
    '''
    Historico de temperaturas de uma proposicao
    '''
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
            date = (
                datetime.today() if data_referencia is None else datetime.strptime(
                    data_referencia, '%Y-%m-%d'))
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            date = datetime.today()

        queryset = queryset.filter(periodo__lte=date)

        if semanas_anteriores is not None:
            start_date = date - timedelta(weeks=int(semanas_anteriores))
            queryset = queryset.filter(periodo__gte=start_date)

        temperaturas = [TemperaturaHistoricoSerializer(temperatura).data
                        for temperatura in queryset]

        return Response({
            'coeficiente': get_coefficient_temperature(queryset),
            'temperaturas': temperaturas
        })


class TramitacaoEventList(generics.ListAPIView):

    serializer_class = TramitacaoEventSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_inicio', openapi.IN_PATH,
                'data de início do período de tempo ao qual os eventos devem pertencer',
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'data_fim', openapi.IN_PATH,
                'data de fim do período de tempo ao qual os eventos devem pertencer',
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'ultimos_n', openapi.IN_PATH,
                'últimos n eventos a serem retornados',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna os últimos n eventos da tramitação de uma proposição, dentro de um período
        delimitado por uma data de início e de fim.
        '''

        id_ext = self.kwargs['id_ext']
        casa = self.kwargs['casa']
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        ultimos_n = self.request.query_params.get('ultimos_n', None)

        queryset = TramitacaoEvent.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        data_inicio_dt = None
        data_fim_dt = None

        try:
            if data_inicio is not None:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
        except ValueError:
            print(f'Data de início ({data_inicio}) inválida. ')
            data_inicio_dt = None

        try:
            data_fim_dt = (
                datetime.today() if data_fim is None else datetime.strptime(
                    data_fim, '%Y-%m-%d'))
        except ValueError:
            print(
                f'Data de fim ({data_fim}) inválida. '
                'Utilizando data atual como data de fim.')
            data_fim_dt = datetime.today()

        if data_inicio_dt is not None:
            queryset = queryset.filter(data__gte=data_inicio_dt)

        queryset = queryset.filter(data__lte=data_fim_dt)

        if ultimos_n is not None:
            queryset = queryset.order_by('-data')[:int(ultimos_n)]

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

        if data_referencia is None:
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

        if data_referencia is None:
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


class EmendasList(generics.ListAPIView):
    '''
    Dados da emenda de uma proposição
    '''

    serializer_class = EmendasSerialzer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna a emenda
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        queryset = Emendas.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        return queryset
