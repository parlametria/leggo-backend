from rest_framework import serializers, generics

from api.model.proposicao_apensada import ProposicaApensada
from api.utils.filters import (
    get_filtered_interesses,
    get_ultima_proposicao_local
)


class ProposicaApensadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposicaApensada
        fields = (
            "id_leggo",
            "id_leggo_prop_principal"
        )

class ProposicaApensadaList(generics.ListAPIView):
    """
    Lista de locais capturados para as proposições de um interesse
    """

    serializer_class = ProposicaApensadaSerializer

    def get_queryset(self):
        """
        Retorna lista de locais possíveis para um interesse
        """
        interesseArg = self.request.query_params.get("interesse")
        interesses = get_filtered_interesses(interesseArg)

        query = (
            ProposicaApensada.objects.filter(
                id_leggo__in=interesses.values("id_leggo")
            )
        )

        return query
