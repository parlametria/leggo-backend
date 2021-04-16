from rest_framework import serializers, generics

from api.model.local_atual_proposicao import LocalAtualProposicao
from api.utils.filters import (
    get_filtered_interesses,
    get_ultima_proposicao_local
)


class LocalAtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalAtualProposicao
        fields = (
            "sigla_ultimo_local",
            "casa_ultimo_local",
            "data_ultima_situacao",
            "nome_ultimo_local",
            "tipo_local"
        )


class LocalProposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalAtualProposicao
        fields = (
            "sigla_ultimo_local",
            "casa_ultimo_local",
            "nome_ultimo_local",
            "tipo_local"
        )


class LocaisProposicaoList(generics.ListAPIView):
    """
    Lista de locais capturados para as proposições de um interesse
    """

    serializer_class = LocalProposicaoSerializer

    def get_queryset(self):
        """
        Retorna lista de locais possíveis para um interesse
        """
        interesseArg = self.request.query_params.get("interesse")
        interesses = get_filtered_interesses(interesseArg)

        locaisFiltered = get_ultima_proposicao_local()

        query = (
            LocalAtualProposicao.objects.filter(
                id_leggo__in=interesses.values("id_leggo"),
                sigla_ultimo_local__in=locaisFiltered.values("sigla_ultimo_local")
            )
            .values('sigla_ultimo_local', 'casa_ultimo_local',
                    'nome_ultimo_local', 'tipo_local')
            .distinct()
        )

        return query
