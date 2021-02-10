from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.tramitacao_event import TramitacaoEvent
from datetime import datetime


class TramitacaoEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TramitacaoEvent
        fields = ('data', 'casa', 'sigla_local', 'evento', 'titulo_evento',
                  'texto_tramitacao', 'status', 'proposicao_id', 'nivel', 'tema')


class TramitacaoEventList(generics.ListAPIView):
    '''
    Retorna os eventos de tramitação de uma proposição. A lista de eventos apresenta
    informações como o local e o nível de importância do evento.
    '''

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
                'nivel', openapi.IN_PATH,
                'se deve retornar apenas os eventos tão ou mais importantes',
                type=openapi.TYPE_BOOLEAN),
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

        queryset = TramitacaoEvent.objects.prefetch_related(
            'etapa_proposicao', 'etapa_proposicao__proposicao')

        id_ext = self.kwargs.get('id_ext')
        if id_ext:
            queryset = queryset.filter(etapa_proposicao__id_ext=id_ext)

        casa = self.kwargs.get('casa')
        if casa:
            queryset = queryset.filter(etapa_proposicao__casa=casa)

        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        nivel = self.request.query_params.get('nivel', 100)
        ultimos_n = self.request.query_params.get('ultimos_n', 100)
        interesseArg = self.request.query_params.get('interesse', None)

        data_inicio_dt = None
        data_fim_dt = None

        if interesseArg is not None:
            queryset = queryset.filter(
                etapa_proposicao__proposicao__interesse__interesse=interesseArg)

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

        if nivel:
            queryset = queryset.order_by('nivel', '-data').filter(nivel__lte=nivel)

        if ultimos_n is not None:
            queryset = queryset[:int(ultimos_n)]

        queryset = sorted(queryset, key=lambda x: x.data, reverse=True)

        return queryset


class TramitacaoEventListByID(generics.ListAPIView):
    '''
    Retorna os eventos de tramitação de uma determinada proposição com base no Id
    da proposicaoe datas de inicio e fim. A lista de eventos apresenta
    informações como o local e o nível de importância do evento.
    '''

    serializer_class = TramitacaoEventSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                "id_leggo", openapi.IN_PATH, "ID Leggo", type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'data_inicio', openapi.IN_PATH,
                'data de início do período de tempo ao qual os eventos devem pertencer',
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'data_fim', openapi.IN_PATH,
                'data de fim do período de tempo ao qual os eventos devem pertencer',
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'nivel', openapi.IN_PATH,
                'se deve retornar apenas os eventos tão ou mais importantes',
                type=openapi.TYPE_BOOLEAN),
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
        
        queryset = nanFreeObjects.prefetch_related(
            'etapa_proposicao', 'etapa_proposicao__proposicao')

        id_leggo = self.kwargs["id_leggo"]
        if id_leggo:
            queryset = queryset.filter(etapa_proposicao__proposicao__id_leggo=id_leggo)

        id_ext = self.kwargs.get('id_ext')
        if id_ext:
            queryset = queryset.filter(etapa_proposicao__id_ext=id_ext)

        casa = self.kwargs.get('casa')
        if casa:
            queryset = queryset.filter(etapa_proposicao__casa=casa)

        data_inicio = self.request.query_params.get('data_inicial', None)
        data_fim = self.request.query_params.get('data_final', None)
        nivel = self.request.query_params.get('nivel', 100)
        ultimos_n = self.request.query_params.get('ultimos_n', 100)
        interesseArg = self.request.query_params.get('interesse', None)

        data_inicio_dt = None
        data_fim_dt = None

        if interesseArg is not None:
            queryset = queryset.filter(
                etapa_proposicao__proposicao__interesse__interesse=interesseArg)

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

        if nivel:
            queryset = queryset.order_by('nivel', '-data').filter(nivel__lte=nivel)

        if ultimos_n is not None:
            queryset = queryset[:int(ultimos_n)]

        queryset = sorted(queryset, key=lambda x: x.data, reverse=True)

        return queryset
