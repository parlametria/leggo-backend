from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.models import (
    TramitacaoEvent)
from datetime import datetime


class TramitacaoEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TramitacaoEvent
        fields = ('data', 'casa', 'sigla_local', 'evento', 'texto_tramitacao', 'status',
                  'proposicao', 'nivel')


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
                'apenas_importantes', openapi.IN_PATH,
                'se deve retornar apenas os eventos importantes',
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

        queryset = TramitacaoEvent.objects.prefetch_related('proposicao')

        id_ext = self.kwargs.get('id_ext')
        if id_ext:
            queryset = queryset.filter(proposicao__id_ext=id_ext)

        casa = self.kwargs.get('casa')
        if casa:
            queryset = queryset.filter(proposicao__casa=casa)

        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        apenas_importantes = self.request.query_params.get('apenas_importantes', False)
        ultimos_n = self.request.query_params.get('ultimos_n', 100)

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

        queryset = queryset.order_by('-data').filter(data__lte=data_fim_dt)

        if apenas_importantes:
            queryset = queryset.exclude(evento__exact="nan")

        if ultimos_n is not None:
            queryset = queryset[:int(ultimos_n)]

        return queryset
