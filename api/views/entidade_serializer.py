from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.entidade import Entidade


class EntidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidade
        fields = (
            "legislatura",
            "id_entidade",
            "id_entidade_parlametria",
            "casa",
            "nome",
            "sexo",
            "partido",
            "uf",
            "situacao",
            "em_exercicio",
            "is_parlamentar",
        )


class EntidadeList(generics.ListAPIView):
    """
    Apresenta lista com todas as entidades
     do Congresso Nacional:
     podem ser parlamentares ou não,
     como Presidência da República e Mesas Diretoras.
    """

    serializer_class = EntidadeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "casa", openapi.IN_PATH, "Casa de interesse", type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "partido",
                openapi.IN_PATH,
                "Partido de interesse",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "uf", openapi.IN_PATH, "UF de interesse", type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "somente_em_exercicio",
                openapi.IN_PATH,
                "Somente em exercício",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "somente_parlamentares",
                openapi.IN_PATH,
                "Somente parlamentares",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get_queryset(self):
        casa_arg = self.request.query_params.get("casa", None)
        partido_arg = self.request.query_params.get("partido", None)
        uf_arg = self.request.query_params.get("uf", None)
        somente_em_exercicio = self.request.query_params.get(
            "somente_em_exercicio", True
        )
        somente_parlamentares = self.request.query_params.get(
            "somente_parlamentares", True
        )

        if somente_em_exercicio:
            queryset = Entidade.objects.filter(em_exercicio=1)
        else:
            queryset = Entidade.objects.all()

        if somente_parlamentares:
            queryset = queryset.filter(is_parlamentar=1)

        if casa_arg:
            queryset = queryset.filter(casa=casa_arg)

        if partido_arg:
            queryset = queryset.filter(partido=partido_arg)

        if uf_arg:
            queryset = queryset.filter(uf=uf_arg)

        return queryset


class EntidadeParlamentarSerializer(serializers.Serializer):
    id_autor_parlametria = serializers.IntegerField(source='id_entidade_parlametria')
    casa_autor = serializers.CharField(source='casa')
    nome_autor = serializers.CharField(source='nome')
    partido = serializers.CharField()
    uf = serializers.CharField()
    governismo = serializers.FloatField()


class ParlamentaresExercicioList(generics.ListAPIView):
    """
    Retorna lista com todos os parlamentares em exercício para a legislatura 56
    """

    serializer_class = EntidadeParlamentarSerializer

    def get_queryset(self):

        casa_arg = self.request.query_params.get("casa")

        query = (
            "SELECT e.id, id_entidade_parlametria, e.casa, nome, "
            "partido, uf, governismo " +
            "FROM api_entidade e " +
            "LEFT JOIN api_governismo " +
            "ON id_entidade_parlametria = id_parlamentar_parlametria " +
            "WHERE em_exercicio = 1 AND is_parlamentar = 1 " +
            "AND legislatura = 56")

        if casa_arg is not None:
            query = (
                query
                + " AND e.casa = '" + casa_arg + "'"
            )

        queryset = (Entidade.objects
                    .raw(query))

        return queryset


class RelatorSerializer(serializers.ModelSerializer):
    id_relator_parlametria = serializers.IntegerField(source="id_entidade_parlametria")

    class Meta:
        model = Entidade
        fields = (
            "id_relator_parlametria",
            "casa",
            "nome",
            "partido",
            "uf"
        )


class AtorEntidadeSerializer(serializers.ModelSerializer):
    id_autor = serializers.IntegerField(source="id_entidade")
    id_autor_parlametria = serializers.IntegerField(source="id_entidade_parlametria")
    nome_autor = serializers.CharField(source="nome")
    casa_autor = serializers.CharField(source="casa")

    class Meta:
        model = Entidade
        fields = (
            "id_autor",
            "id_autor_parlametria",
            "nome_autor",
            "partido",
            "uf",
            "casa_autor"
        )


class AtorEntidadeInfo(generics.ListAPIView):
    """
    Retorna informações específicas de um parlamentar como nome, uf e partido
    """

    serializer_class = AtorEntidadeSerializer

    def get_queryset(self):

        id_autor_arg = self.kwargs["id_autor"]

        queryset = (
            Entidade.objects.filter(id_entidade_parlametria=id_autor_arg)
            .order_by("-legislatura")
        )[:1]

        return queryset
