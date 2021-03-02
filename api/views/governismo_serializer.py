from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.model.governismo import Governismo


class GovernismoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governismo
        fields = (
            "id_parlamentar_parlametria",
            "casa",
            "governismo"
        )


class GovernismoList(generics.ListAPIView):
    """
    Dados de governismo dos parlamentares. O governismo é calculado usando a
    técnica de Ideal points com base nas votações nominais de plenário na
    legislatura
    """

    serializer_class = GovernismoSerializer

    def get_queryset(self):
        """
        Retorna o governismo
        """

        return Governismo.objects


class GovernismoParlamentar(generics.ListAPIView):
    """
    Dados de governismo de um parlamentar. O governismo é calculado usando a
    técnica de Ideal points com base nas votações nominais de plenário na
    legislatura
    """

    serializer_class = GovernismoSerializer

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
        return Governismo.objects.filter(id_parlamentar_parlametria=id_parlamentar)
