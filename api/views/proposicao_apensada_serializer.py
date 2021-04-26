from rest_framework import serializers, generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.model.proposicao_apensada import ProposicaoApensada
from api.model.proposicao import Proposicao


class ProposicaoApensadaSiglaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposicao
        fields = (
            "sigla_camara",
            "sigla_senado"
        )


class ProposicaoApensadaSerializer(serializers.ModelSerializer):
    proposicao_principal = ProposicaoApensadaSiglaSerializer(many=False, read_only=True)

    id_leggo_principal = serializers.CharField(
        source='id_leggo_prop_principal')
    interesse_principal = serializers.CharField(
        source='interesse')
    id_ext_principal = serializers.IntegerField(
        source='id_ext_prop_principal')
    casa_principal = serializers.CharField(
        source='casa_prop_principal')

    class Meta:
        model = ProposicaoApensada
        fields = (
            "id_leggo_principal",
            "interesse_principal",
            "id_ext_principal",
            "casa_principal",
            "proposicao_principal"
        )


class ProposicaoApensadaDetail(generics.ListAPIView):
    """
    Lista de locais capturados para as proposições de um interesse
    """

    serializer_class = ProposicaoApensadaSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "id da proposição no sistema",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs["id"]

        interesseArg = self.request.query_params.get("interesse", "leggo")

        query = (
            ProposicaoApensada.objects.filter(
                id_leggo=id_prop,
                interesse=interesseArg
            )
            .select_related(
                'proposicao_principal'
            )
        )

        return query
