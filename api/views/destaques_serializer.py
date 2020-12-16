from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q, Prefetch
from api.model.destaques import Destaques
from api.views.interesse_serializer import InteresseSerializer
from api.views.etapa_serializer import EtapasSerializer
from api.model.proposicao import Proposicao
from api.utils.filters import get_filtered_interesses


class DestaquesDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destaques
        fields = (
            "id_leggo", "id_ext", "casa", "sigla",
            "criterio_aprovada_em_uma_casa", "fase_global",
            "local", "local_casa", "data_inicio", "data_fim",
            "criterio_avancou_comissoes", "ccj_camara",
            "parecer_aprovado_comissao", "criterio_pressao_alta",
            "maximo_pressao_periodo", "agendas")

class DestaquesSerializer(serializers.ModelSerializer):
    etapas = EtapasSerializer(many=True, read_only=True)
    interesse = InteresseSerializer(many=True, read_only=True)

    class Meta:
        model = Proposicao
        fields = (
            "id",
            "interesse",
            "etapas",
            "id_leggo",
            "sigla_camara",
            "sigla_senado",
            "destaques"
        )


class DestaquesList(generics.ListAPIView):

    serializer_class = DestaquesDetailsSerializer

    def get_queryset(self):
        interesseArg = self.request.query_params.get("interesse")

        if interesseArg is None:
            interesseArg = "leggo"

        interessesFiltered = get_filtered_interesses(interesseArg)

        props = (Destaques.objects
            .filter(Q(criterio_aprovada_em_uma_casa=True) |
                    Q(criterio_avancou_comissoes=True)
            ))

        return props

"""         retorno = (Proposicao.objects.filter(interesse__interesse=interesseArg)
            .distinct()
            .prefetch_related(
                "etapas",
                "progresso",
                Prefetch("etapas__relatoria"),
                Prefetch("interesse", queryset=interessesFiltered),
                Prefetch("destaques", queryset=props)
            )) """
