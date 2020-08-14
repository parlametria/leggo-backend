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


class EntidadeParlamentarSerializer(serializers.ModelSerializer):
    id_autor_parlametria = serializers.IntegerField(source='id_entidade_parlametria')
    casa_autor = serializers.CharField(source='casa')
    nome_autor = serializers.CharField(source='nome')

    class Meta:
        model = Entidade
        fields = (
            "id_autor_parlametria",
            "casa_autor",
            "nome_autor",
            "partido",
            "uf"
        )


class ParlamentaresExercicioList(generics.ListAPIView):
    """
    Retorna lista com todos os parlamentares em exercício para a legislatura 56
    """

    serializer_class = EntidadeParlamentarSerializer

    def get_queryset(self):

        casa_arg = self.request.query_params.get("casa")

        queryset = Entidade.objects.filter(legislatura=56,
                                           is_parlamentar=1,
                                           em_exercicio=1)

        if casa_arg:
            queryset = queryset.filter(casa=casa_arg)

        return queryset
