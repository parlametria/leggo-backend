from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.proposicao import Proposicao
from api.views.temperatura_historico_serializer import TemperaturaHistoricoSerializer
from api.views.etapa_serializer import EtapasSerializer, EtapasDetailSerializer
from api.utils.filters import get_time_filtered_pauta, get_filtered_interesses
from django.db.models import Prefetch
from api.views.ator_serializer import AtoresProposicoesSerializer
from api.views.interesse_serializer import InteresseSerializer
from api.views.autores_proposicao_serializer import AutoresSerializer


class ProposicaoDetailSerializer(serializers.ModelSerializer):
    etapas = EtapasDetailSerializer(many=True, read_only=True)
    temperatura_historico = TemperaturaHistoricoSerializer(many=True, read_only=True)
    important_atores = AtoresProposicoesSerializer(many=True, read_only=True)
    interesse = InteresseSerializer(many=True, read_only=True)
    autoresProposicao = AutoresSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            "id",
            "interesse",
            "autoresProposicao",
            "etapas",
            "resumo_progresso",
            "id_leggo",
            "temperatura_historico",
            "temperatura_coeficiente",
            "important_atores",
            "anotacao_data_ultima_modificacao",
            "sigla_camara",
            "sigla_senado"
        )


class ProposicaoSerializer(serializers.ModelSerializer):
    etapas = EtapasSerializer(many=True, read_only=True)
    interesse = InteresseSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            "id",
            "interesse",
            "etapas",
            "resumo_progresso",
            "temperatura_coeficiente",
            "id_leggo",
            "anotacao_data_ultima_modificacao",
            "sigla_camara",
            "sigla_senado"
        )


class ProposicaoList(generics.ListAPIView):
    """
    Recupera lista de proposições analisadas pelo leggo de acordo com um interesse
    passado como parâmetro (Exemplo: ?interesse=leggo). O interesse default é leggo.
    Um interesse é um assunto geral
    no qual um conjunto de proposições está relacionado. O primeiro
    interesse analisado pelo Leggo é o da RAC, que é uma rede de
    organizações que atua no Congresso em diferentes eixos como
    Meio Ambiente, Direitos Humanos, Nova Economia e Transparência.
    Outros possíveis interesses seriam Primeira Infância (conjunto
    de proposições ligadas a direitos e deveres relacionados às
    crianças).
    """

    serializer_class = ProposicaoSerializer

    def get_queryset(self):
        pautaQs = get_time_filtered_pauta(self.request)

        interesseArg = self.request.query_params.get("interesse")
        tema_arg = self.request.query_params.get('tema')
        # Adiciona interesse default
        if interesseArg is None:
            interesseArg = "leggo"
        interessesFiltered = get_filtered_interesses(interesseArg, tema_arg)

        props = (
            Proposicao.objects.filter(interesse__interesse=interesseArg)
            .distinct()
            .prefetch_related(
                "etapas",
                "progresso",
                Prefetch("etapas__pauta_historico", queryset=pautaQs),
                Prefetch("etapas__relatoria"),
                Prefetch("interesse", queryset=interessesFiltered),
            )
        )
        return props


class ProposicaoDetail(generics.ListAPIView):
    """
    Recupera os detalhes de uma proposição a partir do id desta proposição
    no sistema Leggo. O interesse ao qual a proposição pertence é passado como
    parâmetro (Exemplo: ?interesse=leggo). O interesse default é leggo.
    Um interesse é um assunto geral
    no qual um conjunto de proposições está relacionado. O primeiro
    interesse analisado pelo Leggo é o da RAC, que é uma rede de
    organizações que atua no Congresso em diferentes eixos como
    Meio Ambiente, Direitos Humanos, Nova Economia e Transparência.
    Outros possíveis interesses seriam Primeira Infância (conjunto
    de proposições ligadas a direitos e deveres relacionados às
    crianças).
    """

    serializer_class = ProposicaoDetailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "id da proposição no sistema",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs["id"]

        interesseArg = self.request.query_params.get("interesse")
        tema_arg = self.request.query_params.get('tema')
        # Adiciona interesse default
        if interesseArg is None:
            interesseArg = "leggo"

        interessesFiltered = get_filtered_interesses(interesseArg, tema_arg)

        return (
            Proposicao.objects.filter(
                id_leggo=id_prop, interesse__interesse=interesseArg
            )
            .distinct()
            .prefetch_related(Prefetch("interesse", queryset=interessesFiltered))
        )
