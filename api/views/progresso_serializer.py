from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q, When, Case, Value, CharField
from api.model.progresso import Progresso
from api.utils.filters import get_filtered_interesses


class ProgressoListSerializer(serializers.Serializer):
    id_leggo = serializers.CharField(source="proposicao__id_leggo")
    fase_global = serializers.CharField()
    local = serializers.CharField()
    data_inicio = serializers.CharField()
    data_fim = serializers.CharField()
    local_casa = serializers.CharField()
    pulou = serializers.BooleanField()
    is_mpv = serializers.BooleanField()


class ProgressoList(generics.ListAPIView):
    """
    Dados do progresso das proposições de um interesse,
    de acordo com uma data de referência
    passada como parâmetro (?data_referencia=yyyy-mm-dd).
    """

    serializer_class = ProgressoListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "interesse", openapi.IN_PATH, "interesse", type=openapi.TYPE_STRING
            )
        ]
    )
    def get_queryset(self):
        """
        Retorna o progresso das proposições de um interesse.
        """

        interesseArg = self.request.query_params.get("interesse", "leggo")
        interesses = get_filtered_interesses(interesseArg)

        queryset = (
            Progresso.objects.filter(
                proposicao__id_leggo__in=interesses.values("id_leggo")
            )
            .exclude(fase_global__icontains="Pré")
            .select_related("proposicao")
            .values(
                "proposicao__id_leggo",
                "proposicao__sigla_camara",
                "proposicao__sigla_senado",
                "fase_global",
                "local",
                "data_inicio",
                "data_fim",
                "local_casa",
                "pulou",
            )
            .annotate(
                is_mpv=Case(
                    When(
                        Q(proposicao__sigla_senado__startswith="MPV")
                        | Q(proposicao__sigla_camara__startswith="MPV"),
                        then=Value("True"),
                    ),
                    default=Value("False"),
                    output_field=CharField(),
                )
            )
        )

        return queryset


class ProgressoByID(generics.ListAPIView):
    """
    Dados do progresso das proposições de um interesse,
    de acordo com uma data de referência
    passada como parâmetro (?data_referencia=yyyy-mm-dd).
    """

    serializer_class = ProgressoListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "interesse", openapi.IN_PATH, "interesse", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "id_leggo", openapi.IN_PATH, "ID Leggo", type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna o progresso de uma proposição, passando o id_leggo.
        """
        id_leggo = self.kwargs["id_leggo"]

        queryset = (
            Progresso.objects.filter(proposicao__id_leggo=id_leggo)
            .exclude(fase_global__icontains="Pré")
            .select_related("proposicao")
            .values(
                "proposicao__id_leggo",
                "proposicao__sigla_camara",
                "proposicao__sigla_senado",
                "fase_global",
                "local",
                "data_inicio",
                "data_fim",
                "local_casa",
                "pulou",
            )
            .annotate(
                is_mpv=Case(
                    When(
                        Q(proposicao__sigla_senado__startswith="MPV")
                        | Q(proposicao__sigla_camara__startswith="MPV"),
                        then=Value("True"),
                    ),
                    default=Value("False"),
                    output_field=CharField(),
                )
            )
        )

        return queryset
