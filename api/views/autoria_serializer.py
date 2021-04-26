from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import (
    Count,
    Sum,
    Value,
    F,
    CharField)
from django.db.models.functions import (
    Concat,
    ExtractYear)
from api.model.autoria import Autoria
from api.utils.filters import get_filtered_interesses, get_filtered_destaques
from api.utils.queries_autorias_agregadas import (
    queryAutoriasAgregadas,
    queryAutoriasAgregadasByTipoAcao,
    queryAutoriasAgregadasByTipoAcaoEIdAutor)


class AutoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autoria
        fields = (
            "id_leggo",
            "id_documento",
            "id_autor",
            "descricao_tipo_documento",
            "data",
            "url_inteiro_teor",
            "autores",
        )


class AutoriaList(generics.ListAPIView):
    """
    Dados de autoria de uma proposição. Apresenta lista de documentos contendo informações
    como a data de apresentação, tipo e autores.
    """

    serializer_class = AutoriaSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id_leggo",
                openapi.IN_PATH,
                "id da proposição no sistema do Leg.go",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna a autoria
        """
        id_prop = self.kwargs["id_leggo"]
        return Autoria.objects.filter(id_leggo=id_prop)


class AutoriasPorProposicaoSerializer(serializers.Serializer):
    id_autor_parlametria = serializers.IntegerField()
    casa_autor = serializers.CharField()
    nome_autor = serializers.CharField(source="entidade__nome")
    partido = serializers.CharField(source="entidade__partido")
    uf = serializers.CharField(source="entidade__uf")
    tipo_documento = serializers.CharField()
    peso_documentos = serializers.FloatField()
    total_documentos = serializers.IntegerField()


class AutoriasPorProposicaoList(generics.ListAPIView):
    """
    Contagem de documentos em uma proposição por parlamentar
    e tipo de ação.
    """

    serializer_class = AutoriasPorProposicaoSerializer

    def get_queryset(self):
        '''
        Retorna as autorias em uma proposição.
        Para cada parlamentar que apresentou documentos
        relacionados a uma proposição, retorna a quantidade
        de documentos por tipo de documento.
        '''

        id_leggo_arg = self.kwargs['id_leggo']

        autorias = (
            Autoria.objects
            .filter(id_leggo=id_leggo_arg,
                    data__gte='2019-01-31',
                    tipo_acao__in=['Proposição'])
            .select_related("entidade")
            .values(
                "id_autor_parlametria",
                "casa_autor",
                "entidade__nome",
                "entidade__uf",
                "entidade__partido",
                "tipo_documento"
            )
            .annotate(total_documentos=Count('tipo_documento'))
            .annotate(peso_documentos=Sum('peso_autor_documento'))
        )

        return autorias


class AutoriaAutorSerializer(serializers.Serializer):
    id_autor_parlametria = serializers.IntegerField()
    id_documento = serializers.IntegerField()
    id_leggo = serializers.CharField()
    data = serializers.DateField()
    descricao_tipo_documento = serializers.CharField()
    url_inteiro_teor = serializers.CharField()
    tipo_documento = serializers.CharField()
    tipo_acao = serializers.CharField()
    peso_autor_documento = serializers.FloatField()
    sigla = serializers.CharField(source='etapa_proposicao__sigla')


class AutoriasAutorList(generics.ListAPIView):
    """
    Informações sobre autorias de um autor específico.
    """

    serializer_class = AutoriaAutorSerializer

    def get_queryset(self):
        '''
        Retorna as autorias de um parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg, tema_arg)
        id_autor_arg = self.kwargs['id_autor']

        autorias = Autoria.objects

        if destaques_arg == 'true':
            destaques = get_filtered_destaques(destaques_arg)
            autorias = (
                autorias.filter(id_leggo__in=destaques)
            )

        autorias = (
            autorias
            .filter(id_leggo__in=interesses.values('id_leggo'),
                    id_autor_parlametria=id_autor_arg,
                    data__gte='2019-01-31')
            .distinct('id_autor_parlametria', 'id_documento')
            .values('id_autor_parlametria', 'id_documento', 'id_leggo',
                    'data', 'descricao_tipo_documento', 'url_inteiro_teor',
                    'tipo_documento', 'tipo_acao', 'peso_autor_documento',
                    'etapa_proposicao__sigla')
        )

        return autorias


class AutoriasAgregadasSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    quantidade_autorias = serializers.IntegerField()
    peso_documentos = serializers.FloatField()


class AutoriasAgregadasList(generics.ListAPIView):
    """
    Informação agregada sobre autorias de projetos de lei
    """

    serializer_class = AutoriasAgregadasSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias por parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        Se o query param destaque for igual a true então apenas os projetos
        com destaque serão considerados
        '''
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryAutoriasAgregadasByTipoAcao(
            '2019-02-01',
            interesse_arg,
            tema_arg,
            destaques_arg,
            'Proposição'
        )

        autorias = Autoria.objects.raw(q)

        return autorias


class AutoriasAgregadasByAutorSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    quantidade_autorias = serializers.IntegerField()
    peso_documentos = serializers.FloatField()
    max_quantidade_autorias = serializers.IntegerField()
    min_quantidade_autorias = serializers.IntegerField()


class AutoriasAgregadasByAutor(generics.ListAPIView):
    """
    Informação agregada sobre autorias de projetos de lei
    para um autor específico passado como parâmetro
    """

    serializer_class = AutoriasAgregadasByAutorSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias para um parlamentar específico.
        Considera as autorias do parlamentar para um interesse específico.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        id_autor_parlametria = self.kwargs["id_autor"]

        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryAutoriasAgregadasByTipoAcaoEIdAutor(
            '2019-02-01',
            interesse_arg,
            tema_arg,
            destaques_arg,
            id_autor_parlametria,
            'Proposição')

        autorias = Autoria.objects.raw(q)

        return autorias


class AutoriasAgregadasProjetosSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    quant_autorias_projetos = serializers.IntegerField(source='quantidade_autorias')
    peso_autorias_projetos = serializers.FloatField(source='peso_documentos')


class AutoriasAgregadasProjetos(generics.ListAPIView):
    """
    Informação agregada sobre autorias de projetos de lei para crachas.
    """

    serializer_class = AutoriasAgregadasProjetosSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias por parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''

        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryAutoriasAgregadasByTipoAcao(
            '2019-02-01',
            interesse_arg,
            tema_arg,
            destaques_arg,
            'Proposição',
            'Prop. Original / Apensada'
        )

        autorias = Autoria.objects.raw(q)

        return autorias


class AutoriasAgregadasProjetosById(generics.ListAPIView):
    """
    Informação agregada sobre autorias de projetos de lei para crachas,
    para um autor específico passado como parâmetro.
    """

    serializer_class = AutoriasAgregadasProjetosSerializer

    def get_queryset(self):
        '''
        Retorna quantidade de autorias para um parlamentar específico.
        Considera as autorias do parlamentar para um interesse específico.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        id_autor_parlametria = self.kwargs["id_autor"]

        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryAutoriasAgregadasByTipoAcaoEIdAutor(
            '2019-02-01',
            interesse_arg,
            tema_arg,
            destaques_arg,
            id_autor_parlametria,
            'Proposição',
            'Prop. Original / Apensada'
        )
        autorias = Autoria.objects.raw(q)

        return autorias


class AcoesSerializer(serializers.Serializer):
    id_autor_parlametria = serializers.IntegerField()
    num_documentos = serializers.IntegerField()
    ranking_documentos = serializers.IntegerField()
    peso_total = serializers.FloatField()
    tipo_acao = serializers.CharField()


class Acoes(generics.ListAPIView):
    """
    Dados de ações de um parlamentar. Apresenta números de emendas e requerimentos,
    assim como sua posição no ranking.
    """

    serializer_class = AcoesSerializer

    def get_queryset(self):
        '''
        Retorna as ações do parlamentar
        '''
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryAutoriasAgregadas('2019-02-01', interesse_arg, tema_arg, destaques_arg)
        result = Autoria.objects.raw(q)

        return result


class AutoriasOriginaisSerializer(serializers.Serializer):
    id_autor_parlametria = serializers.IntegerField()
    id_documento = serializers.IntegerField()
    peso_autor_documento = serializers.FloatField()
    id_leggo = serializers.CharField()
    data = serializers.DateField()
    descricao_tipo_documento = serializers.CharField()
    url_inteiro_teor = serializers.CharField()
    tipo_documento = serializers.CharField()
    tipo_acao = serializers.CharField()
    sigla = serializers.CharField()


class AutoriasOriginaisList(generics.ListAPIView):
    '''
    Informações sobre proposições originais ou apensadas de um autor específico.
    '''
    serializer_class = AutoriasOriginaisSerializer

    def get_queryset(self):
        '''
        Retorna as proposições originais ou apensadas de um parlamentar.
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        destaques_arg = self.request.query_params.get('destaque')

        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg, tema_arg)

        id_autor_arg = self.kwargs['id_autor']

        autorias = Autoria.objects

        if destaques_arg == 'true':
            destaques = get_filtered_destaques(destaques_arg)
            autorias = (
                autorias.filter(id_leggo__in=destaques)
            )

        autorias = (
            autorias
            .filter(id_leggo__in=interesses.values('id_leggo'),
                    id_autor_parlametria=id_autor_arg,
                    data__gte='2019-01-31',
                    tipo_documento='Prop. Original / Apensada')
            .distinct('id_autor_parlametria', 'id_documento')
            .values('id_autor_parlametria', 'id_documento', 'peso_autor_documento',
                    'id_leggo', 'data',
                    'descricao_tipo_documento', 'url_inteiro_teor',
                    'tipo_documento', 'tipo_acao', 'sigla')
        )

        return autorias


class AutoriasTabelaSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    casa_autor = serializers.CharField()
    id_documento = serializers.IntegerField()
    id_leggo = serializers.CharField()
    id_principal = serializers.CharField()
    casa = serializers.CharField()
    data = serializers.DateField()
    descricao_tipo_documento = serializers.CharField()
    tipo_documento = serializers.CharField()
    tipo_acao = serializers.CharField()
    peso_autor_documento = serializers.FloatField()


class AutoriasTabelaList(generics.ListAPIView):
    """
    Informações sobre autorias de documentos relacionadas a projetos
    """

    serializer_class = AutoriasTabelaSerializer

    def get_queryset(self):
        '''
        Retorna as autorias dos parlamentares
        Se não for passado um interesse como argumento,
        os dados retornados serão os do interesse default (leggo).
        '''
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')

        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg, tema_arg)

        autorias = (
            Autoria.objects
            .filter(id_leggo__in=interesses.values('id_leggo'),
                    data__gt='2019-01-31')
            .distinct('id_autor, id_documento')
            .select_related('etapa_proposicao')
            .values('id_autor', 'casa_autor', 'id_documento', 'id_leggo',
                    'id_principal', 'casa',
                    'data', 'descricao_tipo_documento',
                    'tipo_documento', 'tipo_acao', 'peso_autor_documento',
                    'etapa_proposicao__sigla_tipo',
                    'etapa_proposicao__numero',
                    'etapa_proposicao__data_apresentacao')
        )

        return autorias
