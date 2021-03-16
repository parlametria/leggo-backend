from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.model.disciplina import Disciplina


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = (
            "id_parlamentar_parlametria",
            "casa",
            "disciplina"
        )


class DisciplinaList(generics.ListAPIView):
    """
    Dados de disciplina dos parlamentares. A disciplina é calculada usando a
    técnica de Ideal points com base nas votações nominais de plenário na
    legislatura
    """

    serializer_class = DisciplinaSerializer

    def get_queryset(self):
        """
        Retorna o disciplina
        """

        return Disciplina.objects


class DisciplinaParlamentar(generics.ListAPIView):
    """
    Dados de disciplina de um parlamentar. A disciplina é calculada usando a
    técnica de Ideal points com base nas votações nominais de plenário na
    legislatura
    """

    serializer_class = DisciplinaSerializer

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
        Retorna a autoria
        """
        id_parlamentar = self.kwargs["id"]
        return Disciplina.objects.filter(id_parlamentar_parlametria=id_parlamentar)
