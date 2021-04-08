from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.model.votacoes_sumarizadas import VotacoesSumarizadas


class VotacoesSumarizadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotacoesSumarizadas
        fields = (
            "id_parlamentar",
            "id_parlamentar_parlametria",
            "casa",
            "ultima_data_votacao",
            "num_votacoes_parlamentar_governismo",
            "num_votacoes_totais_governismo",
            "num_votacoes_parlamentar_disciplina",
            "num_votacoes_totais_disciplina"
        )


class VotacoesSumarizadasList(generics.ListAPIView):
    """
    Dados de votacoes sumarizadas.
    """

    serializer_class = VotacoesSumarizadasSerializer

    def get_queryset(self):
        """
        Retorna as votações sumarizadas.
        """

        return VotacoesSumarizadas.objects


class VotacoesSumarizadasParlamentar(generics.ListAPIView):
    """
    Dados de votações sumarizadas de um parlamentar.
    """

    serializer_class = VotacoesSumarizadasSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "id da proposição no sistema do Leg.go",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna votações sumarizadas de um parlamentar.
        """
        id_parlamentar = self.kwargs["id"]
        return VotacoesSumarizadas.objects.filter(
            id_parlamentar_parlametria=id_parlamentar)
