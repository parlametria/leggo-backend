from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.model.ator import Atores
from api.utils.filters import get_filtered_interesses
from api.utils.peso_politico import get_peso_politico_lista


class PesoPoliticoSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    peso_politico = serializers.FloatField()


class PesoPoliticoLista(generics.ListAPIView):
    """
    Informação sobre o peso político dos parlamentares.
    """

    serializer_class = PesoPoliticoSerializer

    def get_queryset(self):
        """
        Retorna dados de peso político para os atores de um determinado interesse.
        Caso nenhum seja passado, o valor default será leggo.
        """
        interesse_arg = self.request.query_params.get("interesse")
        if interesse_arg is None:
            interesse_arg = "leggo"
        interesses = get_filtered_interesses(interesse_arg)

        lista_ids = list(
            Atores.objects.filter(id_leggo__in=interesses).values_list(
                "id_autor", flat=True
            )
        )

        data = get_peso_politico_lista([1, 23396, 173531])

        return data
