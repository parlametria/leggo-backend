from rest_framework import serializers, generics, status
from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.proposicao import Proposicao
from api.model.destaques import Destaques
from api.views.temperatura_historico_serializer import TemperaturaHistoricoSerializer
from api.views.etapa_serializer import EtapasSerializer, EtapasDetailSerializer
from api.utils.filters import (
    get_time_filtered_pauta,
    get_filtered_interesses,
    get_filtered_destaques
)
from django.db.models import Prefetch, Count, Q
from api.views.ator_serializer import AtoresProposicoesSerializer
from api.views.interesse_serializer import InteresseProposicaoSerializer
from api.views.autores_proposicao_serializer import AutoresSerializer
from api.views.destaques_serializer import DestaquesDetailsSerializer
from api.model.local_atual_proposicao import LocalAtualProposicao


class ProposicaoDetailSerializer(serializers.ModelSerializer):
    etapas = EtapasDetailSerializer(many=True, read_only=True)
    temperatura_historico = TemperaturaHistoricoSerializer(many=True, read_only=True)
    important_atores = AtoresProposicoesSerializer(many=True, read_only=True)
    interesse = InteresseProposicaoSerializer(many=True, read_only=True)
    autoresProposicao = AutoresSerializer(many=True, read_only=True)
    destaques = DestaquesDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            "id",
            "interesse",
            "autoresProposicao",
            "etapas",
            "id_leggo",
            "temperatura_historico",
            "temperatura_coeficiente",
            # TODO: Remover linha seguinte quando a migração do frontend estiver completa
            "important_atores",
            "anotacao_data_ultima_modificacao",
            "sigla_camara",
            "sigla_senado",
            "destaques"
        )


class ProposicaoSerializer(serializers.ModelSerializer):
    etapas = EtapasSerializer(many=True, read_only=True)
    interesse = InteresseProposicaoSerializer(many=True, read_only=True)
    destaques = DestaquesDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            "interesse",
            "etapas",
            "id_leggo",
            "sigla_camara",
            "sigla_senado",
            "destaques"
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
        destaquesFiltered = (Destaques.objects.filter(
            Q(criterio_aprovada_em_uma_casa=True) |
            Q(criterio_avancou_comissoes=True) |
            Q(criterio_req_urgencia_apresentado=True) |
            Q(criterio_req_urgencia_aprovado=True))
        )

        props = (
            Proposicao.objects.filter(interesse__interesse=interesseArg)
            .distinct()
            .prefetch_related(
                "etapas",
                "progresso",
                Prefetch("etapas__pauta_historico", queryset=pautaQs),
                Prefetch("etapas__relatoria"),
                Prefetch("interesse", queryset=interessesFiltered),
                Prefetch("destaques", queryset=destaquesFiltered)
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


class ProposicaoCountSerializer(serializers.Serializer):
    numero_proposicoes = serializers.IntegerField()


class ProposicaoCountList(APIView):
    """
    Recupera a contagem de proposições monitoradas por interesse e tema
    """

    serializer_class = ProposicaoCountSerializer

    def get(self, request, format=None):

        interesseArg = self.request.query_params.get("interesse")
        temaArg = self.request.query_params.get('tema')
        destaqueArg = self.request.query_params.get('destaque')

        # Adiciona interesse default
        if interesseArg is None:
            interesseArg = "leggo"

        interesses = get_filtered_interesses(interesseArg, temaArg)

        props = Proposicao.objects

        if destaqueArg == 'true':
            destaques = get_filtered_destaques(destaqueArg)
            props = props.filter(id_leggo__in=destaques)

        props = (
            props.filter(id_leggo__in=interesses.values('id_leggo'))
            .distinct()
            .aggregate(numero_proposicoes=Count('id_leggo'))
        )

        return JsonResponse(props, status=status.HTTP_200_OK)
