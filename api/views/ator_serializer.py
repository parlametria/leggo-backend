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
            'peso_total_documentos', 'num_documentos', 'tipo_generico',
            'sigla_local_formatada', 'is_important', 'nome_partido_uf')


class AtoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atores
        fields = (
            'id_autor', 'peso_total_documentos', 'num_documentos',
            'tipo_generico', 'nome_partido_uf')


class AtoresList(generics.ListAPIView):
    '''
    Dados de atores de uma proposição
    '''

    serializer_class = AtoresSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id_leggo', openapi.IN_PATH, 'id da proposição no sistema Leggo',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna os atores
        '''
        prop_leggo_id = self.kwargs['id_leggo']
        queryset = Atores.objects.filter(id_leggo=prop_leggo_id)
        return get_filtered_autores(self.request, queryset)
