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


class AtoresList(generics.ListAPIView):
    '''
    Dados de atores de uma proposição. Lista parlamentares que atuaram numa proposição
    com informações como o número de documentos criados e o peso do autor com relação
    aos documentos apresentados. A participação do parlamentar em um documento é
    inversamente proporcional à quantidade de parlamentares que assinaram o documento
    juntos: um documento feito por dois parlamentares terá valor de
    participação igual a 1/2 = 0.5. Desta forma o peso do ator é a soma das
    participações do parlamentar nos documentos relacionados à proposição.
    '''

    serializer_class = AtoresSerializerComissoes

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
