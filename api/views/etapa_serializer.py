from rest_framework import serializers, generics
from api.views.pauta_serializer import PautaHistoricoSerializer
from api.views.entidade_serializer import RelatorSerializer
from api.model.etapa_proposicao import EtapaProposicao


class EtapasSerializer(serializers.ModelSerializer):
    relatoria = RelatorSerializer(many=False, read_only=True)

    class Meta:
        model = EtapaProposicao
        fields = (
            "casa",
            "sigla",
            "data_apresentacao",
            "regime_tramitacao",
            "forma_apreciacao",
            "ementa",
            "url",
            "status",
            "relatoria",
        )


class EtapasDetailSerializer(serializers.ModelSerializer):
    pauta_historico = PautaHistoricoSerializer(many=True, read_only=True)
    relatoria = RelatorSerializer(many=False, read_only=True)

    class Meta:
        model = EtapaProposicao
        fields = (
            "id",
            "id_ext",
            "casa",
            "sigla",
            "data_apresentacao",
            "ano",
            "sigla_tipo",
            "regime_tramitacao",
            "forma_apreciacao",
            "ementa",
            "justificativa",
            "url",
            "casa_origem",
            "em_pauta",
            "status",
            "resumo_tramitacao",
            "comissoes_passadas",
            "pauta_historico",
            "relatoria",
        )


class EtapasList(generics.ListAPIView):
    """
    Lista as etapas de todas as proposições em cada casa de tramitação.
    Retorna os detalhes da tramitação como o regime de tramitação, a forma de apreciação,
    as comissões passadas, dentre outras.
    """

    queryset = EtapaProposicao.objects.prefetch_related("tramitacao")
    serializer_class = EtapasSerializer
