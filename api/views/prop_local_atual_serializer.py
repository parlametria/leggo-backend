from rest_framework import serializers

from api.model.local_atual_proposicao import LocalAtualProposicao


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
