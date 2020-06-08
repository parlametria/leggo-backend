from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count, Prefetch

from api.model.autoria import Autoria
from api.utils.filters import get_filtered_interesses


class AutoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autoria
        fields = (
            'id_leggo', 'id_documento', 'id_autor',
            'descricao_tipo_documento', 'data',
            'url_inteiro_teor', 'autores')


class AutoriaList(generics.ListAPIView):
    '''
    Dados de autoria de uma proposição. Apresenta lista de documentos contendo informações
    como a data de apresentação, tipo e autores.
    '''

    serializer_class = AutoriaSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna a autoria
        '''
        id_prop = self.kwargs['id']
        return Autoria.objects.filter(id_leggo=id_prop)


class AutoriasAgregadasSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    quantidade_autorias = serializers.IntegerField()


class AutoriasAgregadasList(generics.ListAPIView):
    '''
    Informação agregada sobre autorias.
    '''
    serializer_class = AutoriasAgregadasSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias por parlamentar.
        Se não for passado um interesse como argumento, todos os dados são retornados.
        '''
        interesse_arg = self.request.query_params.get("interesse")
        interesses = get_filtered_interesses(interesse_arg)

        autorias = (
            Autoria.objects
            .filter(id_leggo__in=interesses)
            .values('id_autor')
            .annotate(quantidade_autorias=Count('id_autor'))
            .prefetch_related(
                Prefetch("interesse", queryset=interesses)
            )
        )
        return autorias
