from rest_framework import serializers, generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.model.proposicao_apensada import ProposicaoApensada


class ProposicaoApensadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposicaoApensada
        fields = (
            "id_leggo",
            "id_leggo_prop_principal",
            "proposicao_principal"
        )


class ProposicaoApensadaDetailSerializer(serializers.Serializer):
    id_leggo_principal = serializers.CharField(
        source='id_leggo_prop_principal')
    interesse_principal = serializers.CharField(
        source='interesse')
    id_ext_principal = serializers.IntegerField(
        source='id_ext_prop_principal')
    casa_principal = serializers.CharField(
        source='casa_prop_principal')
    sigla_camara_principal = serializers.CharField(
        source='proposicao_principal__sigla_camara')
    sigla_senado_principal = serializers.CharField(
        source='proposicao_principal__sigla_senado')


class ProposicaoApensadaDetail(generics.ListAPIView):
    """
    Lista de locais capturados para as proposições de um interesse
    """

    serializer_class = ProposicaoApensadaDetailSerializer

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
            .values(
                'id_leggo_prop_principal', 'interesse',
                'id_ext_prop_principal', 'casa_prop_principal',
                'proposicao_principal__sigla_camara',
                'proposicao_principal__sigla_senado'
            )
        )

        return query
