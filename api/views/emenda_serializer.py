from rest_framework import serializers, generics
from api.model.emenda import Emendas
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class EmendasSerialzer(serializers.ModelSerializer):
    titulo = serializers.ReadOnlyField()

    class Meta:
        model = Emendas
        fields = ('data_apresentacao', 'codigo_emenda', 'local',
                  'autor', 'inteiro_teor', 'distancia', 'titulo')

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
