from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema, generics
from drf_yasg import openapi
from api.model.pressao import Pressao

class PressaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pressao
        fields = (
            'date', 'max_pressao_principal',
            'max_pressao_rel',	'maximo_geral')

class PressaoList(generics.ListAPIView):
    '''
    Dados de pressão de proposições
    '''

    serializer_class = PressaoSerializer

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
        Retorna a pressão
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        queryset = Pressao.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        return queryset

