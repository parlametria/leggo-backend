from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.utils.filters import get_time_filtered_pauta
from api.model.pauta_historico import PautaHistorico

class PautaHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PautaHistorico
        fields = ('data', 'semana', 'local', 'em_pauta')

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
        id = self.kwargs['id']
        return get_time_filtered_pauta.filter(proposicao__id=id)
