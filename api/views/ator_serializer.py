from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Prefetch, Sum, Count

from api.model.ator import Atores
from api.model.etapa_proposicao import EtapaProposicao
from api.utils.filters import get_filtered_autores, get_filtered_interesses


class AtorSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    nome_autor = serializers.CharField(source='entidade__nome')
    partido = serializers.CharField(source='entidade__partido')
    uf = serializers.CharField(source='entidade__uf')
    casa_autor = serializers.CharField()
    bancada = serializers.CharField()


class AtorList(generics.ListAPIView):

    '''
    Informações sobre um parlamentar específico.
    '''
    serializer_class = AtorSerializer

    def get_queryset(self):
        '''
        Retorna dados básicos e de atividade de um parlamentar por interesse.
        '''
        tema_arg = self.request.query_params.get('tema')
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg, tema_arg)
        id_autor_arg = self.kwargs['id_autor']

        ator = (
            Atores.objects
            .filter(id_leggo__in=interesses.values('id_leggo'),
                    id_autor_parlametria=id_autor_arg)
            .select_related('entidade')
            .values('id_autor', 'id_autor_parlametria', 'entidade__nome',
                    'entidade__uf', 'entidade__partido', 'casa_autor', 'bancada')
            .order_by('-casa_autor')
            .distinct()
            .prefetch_related(Prefetch("interesse", queryset=interesses))
        )

        return ator


class AtoresSerializerComissoes(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    nome_autor = serializers.CharField(source='entidade__nome')
    partido = serializers.CharField(source='entidade__partido')
    uf = serializers.CharField(source='entidade__uf')
    casa_autor = serializers.CharField()
    bancada = serializers.CharField()


class AtoresProposicaoList(generics.ListAPIView):
    """
    Dados de atores de uma proposição. Lista parlamentares que atuaram numa proposição
    com informações como o número de documentos criados e o peso do autor com relação
    aos documentos apresentados. A participação do parlamentar em um documento é
    inversamente proporcional à quantidade de parlamentares que assinaram o documento
    juntos: um documento feito por dois parlamentares terá valor de
    participação igual a 1/2 = 0.5. Desta forma o peso do ator é a soma das
    participações do parlamentar nos documentos relacionados à proposição.
    """

    serializer_class = AtoresSerializerComissoes

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id_leggo",
                openapi.IN_PATH,
                "id da proposição no sistema Leggo",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna os atores por proposição
        """
        prop_leggo_id = self.kwargs["id_leggo"]
        queryset = (
            Atores.objects.filter(id_leggo=prop_leggo_id)
            .select_related('entidade')
            .values('id_autor', 'id_autor_parlametria', 'entidade__nome',
                    'entidade__uf', 'entidade__partido', 'casa_autor', 'bancada')
        )
        return get_filtered_autores(self.request, queryset)


class AtoresAgregadosSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    nome_autor = serializers.CharField(source='entidade__nome')
    partido = serializers.CharField(source='entidade__partido')
    uf = serializers.CharField(source='entidade__uf')
    casa_autor = serializers.CharField()
    bancada = serializers.CharField()
    total_documentos = serializers.IntegerField()
    peso_documentos = serializers.IntegerField()


class AtoresAgregadosList(generics.ListAPIView):
    """
    Informação agregada sobre parlamentares.
    """

    serializer_class = AtoresAgregadosSerializer

    def get_queryset(self):
        """
        Retorna dados básicos e de atividade parlamentar por interesse.
        """
        tema_arg = self.request.query_params.get('tema')
        interesse_arg = self.request.query_params.get("interesse")
        if interesse_arg is None:
            interesse_arg = "leggo"
        interesses = get_filtered_interesses(interesse_arg, tema_arg)

        atores = (
            Atores.objects.filter(id_leggo__in=interesses.values('id_leggo'))
            .select_related('entidade')
            .values("id_autor", "id_autor_parlametria", "entidade__nome", "entidade__uf",
                    "entidade__partido", "casa_autor", "bancada")
            .annotate(
                total_documentos=Sum("num_documentos"),
                peso_documentos=Sum("peso_total_documentos"),
            )
            .prefetch_related(Prefetch("interesse", queryset=interesses))
        )
        return atores


class AtoresRelatoriasDetalhadaSerializer(serializers.Serializer):
    ids_relatorias = serializers.ListField()
    quantidade_relatorias = serializers.IntegerField()


class AtoresRelatoriasDetalhada(generics.ListAPIView):

    serializer_class = AtoresRelatoriasDetalhadaSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id_autor', openapi.IN_PATH, 'id do autor no sistema Leggo',
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'interesse', openapi.IN_PATH, 'interesse da proposição no sistema Leggo',
                type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        '''
        Retorna id's e quantidade de relatorias de um determinado parlamentar
        '''
        leggo_id_autor = self.kwargs['id_autor']
        interesseArg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        if interesseArg is None:
            interesseArg = 'leggo'
        interesses = get_filtered_interesses(interesseArg, tema_arg)

        atoresRE = (
            Atores.objects.filter(id_autor_parlametria=leggo_id_autor)
            .select_related('entidade')
            .values('entidade__nome')
            .distinct()
        )

        relatorias = list(
            EtapaProposicao.objects.filter(id_leggo__in=interesses)
            .filter(relator_nome__icontains=atoresRE)
            .values('id_leggo')
            .prefetch_related(
                Prefetch("interesse", queryset=interesses)
            )
        )

        queryset = [
            {
                'ids_relatorias': relatorias,
                'quantidade_relatorias': len(relatorias)
            }
        ]

        return queryset


class AtoresRelatoresSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_autor_parlametria = serializers.IntegerField()
    quantidade_relatorias = serializers.IntegerField()


class AtoresRelatoriasList(generics.ListAPIView):

    serializer_class = AtoresRelatoresSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "interesse",
                openapi.IN_PATH,
                "interesse da proposição no sistema Leggo",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna parlamentares e a quantidade de relatorias
        """
        interesseArg = self.request.query_params.get("interesse")
        tema_arg = self.request.query_params.get('tema')
        if interesseArg is None:
            interesseArg = "leggo"
        interesses = get_filtered_interesses(interesseArg, tema_arg)

        queryset = (
            EtapaProposicao.objects.filter(id_leggo__in=interesses.values('id_leggo'))
            .exclude(relator_nome="Relator não encontrado")
            .values("id")
            .distinct()
            .prefetch_related(Prefetch("interesse", queryset=interesses))
        )

        atoresRE = (
            Atores.objects.filter(id_leggo__in=queryset)
            .values("id_autor", "id_autor_parlametria")
            .annotate(quantidade_relatorias=Count("id_autor"))
        )

        return atoresRE
