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


class AutoriaAutorSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    id_documento = serializers.IntegerField()
    id_leggo = serializers.IntegerField()
    data = serializers.DateField()
    descricao_tipo_documento = serializers.CharField()
    url_inteiro_teor = serializers.CharField()
    tipo_documento = serializers.CharField()


class AutoriasAutorList(generics.ListAPIView):
    '''
    Informações sobre autorias de um autor específico.
    '''
    serializer_class = AutoriaAutorSerializer

    def get_queryset(self):
        '''
        Retorna as autorias de um parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg)
        id_autor_arg = self.kwargs['id_autor']
        autorias = (
            Autoria.objects
            .filter(id_leggo__in=interesses,
                    id_autor_parlametria=id_autor_arg)
        )
        return autorias


class AutoriasAgregadasSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    quantidade_autorias = serializers.IntegerField()


class AutoriasAgregadasList(generics.ListAPIView):
    '''
    Informação agregada sobre autorias de projetos de lei
    '''
    serializer_class = AutoriasAgregadasSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias por parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg)

        autorias = (
            Autoria.objects
            .filter(id_leggo__in=interesses, tipo_documento="Prop. Original / Apensada")
            .values('id_autor', 'id_autor_parlametria')
            .annotate(quantidade_autorias=Count('id_autor'))
            .prefetch_related(
                Prefetch("interesse", queryset=interesses)
            )
        )
        return autorias


class AutoriasAgregadasByAutor(generics.ListAPIView):
    '''
    Informação agregada sobre autorias de projetos de lei
    para um autor específico passado como parâmetro
    '''
    serializer_class = AutoriasAgregadasSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias para um parlamentar específico.
        Considera as autorias do parlamentar para um interesse específico.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg)

        id_autor_parlametria = self.kwargs["id_autor"]

        autorias = (
            Autoria.objects
            .filter(id_autor_parlametria=id_autor_parlametria,
                    id_leggo__in=interesses, tipo_documento="Prop. Original / Apensada")
            .values('id_autor', 'id_autor_parlametria')
            .annotate(quantidade_autorias=Count('id_autor'))
            .prefetch_related(
                Prefetch("interesse", queryset=interesses)
            )
        )
        return autorias
