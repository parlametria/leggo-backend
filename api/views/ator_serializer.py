from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.utils.filters import get_filtered_autores
from api.model.ator import Atores


class AtoresSerializerComissoes(serializers.ModelSerializer):
    class Meta:
        model = Atores
        fields = (
            'id_autor', 'nome_autor', 'partido', 'uf',
            'peso_total_documentos', 'tipo_generico',
            'sigla_local', 'is_important', 'nome_partido_uf')


class AtoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atores
        fields = (
            'id_autor', 'peso_total_documentos', 'tipo_generico',
            'nome_partido_uf')


class AtoresList(generics.ListAPIView):
    '''
    Dados de atores de uma proposição
    '''

    serializer_class = AtoresSerializer

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
        Retorna o autor
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        queryset = Atores.objects.filter(
            proposicao__casa=casa, proposicao__id_ext=id_ext)

        return get_filtered_autores(self.request, queryset)
